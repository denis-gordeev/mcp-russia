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

from .constants import KATEGORII_ZEMEL_MAP, STATUSY_UCHE_TA_MAP
from .schemas import KadastrovayaStoimost, KadastrovyyObekt

PKK_API_BASE = "https://pkk.rosreestr.ru/api/features"
PKK_SEARCH_URL = "https://pkk.rosreestr.ru/api/features/1"

TIPY_OBEKTA_CODE = {
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
    tip_code = TIPY_OBEKTA_CODE.get(tip, "")

    adres = ""
    if dannye.get("address"):
        addr = dannye["address"]
        adres = addr.get("note", "") or addr.get("formatted", "") or str(addr)

    ploshchad = ""
    if dannye.get("area"):
        dannye_ploshchadi = dannye["area"]
        if isinstance(dannye_ploshchadi, dict):
            ploshchad = str(dannye_ploshchadi.get("value", ""))
        else:
            ploshchad = str(dannye_ploshchadi)

    stoimost = ""
    if dannye.get("cad_cost"):
        stoimost = str(dannye["cad_cost"])
    elif dannye.get("cadastral_cost"):
        stoimost_slovar = dannye["cadastral_cost"]
        stoimost = (
            str(stoimost_slovar.get("value", ""))
            if isinstance(stoimost_slovar, dict)
            else str(stoimost_slovar)
        )

    data_stoimosti = ""
    if dannye.get("cad_record_date"):
        data_stoimosti = str(dannye["cad_record_date"])
    elif dannye.get("date_cad_cost"):
        data_stoimosti = str(dannye["date_cad_cost"])

    status_ucheta = ""
    if dannye.get("state"):
        st = dannye["state"]
        if isinstance(st, dict):
            status_ucheta = STATUSY_UCHE_TA_MAP.get(st.get("code", ""), st.get("name", ""))
        else:
            status_ucheta = str(st)

    kategoriya = ""
    if dannye.get("category"):
        kategoriya_slovar = dannye["category"]
        if isinstance(kategoriya_slovar, dict):
            kategoriya = KATEGORII_ZEMEL_MAP.get(
                kategoriya_slovar.get("code", ""), kategoriya_slovar.get("name", "")
            )
        else:
            kategoriya = str(kategoriya_slovar)

    return KadastrovyyObekt(
        kadastrovyy_nomer=kadastrovyy_nomer,
        tip_obekta=tip_code,
        adreshnye_svedeniya=adres,
        ploshchad=ploshchad,
        kadastrovaya_stoimost=stoimost,
        data_opredeleniya_stoimosti=data_stoimosti,
        status_ucheta=status_ucheta,
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
        adres_url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        attrs = obekt_dannykh.get("attrs", obekt_dannykh)
        return _razobrat_obekt(kadastrovyy_nomer, attrs)
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
        adres_url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        attrs = obekt_dannykh.get("attrs", obekt_dannykh)

        stoimost = None
        if attrs.get("cad_cost"):
            with contextlib.suppress(ValueError, TypeError):
                stoimost = float(attrs["cad_cost"])
        elif attrs.get("cadastral_cost"):
            stoimost_slovar = attrs["cadastral_cost"]
            if isinstance(stoimost_slovar, dict):
                with contextlib.suppress(ValueError, TypeError):
                    stoimost = float(stoimost_slovar.get("value", 0))

        data_opr = ""
        if attrs.get("cad_record_date"):
            data_opr = str(attrs["cad_record_date"])
        elif attrs.get("date_cad_cost"):
            data_opr = str(attrs["date_cad_cost"])

        data_vneseniya = ""
        if attrs.get("date_created"):
            data_vneseniya = str(attrs["date_created"])

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
        adres_url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        rezultat = await http_poluchit(adres_url, zagolovki={"Accept": "application/json"})
        obekt_dannykh = rezultat.get("feature", rezultat)
        prava_spisok = obekt_dannykh.get("rights", [])
        if not prava_spisok:
            return []

        razobrannye = []
        for r in prava_spisok:
            razobrannye.append(
                {
                    "tip_prava": r.get("type", "") or r.get("name", ""),
                    "sobstvennik": r.get("owner", ""),
                    "data_registratsii": r.get("reg_date", ""),
                    "nomer_registratsii": r.get("reg_number", ""),
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
        adres_url = f"{PKK_SEARCH_URL}"
        rezultat = await http_poluchit(
            adres_url,
            parametry={"sqo": zapros},
            zagolovki={"Accept": "application/json"},
        )
        obekty_spisok = rezultat.get("features", [])
        if not obekty_spisok:
            return []

        naydennye = []
        for f in obekty_spisok[:10]:
            attrs = f.get("attrs", {})
            naydennye.append(
                {
                    "kadastrovyy_nomer": attrs.get("cn", ""),
                    "tip": attrs.get("type", ""),
                    "adres": attrs.get("address", {}).get("note", "")
                    if isinstance(attrs.get("address"), dict)
                    else "",
                    "sostoyanie": attrs.get("state", {}).get("name", "")
                    if isinstance(attrs.get("state"), dict)
                    else "",
                }
            )
        return naydennye
    except Exception:
        return []
