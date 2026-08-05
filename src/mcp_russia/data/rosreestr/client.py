"""HTTP-клиент для модуля Росреестра.

Обеспечивает доступ к данным о недвижимости через pkk.rosreestr.ru:
- Поиск объектов по кадастровому номеру
- Детали объекта (тип, площадь, адрес, кадастровая стоимость)
- Информация о кадастровой стоимости

pkk.rosreestr.ru — публичный сервис с JSON API эндпоинтами.
API-ключ не требуется.
"""

from __future__ import annotations

import contextlib
from typing import Any

from mcp_russia._shared.http_client import http_poluchit
from mcp_russia._shared.normalizatsiya import bezopasnaya_stroka, pervoe_znachenie

from .constants import KATEGORII_ZEMEL_SLOVAR, STATUSY_UCHE_TA_SLOVAR
from .schemas import KadastrovayaStoimost, KadastrovyyObekt

PKK_BAZA_API = "https://pkk.rosreestr.ru/api/features"
PKK_URL_POISKA = "https://pkk.rosreestr.ru/api/features/1"

TIPY_OBEKTA_KOD = {
    "земельный участок": "zemelnyy_uchastok",
    "здание": "zdanie",
    "помещение": "pomeshchenie",
    "сооружение": "sooruzhenie",
    "объект незавершённого строительства": "obekt_nedostroenny",
    "многоквартирный дом": "mnogokvartirnyy_dom",
}


def _razobrat_obekt(kadastrovyy_nomer: str, dannye: dict[str, Any]) -> KadastrovyyObekt:
    """Разбор данных объекта недвижимости из ответа pkk.rosreestr.ru."""
    tip = dannye.get("type", "").lower()
    kod_tipa = TIPY_OBEKTA_KOD.get(tip, "")

    adres = ""
    if dannye.get("address"):
        adres_dannye = dannye["address"]
        adres = bezopasnaya_stroka(adres_dannye.get("note")) or bezopasnaya_stroka(
            adres_dannye.get("formatted")
        )

    ploshchad = ""
    if dannye.get("area"):
        dannye_ploshchadi = dannye["area"]
        if isinstance(dannye_ploshchadi, dict):
            ploshchad = bezopasnaya_stroka(dannye_ploshchadi.get("value"))
        else:
            ploshchad = bezopasnaya_stroka(dannye_ploshchadi)

    stoimost = ""
    if dannye.get("cad_cost"):
        stoimost = bezopasnaya_stroka(dannye["cad_cost"])
    elif dannye.get("cadastral_cost"):
        stoimost_slovar = dannye["cadastral_cost"]
        stoimost = (
            bezopasnaya_stroka(stoimost_slovar.get("value"))
            if isinstance(stoimost_slovar, dict)
            else bezopasnaya_stroka(stoimost_slovar)
        )

    data_stoimosti = ""
    if dannye.get("cad_record_date"):
        data_stoimosti = bezopasnaya_stroka(dannye["cad_record_date"])
    elif dannye.get("date_cad_cost"):
        data_stoimosti = bezopasnaya_stroka(dannye["date_cad_cost"])

    sostoyanie_ucheta = ""
    if dannye.get("state"):
        sostoyanie_dannykh = dannye["state"]
        if isinstance(sostoyanie_dannykh, dict):
            sostoyanie_ucheta = (
                STATUSY_UCHE_TA_SLOVAR.get(
                    bezopasnaya_stroka(sostoyanie_dannykh.get("code")),
                    bezopasnaya_stroka(sostoyanie_dannykh.get("name")),
                )
                or ""
            )
        else:
            sostoyanie_ucheta = bezopasnaya_stroka(sostoyanie_dannykh)

    kategoriya = ""
    if dannye.get("category"):
        kategoriya_slovar = dannye["category"]
        if isinstance(kategoriya_slovar, dict):
            kategoriya = (
                KATEGORII_ZEMEL_SLOVAR.get(
                    bezopasnaya_stroka(kategoriya_slovar.get("code")),
                    bezopasnaya_stroka(kategoriya_slovar.get("name")),
                )
                or ""
            )
        else:
            kategoriya = bezopasnaya_stroka(kategoriya_slovar)

    return KadastrovyyObekt(
        kadastrovyy_nomer=kadastrovyy_nomer,
        tip_obekta=kod_tipa,
        adreshnye_svedeniya=adres,
        ploshchad=ploshchad,
        kadastrovaya_stoimost=stoimost,
        data_opredeleniya_stoimosti=data_stoimosti,
        sostoyanie_ucheta=sostoyanie_ucheta,
        kategoriya_zemel=kategoriya,
    )


