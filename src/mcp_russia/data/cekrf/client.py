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

from mcp_russia._shared.http_client import create_client, http_get

from .constants import (
    CIK_API_BASE,
    DOLZHNOSTI_FEDERAL,
    GODY_VYBOROV,
    IZBIRATELNYY_KOD_REGIONA,
    IZVESTNYE_VYBORY,
    PARTII_RF,
    SUBYEKTY_RF,
    TIPOVY_VYBORY,
    VYBORY_API,
    VYBORY_API_BASE,
)
from .schemas import (
    Dolzhnost,
    Kandidat,
    KandidatKratko,
    PartiaInfo,
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
        self._in_td = False
        self._in_th = False
        self._current_row: list[str] = []
        self.rows: list[list[str]] = []
        self._in_title = False
        self.title_text = ""
        self._in_stats = False
        self.stats_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Обработка открывающего HTML-тега."""
        attr_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == "td":
            self._in_td = True
            self._current_cell = ""
        elif tag_lower == "th":
            self._in_th = True
            self._current_cell = ""
        elif tag_lower == "tr":
            self._current_row = []
        elif tag_lower in ("h1", "h2", "h3"):
            cls = attr_dict.get("class", "") or ""
            if "title" in cls.lower() or tag_lower == "h1":
                self._in_title = True
                self.title_text = ""
        elif tag_lower in ("div", "span"):
            cls = attr_dict.get("class", "") or ""
            if any(k in cls.lower() for k in ("stats", "itog", "total")):
                self._in_stats = True
                self.stats_text = ""

    def handle_endtag(self, tag: str) -> None:
        """Обработка закрывающего HTML-тега."""
        tag_lower = tag.lower()
        if tag_lower == "td" and self._in_td:
            self._in_td = False
            cell = getattr(self, "_current_cell", "").strip()
            self._current_row.append(cell)
        elif tag_lower == "th" and self._in_th:
            self._in_th = False
            cell = getattr(self, "_current_cell", "").strip()
            self._current_row.append(cell)
        elif tag_lower == "tr":
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = []
        elif tag_lower in ("h1", "h2", "h3") and self._in_title:
            self._in_title = False
        elif tag_lower in ("div", "span") and self._in_stats:
            self._in_stats = False

    def handle_data(self, data: str) -> None:
        """Обработка текстового содержимого HTML."""
        text = data.strip()
        if not text:
            return
        if self._in_td or self._in_th:
            current = getattr(self, "_current_cell", "")
            self._current_cell = current + " " + text if current else text
        if self._in_title:
            self.title_text += text + " "
        if self._in_stats:
            self.stats_text += text + " "


def _parse_number(text: str) -> int:
    """Извлечь целое число из текста (убрать пробелы, %, и т.д.)."""
    cleaned = re.sub(r"[^\d]", "", text.split(",")[0].split(".")[0])
    return int(cleaned) if cleaned else 0


def _parse_float(text: str) -> float:
    """Извлечь число с плавающей точкой из текста."""
    m = re.search(r"[\d]+[.,][\d]+", text)
    if m:
        return float(m.group().replace(",", "."))
    m = re.search(r"[\d]+", text)
    return float(m.group()) if m else 0.0


async def _fetch_vybory_html(
    tvd: str,
    vrn: str,
    region: int = 0,
    podregion: int = 0,
    tip_golosovaniya: int = 242,
    vibid: str | None = None,
) -> str | None:
    """Получить HTML-страницу результатов выборов из ГАС «Выборы»."""
    params: dict[str, Any] = {
        "action": "show",
        "root": 1,
        "tvd": tvd,
        "vrn": vrn,
        "prver": 0,
        "pronetvd": "null",
        "region": region,
        "sub_region": podregion,
        "type": tip_golosovaniya,
        "vibid": vibid or vrn,
    }
    url = f"{VYBORY_API}/izbirkom"
    try:
        async with create_client(
            base_url=VYBORY_API_BASE,
            headers={"Accept": "text/html,application/xhtml+xml"},
            timeout=30.0,
        ) as c:
            resp = await c.get(url, params=params)
            resp.raise_for_status()
            return resp.text
    except Exception as exc:
        logger.warning("Не удалось получить страницу ГАС «Выборы» %s: %s", url, exc)
        return None


async def _fetch_cik_json(path: str, params: dict[str, Any] | None = None) -> Any:
    """Получить JSON данные из API cikrf.ru."""
    url = f"{CIK_API_BASE}{path}"
    try:
        return await http_get(url, params=params, timeout=15.0, max_retries=1)
    except Exception as exc:
        logger.debug("CIK API %s недоступен: %s", url, exc)
        return None


def _find_vybory_by_god_tip(god: int, tip: int | None = None) -> dict[str, Any] | None:
    """Найти известные выборы по году и типу."""
    for v in IZVESTNYE_VYBORY.values():
        if v["god"] == god and (tip is None or v["tip"] == tip):
            return v
    return None


def _parse_results_from_html(html: str) -> list[ResultatKandidata]:
    """Извлечь результаты кандидатов из HTML ГАС «Выборы»."""
    parser = _VyboryTableParser()
    try:
        parser.feed(html)
    except Exception as exc:
        logger.warning("Ошибка парсинга HTML: %s", exc)
        return []

    results: list[ResultatKandidata] = []
    for row in parser.rows:
        if len(row) < 4:
            continue
        fio = ""
        partia = ""
        golosov = 0
        procent = 0.0
        izbrann = False

        for i, cell in enumerate(row):
            cell_lower = cell.lower()
            if i == 1 and len(cell) > 2:
                fio = cell
            elif i == 2 and len(cell) > 1:
                partia = cell
            if "%" in cell:
                procent = _parse_float(cell)
            if "избран" in cell_lower or "избрана" in cell_lower:
                izbrann = True

        for cell in row:
            digits = re.sub(r"[^\d]", "", cell)
            if digits and 100 < len(digits) < 15 and fio:
                golosov = int(digits)
                break

        if fio:
            for cell in row:
                m = re.match(r"^[\d\s]+$", cell.replace("\xa0", "").strip())
                if m and fio:
                    val = _parse_number(cell)
                    if val > 0:
                        golosov = val
                        break

        if fio:
            results.append(
                ResultatKandidata(
                    kandidat_id="",
                    fio=fio,
                    partia=partia,
                    golosov=golosov,
                    procent=procent,
                    izbrann=izbrann,
                )
            )

    return results


def _parse_turnout_from_html(html: str) -> dict[str, Any]:
    """Извлечь данные о явке из HTML ГАС «Выборы»."""
    result: dict[str, Any] = {
        "yavka_procent": 0.0,
        "vseh_izbirateley": 0,
        "progalosovalo": 0,
        "deystvitelnykh_byulleteney": 0,
        "nedeystvitelnykh_byulleteney": 0,
    }

    yavka_match = re.search(r"явк[аи][^<>]*?([\d]+[.,][\d]+)\s*%", html, re.IGNORECASE)
    if yavka_match:
        result["yavka_procent"] = float(yavka_match.group(1).replace(",", "."))

    vse_match = re.search(r"число избирателей[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if vse_match:
        result["vseh_izbirateley"] = _parse_number(vse_match.group(1))

    progol_match = re.search(r"проголосовало[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if progol_match:
        result["progalosovalo"] = _parse_number(progol_match.group(1))

    deystv_match = re.search(r"действительн[а-яё]+[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if deystv_match:
        result["deystvitelnykh_byulleteney"] = _parse_number(deystv_match.group(1))

    nedeystv_match = re.search(r"недействительн[а-яё]+[^<>]*?([\d\s]+)", html, re.IGNORECASE)
    if nedeystv_match:
        result["nedeystvitelnykh_byulleteney"] = _parse_number(nedeystv_match.group(1))

    return result


def _parse_candidates_from_html(html: str) -> list[KandidatKratko]:
    """Извлечь список кандидатов из HTML ГАС «Выборы»."""
    parser = _VyboryTableParser()
    try:
        parser.feed(html)
    except Exception as exc:
        logger.warning("Ошибка парсинга HTML кандидатов: %s", exc)
        return []

    kandidaty: list[KandidatKratko] = []
    for row in parser.rows:
        if len(row) < 3:
            continue
        fio = ""
        partia = ""
        status = ""
        dolzhnost = ""
        region = ""
        kandidat_id = ""

        for i, cell in enumerate(row):
            if i == 0 and re.match(r"^\d+$", cell.strip()):
                kandidat_id = cell.strip()
            elif i == 1 and len(cell) > 2:
                fio = cell.strip()
            elif i == 2 and len(cell) > 1:
                partia = cell.strip()
            elif "зарегистрирован" in cell.lower():
                status = "Зарегистрирован"
            elif "снят" in cell.lower():
                status = "Снят"
            elif "исключён" in cell.lower():
                status = "Исключён"

        if fio:
            kandidaty.append(
                KandidatKratko(
                    identifikator=kandidat_id or fio,
                    fio=fio,
                    partia=partia,
                    dolzhnost=dolzhnost,
                    region=region,
                    status=status,
                )
            )

    return kandidaty


async def tipy_vyborov() -> list[TipVyborov]:
    """Получить список типов выборов."""
    results: list[TipVyborov] = []
    for v in TIPOVY_VYBORY.values():
        code: Any = v["kod"]
        name: Any = v["nazvanie"]
        results.append(
            TipVyborov(kod=code if isinstance(code, int) else int(str(code)), nazvanie=str(name))
        )
    return results


async def subyekty_rf() -> list[SubyektRF]:
    """Получить справочник субъектов Российской Федерации."""
    return [SubyektRF(kod=s["kod"], nazvanie=s["nazvanie"], okato=s["okato"]) for s in SUBYEKTY_RF]


async def dolzhnosti_federal() -> list[Dolzhnost]:
    """Получить список федеральных избирательных должностей."""
    results: list[Dolzhnost] = []
    for d in DOLZHNOSTI_FEDERAL:
        code: Any = d["kod"]
        results.append(
            Dolzhnost(
                kod=code if isinstance(code, int) else int(str(code)),
                nazvanie=str(d["nazvanie"]),
                uroven=str(d["uroven"]),
            )
        )
    return results


async def partii_rf() -> list[PartiaInfo]:
    """Получить справочник политических партий РФ."""
    return [
        PartiaInfo(
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
    region: int | None = None,
) -> list[dict[str, Any]]:
    """Получить список выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов.
        region: Номер региона.

    Возвращает:
        Список выборов с метаданными.
    """
    if god is not None and tip is not None:
        vybory = _find_vybory_by_god_tip(god, tip)
        if vybory:
            return [vybory]

    results = []
    for key, v in IZVESTNYE_VYBORY.items():
        if god is not None and v["god"] != god:
            continue
        if tip is not None and v["tip"] != tip:
            continue
        if region is not None and v.get("region", 0) != region:
            continue
        results.append({**v, "key": key})

    if not results and god is not None:
        url = f"{VYBORY_API}/izbirkom"
        params: dict[str, Any] = {
            "action": "show",
            "root": 1,
            "region": region or 0,
            "type": 0,
        }
        try:
            async with create_client(
                base_url=VYBORY_API_BASE,
                headers={"Accept": "text/html,application/xhtml+xml"},
                timeout=20.0,
            ) as c:
                resp = await c.get(url, params=params)
                resp.raise_for_status()
                html = resp.text
                year_pattern = re.compile(rf"\b{god}\b")
                if year_pattern.search(html):
                    title_match = re.search(r"<h[12][^>]*>([^<]+)</h[12]>", html, re.IGNORECASE)
                    if title_match:
                        results.append(
                            {
                                "nazvanie": title_match.group(1).strip(),
                                "tip": tip or 0,
                                "god": god,
                                "tvd": "",
                                "vrn": "",
                                "data": str(god),
                                "region": region or 0,
                            }
                        )
        except Exception as exc:
            logger.debug("Не удалось получить список выборов: %s", exc)

    return results


async def poisk_kandidata(
    fio: str,
    god: int | None = None,
    region: str | None = None,
) -> list[KandidatKratko]:
    """Поиск кандидата по ФИО в ГАС «Выборы».

    Аргументы:
        fio: Фамилия, имя или отчество (частичное совпадение).
        god: Год выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Возвращает:
        Список найденных кандидатов.
    """
    search_url = f"{VYBORY_API}/izbirkom"
    region_num = IZBIRATELNYY_KOD_REGIONA.get(region, 0) if region else 0

    vybory_info = None
    if god is not None:
        for v in IZVESTNYE_VYBORY.values():
            if v["god"] == god:
                vybory_info = v
                break

    params: dict[str, Any] = {
        "action": "show",
        "root": 1,
        "region": region_num,
        "sub_region": 0,
    }
    if vybory_info:
        params["tvd"] = vybory_info["tvd"]
        params["vrn"] = vybory_info["vrn"]
        params["type"] = vybory_info.get("tip", 242)
        params["vibid"] = vybory_info["vrn"]

    try:
        async with create_client(
            base_url=VYBORY_API_BASE,
            headers={"Accept": "text/html,application/xhtml+xml"},
            timeout=20.0,
        ) as c:
            resp = await c.get(search_url, params=params)
            resp.raise_for_status()
            html = resp.text
            all_kandidaty = _parse_candidates_from_html(html)

            fio_lower = fio.lower()
            filtered = [k for k in all_kandidaty if fio_lower in k.fio.lower()]

            if filtered:
                return filtered
            return all_kandidaty[:20]

    except Exception as exc:
        logger.warning("Поиск кандидата '%s' не удался: %s", fio, exc)

    cik_data = await _fetch_cik_json(
        "/api/elections/candidates",
        {"fio": fio, "year": god, "region": region},
    )
    if isinstance(cik_data, list):
        results = []
        for item in cik_data:
            if not isinstance(item, dict):
                continue
            results.append(
                KandidatKratko(
                    identifikator=str(item.get("id", "")),
                    fio=str(item.get("fio", item.get("name", ""))),
                    partia=str(item.get("party", item.get("partia", ""))),
                    dolzhnost=str(item.get("position", item.get("dolzhnost", ""))),
                    region=str(item.get("region", "")),
                    status=str(item.get("status", "")),
                )
            )
        return results

    return []


async def kandidat_podrobno(
    kandidat_id: str,
    god: int | None = None,
) -> Kandidat | None:
    """Получить подробную информацию о кандидате из ГАС «Выборы».

    Аргументы:
        kandidat_id: ID кандидата или ФИО.
        god: Год выборов (необязательно).

    Возвращает:
        Подробная информация о кандидате или None.
    """
    cik_data = await _fetch_cik_json(
        f"/api/elections/candidates/{kandidat_id}",
        {"year": god},
    )
    if isinstance(cik_data, dict):
        return Kandidat(
            identifikator=str(cik_data.get("id", kandidat_id)),
            fio=str(cik_data.get("fio", cik_data.get("name", ""))),
            data_rozhdeniya=str(cik_data.get("birthDate", cik_data.get("data_rozhdeniya", ""))),
            mesto_rozhdeniya=str(cik_data.get("birthPlace", cik_data.get("mesto_rozhdeniya", ""))),
            partia=str(cik_data.get("party", cik_data.get("partia", ""))),
            dolzhnost=str(cik_data.get("position", cik_data.get("dolzhnost", ""))),
            region=str(cik_data.get("region", "")),
            status=str(cik_data.get("status", "")),
            obrazovanie=str(cik_data.get("education", cik_data.get("obrazovanie", ""))),
            mesto_raboty=str(cik_data.get("workPlace", cik_data.get("mesto_raboty", ""))),
            dolzhnost_rabota=str(
                cik_data.get("workPosition", cik_data.get("dolzhnost_rabota", ""))
            ),
            dokhod=str(cik_data.get("income", cik_data.get("dokhod", ""))),
            scheta=str(cik_data.get("bankAccounts", cik_data.get("scheta", ""))),
            nedvizhimost=str(cik_data.get("realEstate", cik_data.get("nedvizhimost", ""))),
            transport=str(cik_data.get("vehicles", cik_data.get("transport", ""))),
        )

    vybory_info = None
    if god is not None:
        for v in IZVESTNYE_VYBORY.values():
            if v["god"] == god:
                vybory_info = v
                break

    if vybory_info:
        html = await _fetch_vybory_html(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            region=0,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html:
            kandidaty = _parse_candidates_from_html(html)
            for k in kandidaty:
                if k.identifikator == kandidat_id or kandidat_id.lower() in k.fio.lower():
                    return Kandidat(
                        identifikator=k.identifikator,
                        fio=k.fio,
                        partia=k.partia,
                        dolzhnost=k.dolzhnost,
                        region=k.region,
                        status=k.status,
                    )

    return None


async def rezultaty_vyborov(
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> list[ResultatKandidata]:
    """Получить результаты выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Возвращает:
        Список результатов кандидатов.
    """
    vybory_info = _find_vybory_by_god_tip(god, tip)

    if vybory_info:
        region_num = 0
        if region and region in IZBIRATELNYY_KOD_REGIONA:
            region_num = IZBIRATELNYY_KOD_REGIONA[region]

        html = await _fetch_vybory_html(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            region=region_num,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html:
            results = _parse_results_from_html(html)
            if results:
                return results

    cik_data = await _fetch_cik_json(
        "/api/elections/results",
        {"year": god, "type": tip, "region": region},
    )
    if isinstance(cik_data, dict):
        items = cik_data.get("results", cik_data.get("candidates", []))
        if isinstance(items, list):
            results = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                results.append(
                    ResultatKandidata(
                        kandidat_id=str(item.get("id", "")),
                        fio=str(item.get("fio", item.get("name", ""))),
                        partia=str(item.get("party", item.get("partia", ""))),
                        golosov=int(str(item.get("votes", item.get("golosov", 0)))),
                        procent=float(str(item.get("percent", item.get("procent", 0.0)))),
                        izbrann=bool(item.get("elected", item.get("izbrann", False))),
                    )
                )
            return results

    return []


async def yavka_i_itogi(
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> dict[str, Any]:
    """Получить данные о явке и итогах выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Возвращает:
        Словарь с итогами выборов.
    """
    vybory_info = _find_vybory_by_god_tip(god, tip)

    if vybory_info:
        region_num = 0
        if region and region in IZBIRATELNYY_KOD_REGIONA:
            region_num = IZBIRATELNYY_KOD_REGIONA[region]

        html = await _fetch_vybory_html(
            tvd=str(vybory_info["tvd"]),
            vrn=str(vybory_info["vrn"]),
            region=region_num,
            tip_golosovaniya=int(str(vybory_info.get("tip", 242))),
        )
        if html:
            turnout = _parse_turnout_from_html(html)
            if turnout["vseh_izbirateley"] > 0 or turnout["yavka_procent"] > 0:
                return {
                    "god": god,
                    "tip": tip,
                    "region": region,
                    "name": str(vybory_info["nazvanie"]),
                    "data": str(vybory_info["data"]),
                    **turnout,
                    "istochnik": f"ГАС «Выборы» ({VYBORY_API_BASE})",
                }

    cik_data = await _fetch_cik_json(
        "/api/elections/turnout",
        {"year": god, "type": tip, "region": region},
    )
    if isinstance(cik_data, dict):
        return {
            "god": god,
            "tip": tip,
            "region": region,
            "name": cik_data.get("name", ""),
            "data": cik_data.get("date", ""),
            "yavka_procent": cik_data.get("turnout", cik_data.get("yavka_procent", 0.0)),
            "vseh_izbirateley": cik_data.get("totalVoters", cik_data.get("vseh_izbirateley", 0)),
            "progalosovalo": cik_data.get("voted", cik_data.get("progalosovalo", 0)),
            "deystvitelnykh_byulleteney": cik_data.get("validBallots", 0),
            "nedeystvitelnykh_byulleteney": cik_data.get("invalidBallots", 0),
            "istochnik": f"ЦИК РФ ({CIK_API_BASE})",
        }

    return {
        "god": god,
        "tip": tip,
        "region": region,
        "name": "",
        "data": "",
        "yavka_procent": 0.0,
        "vseh_izbirateley": 0,
        "progalosovalo": 0,
        "deystvitelnykh_byulleteney": 0,
        "nedeystvitelnykh_byulleteney": 0,
        "istochnik": f"ЦИК РФ / ГАС «Выборы» ({CIK_API_BASE}, {VYBORY_API_BASE})",
    }
