"""HTTP-клиент для API ЦИК РФ.

Эндпоинты:
    - https://cikrf.ru — основной сайт ЦИК РФ
    - https://vybory.izbirkom.ru — ГАС «Выборы» (результаты выборов)

Источники данных:
    - ГАС «Выборы» (vybory.izbirkom.ru) — публичные данные о результатах выборов
    - ЦИК РФ (cikrf.ru) — информация о кандидатах и избирательных кампаниях

Примечание: данные ГАС «Выборы» предоставляются в формате HTML.
Модуль выполняет парсинг HTML-страниц для извлечения структурированных данных.
"""

from __future__ import annotations

import logging
import re
from html.parser import HTMLParser
from typing import Any

from mcp_russia._shared.http_client import http_poluchit, sozdat_klienta

from .constants import (
    CIK_BAZA_API,
    DOLZHNOSTI_FEDERAL,
    GODY_VYBOROV,
    IZBIRATELNYY_KOD_REGIONA,
    IZVESTNYE_VYBORY,
    PARTII_RF,
    SUBYEKTY_RF,
    TIPOVY_VYBORY,
    VYBORY_API,
    VYBORY_BAZA_API,
)
from .schemas import (
    Dolzhnost,
    InformatsiyaPartii,
    Kandidat,
    KandidatKratko,
    ResultatKandidata,
    SubyektRF,
    TipVyborov,
)

logger = logging.getLogger(__name__)