async def poluchit_obekt(kadastrovyy_nomer: str) -> KadastrovyyObekt | None:
    """Получить информацию об объекте недвижимости по кадастровому номеру.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Возвращает:
        Данные объекта или None.
    """
    try:
        adres_url = f"{PKK_BAZA_API}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        atributy = obekt_dannykh.get("attrs", obekt_dannykh)
        return _razobrat_obekt(kadastrovyy_nomer, atributy)
    except Exception:
        return None


async def poluchit_kadastrovnuyu_stoimost(kadastrovyy_nomer: str) -> KadastrovayaStoimost | None:
    """Получить кадастровую стоимость объекта по кадастровому номеру.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Возвращает:
        Данные о кадастровой стоимости или None.
    """
    try:
        adres_url = f"{PKK_BAZA_API}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        atributy = obekt_dannykh.get("attrs", obekt_dannykh)

        stoimost = None
        if atributy.get("cad_cost"):
            with contextlib.suppress(ValueError, TypeError):
                stoimost = float(atributy["cad_cost"])
        elif atributy.get("cadastral_cost"):
            stoimost_slovar = atributy["cadastral_cost"]
            if isinstance(stoimost_slovar, dict):
                with contextlib.suppress(ValueError, TypeError):
                    stoimost = float(stoimost_slovar.get("value", 0))

        data_opr = ""
        if atributy.get("cad_record_date"):
            data_opr = bezopasnaya_stroka(atributy["cad_record_date"])
        elif atributy.get("date_cad_cost"):
            data_opr = bezopasnaya_stroka(atributy["date_cad_cost"])

        data_vneseniya = ""
        if atributy.get("date_created"):
            data_vneseniya = bezopasnaya_stroka(atributy["date_created"])

        return KadastrovayaStoimost(
            kadastrovyy_nomer=kadastrovyy_nomer,
            stoimost=stoimost,
            data_opredeleniya=data_opr,
            data_vneseniya_v_egrn=data_vneseniya,
            osnovanie="Определена в порядке массовой оценки",
        )
    except Exception:
        return None


async def poluchit_prava(kadastrovyy_nomer: str) -> list[dict[str, Any]]:
    """Получить информацию о правах на объект недвижимости.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Возвращает:
        Список зарегистрированных прав.
    """
    try:
        adres_url = f"{PKK_BAZA_API}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        prava_spisok = obekt_dannykh.get("rights", [])
        if not prava_spisok:
            return []

        razobrannye = []
        for pravo in prava_spisok:
            razobrannye.append(
                {
                    "tip_prava": bezopasnaya_stroka(pervoe_znachenie(pravo, "type", "name")),
                    "sobstvennik": pravo.get("owner", ""),
                    "data_registratsii": pravo.get("reg_date", ""),
                    "nomer_registratsii": pravo.get("reg_number", ""),
                }
            )
        return razobrannye
    except Exception:
        return []


async def poisk_po_nomeru(zapros: str) -> list[dict[str, Any]]:
    """Поиск объектов недвижимости по запросу через pkk.rosreestr.ru.

    Аргументы:
        zapros: Поисковый запрос (кадастровый номер или адрес).

    Возвращает:
        Список найденных объектов.
    """
    try:
        adres_url = f"{PKK_URL_POISKA}"
        rezultat = await http_poluchit(
            adres_url,
            parametry={"sqo": zapros},
            zagolovki={"Accept": "application/json"},
        )
        obekty_spisok = rezultat.get("features", [])
        if not obekty_spisok:
            return []

        naydennye = []
        for obekt in obekty_spisok[:10]:
            atributy = obekt.get("attrs", {})
            naydennye.append(
                {
                    "kadastrovyy_nomer": atributy.get("cn", ""),
                    "tip": atributy.get("type", ""),
                    "adres": atributy.get("address", {}).get("note", "")
                    if isinstance(atributy.get("address"), dict)
                    else "",
                    "sostoyanie": atributy.get("state", {}).get("name", "")
                    if isinstance(atributy.get("state"), dict)
                    else "",
                }
            )
        return naydennye
    except Exception:
        return []