class _VyboryTableParser(HTMLParser):
    """Парсер HTML-таблиц ГАС «Выборы» для извлечения результатов."""

    def __init__(self) -> None:
        """Инициализация парсера HTML-таблиц."""
        super().__init__()
        self._v_yacheyke_dannykh = False
        self._v_yacheyke_zagolovka = False
        self._tekushchaya_stroka: list[str] = []
        self.stroki_tablitsy: list[list[str]] = []
        self._v_zagolovke = False
        self.tekst_zagolovka = ""
        self._v_statistike = False
        self.tekst_statistiki = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Обработка открывающего HTML-тега."""
        slovar_atributov = dict(attrs)
        teg_nizhniy = tag.lower()

        if teg_nizhniy == "td":
            self._v_yacheyke_dannykh = True
            self._tekushchaya_yacheyka = ""
        elif teg_nizhniy == "th":
            self._v_yacheyke_zagolovka = True
            self._tekushchaya_yacheyka = ""
        elif teg_nizhniy == "tr":
            self._tekushchaya_stroka = []
        elif teg_nizhniy in ("h1", "h2", "h3"):
            klass_css = slovar_atributov.get("class", "") or ""
            if "title" in klass_css.lower() or teg_nizhniy == "h1":
                self._v_zagolovke = True
                self.tekst_zagolovka = ""
        elif teg_nizhniy in ("div", "span"):
            klass_css = slovar_atributov.get("class", "") or ""
            if any(klyuch in klass_css.lower() for klyuch in ("stats", "itog", "total")):
                self._v_statistike = True
                self.tekst_statistiki = ""

    def handle_endtag(self, tag: str) -> None:
        """Обработка закрывающего HTML-тега."""
        teg_nizhniy = tag.lower()
        if teg_nizhniy == "td" and self._v_yacheyke_dannykh:
            self._v_yacheyke_dannykh = False
            yacheyka = getattr(self, "_tekushchaya_yacheyka", "").strip()
            self._tekushchaya_stroka.append(yacheyka)
        elif teg_nizhniy == "th" and self._v_yacheyke_zagolovka:
            self._v_yacheyke_zagolovka = False
            yacheyka = getattr(self, "_tekushchaya_yacheyka", "").strip()
            self._tekushchaya_stroka.append(yacheyka)
        elif teg_nizhniy == "tr":
            if self._tekushchaya_stroka:
                self.stroki_tablitsy.append(self._tekushchaya_stroka)
            self._tekushchaya_stroka = []
        elif teg_nizhniy in ("h1", "h2", "h3") and self._v_zagolovke:
            self._v_zagolovke = False
        elif teg_nizhniy in ("div", "span") and self._v_statistike:
            self._v_statistike = False

    def handle_data(self, data: str) -> None:
        """Обработка текстового содержимого HTML."""
        tekst = data.strip()
        if not tekst:
            return
        if self._v_yacheyke_dannykh or self._v_yacheyke_zagolovka:
            tekushchaya_yacheyka_tekst = getattr(self, "_tekushchaya_yacheyka", "")
            self._tekushchaya_yacheyka = (
                tekushchaya_yacheyka_tekst + " " + tekst if tekushchaya_yacheyka_tekst else tekst
            )
        if self._v_zagolovke:
            self.tekst_zagolovka += tekst + " "
        if self._v_statistike:
            self.tekst_statistiki += tekst + " "


def _razobrat_chislo(tekst: str) -> int:
    """Извлечь целое число из текста (убрать пробелы, %, и т.д.)."""
    ochishchennoe = re.sub(r"[^\d]", "", tekst.split(",")[0].split(".")[0])
    return int(ochishchennoe) if ochishchennoe else 0


def _razobrat_veshchestvennoe(tekst: str) -> float:
    """Извлечь число с плавающей точкой из текста."""
    sovpadenie = re.search(r"[\d]+[.,][\d]+", tekst)
    if sovpadenie:
        return float(sovpadenie.group().replace(",", "."))
    sovpadenie = re.search(r"[\d]+", tekst)
    return float(sovpadenie.group()) if sovpadenie else 0.0


async def _zaprosit_html_vyborov(
    tvd: str,
    vrn: str,
    subiekt: int = 0,
    podregion: int = 0,
    tip_golosovaniya: int = 242,
    vibid: str | None = None,
) -> str | None:
    """Получить HTML-страницу результатов выборов из ГАС «Выборы»."""
    parametry: dict[str, Any] = {
        "action": "show",
        "root": 1,
        "tvd": tvd,
        "vrn": vrn,
        "prver": 0,
        "pronetvd": "null",
        "region": subiekt,
        "sub_region": podregion,
        "type": tip_golosovaniya,
        "vibid": vibid or vrn,
    }
    adres_url = f"{VYBORY_API}/izbirkom"
    try:
        async with sozdat_klienta(
            bazovyy_adres_url=VYBORY_BAZA_API,
            zagolovki={"Accept": "text/html,application/xhtml+xml"},
            taimaut=30.0,
        ) as klient:
            otvet = await klient.get(adres_url, params=parametry)
            otvet.raise_for_status()
            return otvet.text
    except Exception as exc:
        logger.warning("Не удалось получить страницу ГАС «Выборы» %s: %s", adres_url, exc)
        return None


async def _zaprosit_json_tsik(put_api: str, parametry: dict[str, Any] | None = None) -> Any:
    """Получить JSON данные из API cikrf.ru."""
    adres_url = f"{CIK_BAZA_API}{put_api}"
    try:
        return await http_poluchit(adres_url, parametry=parametry, taimaut=15.0, maks_povtorov=1)
    except Exception as exc:
        logger.debug("CIK API %s недоступен: %s", adres_url, exc)
        return None


def _nayti_vybory_po_godu_tipu(god: int, tip: int | None = None) -> dict[str, Any] | None:
    """Найти известные выборы по году и типу."""
    for znachenie in IZVESTNYE_VYBORY.values():
        if znachenie["god"] == god and (tip is None or znachenie["tip"] == tip):
            return znachenie
    return None


def _razobrat_rezultaty_iz_html(html: str) -> list[ResultatKandidata]:
    """Извлечь результаты кандидатов из HTML ГАС «Выборы»."""
    razobratchik = _VyboryTableParser()
    try:
        razobratchik.feed(html)
    except Exception as exc:
        logger.warning("Ошибка парсинга HTML: %s", exc)
        return []

    rezultaty: list[ResultatKandidata] = []
    for stroka_tablitsy in razobratchik.stroki_tablitsy:
        if len(stroka_tablitsy) < 4:
            continue
        fio = ""
        partia = ""
        golosov = 0
        procent = 0.0
        izbrann = False

        for indeks, yacheyka in enumerate(stroka_tablitsy):
            yacheyka_nizhniy = yacheyka.lower()
            if indeks == 1 and len(yacheyka) > 2:
                fio = yacheyka
            elif indeks == 2 and len(yacheyka) > 1:
                partia = yacheyka
            if "%" in yacheyka:
                procent = _razobrat_veshchestvennoe(yacheyka)
            if "избран" in yacheyka_nizhniy or "избрана" in yacheyka_nizhniy:
                izbrann = True

        for yacheyka in stroka_tablitsy:
            tsifry_stroka = re.sub(r"[^\d]", "", yacheyka)
            if tsifry_stroka and 100 < len(tsifry_stroka) < 15 and fio:
                golosov = int(tsifry_stroka)
                break

        if fio:
            for yacheyka in stroka_tablitsy:
                sovpadenie = re.match(r"^[\d\s]+$", yacheyka.replace("\xa0", "").strip())
                if sovpadenie and fio:
                    znachenie = _razobrat_chislo(yacheyka)
                    if znachenie > 0:
                        golosov = znachenie
                        break

        if fio:
            rezultaty.append(
                ResultatKandidata(
                    kandidat_identifikator="",
                    fio=fio,
                    partia=partia,
                    golosov=golosov,
                    procent=procent,
                    izbrann=izbrann,
                )
            )

    return rezultaty


def _razobrat_yavku_iz_html(html: str) -> dict[str, Any]:
    """Извлечь данные о явке из HTML ГАС «Выборы»."""
    rezultat: dict[str, Any] = {
        "yavka_procent": 0.0,
        "vseh_izbirateley": 0,
        "progalosovalo": 0,
        "deystvitelnykh_byulleteney": 0,
        "nedeystvitelnykh_byulleteney": 0,
    }

    yavka_match = re.search(r"явк[аи][^<>]*?([\d]+[.,][\d]+)\s*%", html, re.IGNORECASE)
    if yavka_match:
        rezultat["yavka_procent"] = float(yavka_match.group(1).replace(",", "."))

    vse_match = re.search(r"число избирателей[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if vse_match:
        rezultat["vseh_izbirateley"] = _razobrat_chislo(vse_match.group(1))

    progol_match = re.search(r"проголосовало[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if progol_match:
        rezultat["progalosovalo"] = _razobrat_chislo(progol_match.group(1))

    deystv_match = re.search(r"действительн[а-яё]+[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if deystv_match:
        rezultat["deystvitelnykh_byulleteney"] = _razobrat_chislo(deystv_match.group(1))

    nedeystv_match = re.search(r"недействительн[а-яё]+[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if nedeystv_match:
        rezultat["nedeystvitelnykh_byulleteney"] = _razobrat_chislo(nedeystv_match.group(1))

    return rezultat


def _razobrat_kandidatov_iz_html(html: str) -> list[KandidatKratko]:
    """Извлечь список кандидатов из HTML ГАС «Выборы»."""
    razobratchik = _VyboryTableParser()
    try:
        razobratchik.feed(html)
    except Exception as exc:
        logger.warning("Ошибка парсинга HTML кандидатов: %s", exc)
        return []

    kandidaty: list[KandidatKratko] = []
    for stroka_tablitsy in razobratchik.stroki_tablitsy:
        if len(stroka_tablitsy) < 3:
            continue
        fio = ""
        partia = ""
        sostoyanie = ""
        dolzhnost = ""
        subiekt_str = ""
        kandidat_identifikator = ""

        for indeks, yacheyka in enumerate(stroka_tablitsy):
            if indeks == 0 and re.match(r"^\d+$", yacheyka.strip()):
                kandidat_identifikator = yacheyka.strip()
            elif indeks == 1 and len(yacheyka) > 2:
                fio = yacheyka.strip()
            elif indeks == 2 and len(yacheyka) > 1:
                partia = yacheyka.strip()
            elif "зарегистрирован" in yacheyka.lower():
                sostoyanie = "Зарегистрирован"
            elif "снят" in yacheyka.lower():
                sostoyanie = "Снят"
            elif "исключён" in yacheyka.lower():
                sostoyanie = "Исключён"

        if fio:
            kandidaty.append(
                KandidatKratko(
                    identifikator=kandidat_identifikator or fio,
                    fio=fio,
                    partia=partia,
                    dolzhnost=dolzhnost,
                    subiekt=subiekt_str,
                    sostoyanie=sostoyanie,
                )
            )

    return kandidaty


async def tipy_vyborov() -> list[TipVyborov]:
    """Получить список типов выборов."""
    rezultaty: list[TipVyborov] = []
    for znachenie in TIPOVY_VYBORY.values():
        kod: Any = znachenie["kod"]
        nazvanie: Any = znachenie["nazvanie"]
        rezultaty.append(
            TipVyborov(kod=kod if isinstance(kod, int) else int(str(kod)), nazvanie=str(nazvanie))
        )
    return rezultaty


async def subyekty_rf() -> list[SubyektRF]:
    """Получить справочник субъектов Российской Федерации."""
    return [SubyektRF(kod=s["kod"], nazvanie=s["nazvanie"], okato=s["okato"]) for s in SUBYEKTY_RF]


async def dolzhnosti_federal() -> list[Dolzhnost]:
    """Получить список федеральных избирательных должностей."""
    rezultaty: list[Dolzhnost] = []
    for d in DOLZHNOSTI_FEDERAL:
        kod: Any = d["kod"]
        rezultaty.append(
            Dolzhnost(
                kod=kod if isinstance(kod, int) else int(str(kod)),
                nazvanie=str(d["nazvanie"]),
                uroven=str(d["uroven"]),
            )
        )
    return rezultaty


async def partii_rf() -> list[InformatsiyaPartii]:
    """Получить справочник политических партий РФ."""
    return [
        InformatsiyaPartii(
            nazvanie=p["nazvanie"], kratkoe_nazvanie=p["korotkoe_nazvanie"], tsvet=p["tsvet"]
        )
        for p in PARTII_RF
    ]


async def gody_vyborov() -> list[int]:
    """Получить список годов основных федеральных выборов."""
    return GODY_VYBOROV.copy()


async def spisok_vyborov(
    god: int | None = None,
    tip: int | None = None,
    subiekt: int | None = None,
) -> list[dict[str, Any]]:
    """Получить список выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов.
        subiekt: Номер региона.

    Возвращает:
        Список выборов с метаданными.
    """
    if god is not None and tip is not None:
        vybory = _nayti_vybory_po_godu_tipu(god, tip)
        if vybory:
            return [vybory]

    rezultaty = []
    for klyuch, znachenie in IZVESTNYE_VYBORY.items():
        if god is not None and znachenie["god"] != god:
            continue
        if tip is not None and znachenie["tip"] != tip:
            continue
        if subiekt is not None and znachenie.get("subiekt", 0) != subiekt:
            continue
        rezultaty.append({**znachenie, "klyuch": klyuch})

    if not rezultaty and god is not None:
        adres_url = f"{VYBORY_API}/izbirkom"
        parametry: dict[str, Any] = {
            "action": "show",
            "root": 1,
            "region": subiekt or 0,
            "type": 0,
        }
        try:
            async with sozdat_klienta(
                bazovyy_adres_url=VYBORY_BAZA_API,
                zagolovki={"Accept": "text/html,application/xhtml+xml"},
                taimaut=20.0,
            ) as klient:
                otvet = await klient.get(adres_url, params=parametry)
                otvet.raise_for_status()
                html_tekst = otvet.text
                shablon_goda = re.compile(rf"\b{god}\b")
                if shablon_goda.search(html_tekst):
                    sovpadenie_zagolovka = re.search(
                        r"<h[12][^>]*>([^<]+)</h[12]>", html_tekst, re.IGNORECASE
                    )
                    if sovpadenie_zagolovka:
                        rezultaty.append(
                            {
                                "nazvanie": sovpadenie_zagolovka.group(1).strip(),
                                "tip": tip or 0,
                                "god": god,
                                "tvd": "",
                                "vrn": "",
                                "data": str(god),
                                "subiekt": subiekt or 0,
                            }
                        )
        except Exception as exc:
            logger.debug("Не удалось получить список выборов: %s", exc)

    return rezultaty


async def poisk_kandidata(
    fio: str,
    god: int | None = None,
    subiekt: str | None = None,
) -> list[KandidatKratko]:
    """Поиск кандидата по ФИО в ГАС «Выборы».

    Аргументы:
        fio: Фамилия, имя или отчество (частичное совпадение).
        god: Год выборов (необязательно).
        subiekt: Код субъекта РФ (необязательно).

    Возвращает:
        Список найденных кандидатов.
    """
    adres_url_poiska = f"{VYBORY_API}/izbirkom"
    nomer_regiona = IZBIRATELNYY_KOD_REGIONA.get(subiekt, 0) if subiekt else 0

    vybory_info = None
    if god is not None:
        for znachenie in IZVESTNYE_VYBORY.values():
            if znachenie["god"] == god:
                vybory_info = znachenie
                break

    parametry: dict[str, Any] = {
        "action": "show",
        "root": 1,
        "region": nomer_regiona,
        "sub_region": 0,
    }
    if vybory_info:
        parametry["tvd"] = vybory_info["tvd"]
        parametry["vrn"] = vybory_info["vrn"]
        parametry["type"] = vybory_info.get("tip", 242)
        parametry["vibid"] = vybory_info["vrn"]

    try:
        async with sozdat_klienta(
            bazovyy_adres_url=VYBORY_BAZA_API,
            zagolovki={"Accept": "text/html,application/xhtml+xml"},
            taimaut=20.0,
        ) as klient:
            otvet = await klient.get(adres_url_poiska, params=parametry)
            otvet.raise_for_status()
            html_tekst = otvet.text
            vse_kandidaty = _razobrat_kandidatov_iz_html(html_tekst)

            fio_nizhniy = fio.lower()
            otfiltrovannye = [
                klyuch for klyuch in vse_kandidaty if fio_nizhniy in klyuch.fio.lower()
            ]

            if otfiltrovannye:
                return otfiltrovannye
            return vse_kandidaty[:20]

    except Exception as exc:
        logger.warning("Поиск кандидата '%s' не удался: %s", fio, exc)

    cik_dannye = await _zaprosit_json_tsik(
        "/api/elections/candidates",
        {"fio": fio, "year": god, "region": subiekt},
    )
    if isinstance(cik_dannye, list):
        rezultaty = []
        for zapis in cik_dannye:
            if not isinstance(zapis, dict):
                continue
            rezultaty.append(
                KandidatKratko(
                    identifikator=str(zapis.get("id", "")),
                    fio=str(zapis.get("fio", zapis.get("name", ""))),
                    partia=str(zapis.get("party", zapis.get("partia", ""))),
                    dolzhnost=str(zapis.get("position", zapis.get("dolzhnost", ""))),
                    subiekt=str(zapis.get("region", "")),
                    sostoyanie=str(zapis.get("status", "")),
                )
            )
        return rezultaty

    return []


async def kandidat_podrobno(
    kandidat_identifikator: str,
    god: int | None = None,
) -> Kandidat | None:
    """Получить подробную информацию о кандидате из ГАС «Выборы».

    Аргументы:
        kandidat_identifikator: ID кандидата или ФИО.
        god: Год выборов (необязательно).

    Возвращает:
        Подробная информация о кандидате или None.
    """
    cik_dannye = await _zaprosit_json_tsik(
        f"/api/elections/candidates/{kandidat_identifikator}",
        {"year": god},
    )
    if isinstance(cik_dannye, dict):
        return Kandidat(
            identifikator=str(cik_dannye.get("id", kandidat_identifikator)),
            fio=str(cik_dannye.get("fio", cik_dannye.get("name", ""))),
            data_rozhdeniya=str(
                cik_dannye.get("birthDate", cik_dannye.get("data_rozhdeniya", ""))
            ),
            mesto_rozhdeniya=str(
                cik_dannye.get("birthPlace", cik_dannye.get("mesto_rozhdeniya", ""))
            ),
            partia=str(cik_dannye.get("party", cik_dannye.get("partia", ""))),
            dolzhnost=str(cik_dannye.get("position", cik_dannye.get("dolzhnost", ""))),
            subiekt=str(cik_dannye.get("region", "")),
            obrazovanie=str(cik_dannye.get("education", cik_dannye.get("obrazovanie", ""))),
            mesto_raboty=str(cik_dannye.get("workPlace", cik_dannye.get("mesto_raboty", ""))),
            dolzhnost_rabota=str(
                cik_dannye.get("workPosition", cik_dannye.get("dolzhnost_rabota", ""))
            ),
            dokhod=str(cik_dannye.get("income", cik_dannye.get("dokhod", ""))),
            scheta=str(cik_dannye.get("bankAccounts", cik_dannye.get("scheta", ""))),
            nedvizhimost=str(cik_dannye.get("realEstate", cik_dannye.get("nedvizhimost", ""))),
            transport=str(cik_dannye.get("vehicles", cik_dannye.get("transport", ""))),
        )

    vybory_info = None
    if god is not None:
        for znachenie in IZVESTNYE_VYBORY.values():
            if znachenie["god"] == god:
                vybory_info = znachenie
                break

    if vybory_info:
        html_tekst = await _zaprosit_html_vyborov(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            subiekt=0,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html_tekst:
            kandidaty = _razobrat_kandidatov_iz_html(html_tekst)
            for klyuch in kandidaty:
                if (
                    klyuch.identifikator == kandidat_identifikator
                    or kandidat_identifikator.lower() in klyuch.fio.lower()
                ):
                    return Kandidat(
                        identifikator=klyuch.identifikator,
                        fio=klyuch.fio,
                        partia=klyuch.partia,
                        dolzhnost=klyuch.dolzhnost,
                        subiekt=klyuch.subiekt,
                        sostoyanie=klyuch.sostoyanie,
                    )

    return None


async def rezultaty_vyborov(
    god: int,
    tip: int | None = None,
    subiekt: str | None = None,
) -> list[ResultatKandidata]:
    """Получить результаты выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        subiekt: Код субъекта РФ (необязательно).

    Возвращает:
        Список результатов кандидатов.
    """
    vybory_info = _nayti_vybory_po_godu_tipu(god, tip)

    if vybory_info:
        nomer_regiona = 0
        if subiekt and subiekt in IZBIRATELNYY_KOD_REGIONA:
            nomer_regiona = IZBIRATELNYY_KOD_REGIONA[subiekt]

        html_tekst = await _zaprosit_html_vyborov(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            subiekt=nomer_regiona,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html_tekst:
            rezultaty = _razobrat_rezultaty_iz_html(html_tekst)
            if rezultaty:
                return rezultaty

    cik_dannye = await _zaprosit_json_tsik(
        "/api/elections/results",
        {"year": god, "type": tip, "region": subiekt},
    )
    if isinstance(cik_dannye, dict):
        elementy = cik_dannye.get("results", cik_dannye.get("candidates", []))
        if isinstance(elementy, list):
            rezultaty = []
            for zapis in elementy:
                if not isinstance(zapis, dict):
                    continue
                rezultaty.append(
                    ResultatKandidata(
                        kandidat_identifikator=str(zapis.get("id", "")),
                        fio=str(zapis.get("fio", zapis.get("name", ""))),
                        partia=str(zapis.get("party", zapis.get("partia", ""))),
                        golosov=int(str(zapis.get("votes", zapis.get("golosov", 0)))),
                        procent=float(str(zapis.get("percent", zapis.get("procent", 0.0)))),
                        izbrann=bool(zapis.get("elected", zapis.get("izbrann", False))),
                    )
                )
            return rezultaty

    return []


async def yavka_i_itogi(
    god: int,
    tip: int | None = None,
    subiekt: str | None = None,
) -> dict[str, Any]:
    """Получить данные о явке и итогах выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        subiekt: Код субъекта РФ (необязательно).

    Возвращает:
        Словарь с итогами выборов.
    """
    vybory_info = _nayti_vybory_po_godu_tipu(god, tip)

    if vybory_info:
        nomer_regiona = 0
        if subiekt and subiekt in IZBIRATELNYY_KOD_REGIONA:
            nomer_regiona = IZBIRATELNYY_KOD_REGIONA[subiekt]

        html_tekst = await _zaprosit_html_vyborov(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            subiekt=nomer_regiona,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html_tekst:
            yavka = _razobrat_yavku_iz_html(html_tekst)
            if yavka["vseh_izbirateley"] > 0 or yavka["yavka_procent"] > 0:
                return {
                    "god": god,
                    "tip": tip,
                    "subiekt": subiekt,
                    "nazvanie": str(vybory_info["nazvanie"]),
                    "data": str(vybory_info["data"]),
                    **yavka,
                    "istochnik": f"ГАС «Выборы» ({VYBORY_BAZA_API})",
                }

    cik_dannye = await _zaprosit_json_tsik(
        "/api/elections/turnout",
        {"year": god, "type": tip, "region": subiekt},
    )
    if isinstance(cik_dannye, dict):
        return {
            "god": god,
            "tip": tip,
            "subiekt": subiekt,
            "nazvanie": cik_dannye.get("name", ""),
            "data": cik_dannye.get("date", ""),
            "yavka_procent": cik_dannye.get("turnout", cik_dannye.get("yavka_procent", 0.0)),
            "vseh_izbirateley": cik_dannye.get(
                "totalVoters", cik_dannye.get("vseh_izbirateley", 0)
            ),
            "progalosovalo": cik_dannye.get("voted", cik_dannye.get("progalosovalo", 0)),
            "deystvitelnykh_byulleteney": cik_dannye.get("validBallots", 0),
            "nedeystvitelnykh_byulleteney": cik_dannye.get("invalidBallots", 0),
            "istochnik": f"ЦИК РФ ({CIK_BAZA_API})",
        }

    return {
        "god": god,
        "tip": tip,
        "subiekt": subiekt,
        "nazvanie": "",
        "data": "",
        "yavka_procent": 0.0,
        "vseh_izbirateley": 0,
        "progalosovalo": 0,
        "deystvitelnykh_byulleteney": 0,
        "nedeystvitelnykh_byulleteney": 0,
        "istochnik": f"ЦИК РФ / ГАС «Выборы» ({CIK_BAZA_API}, {VYBORY_BAZA_API})",
    }
