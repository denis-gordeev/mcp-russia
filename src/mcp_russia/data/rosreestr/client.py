"""HTTP client for the Росреестр feature.

Provides access to Russian real estate data via pkk.rosreestr.ru:
- Object search by cadastral number
- Object details (type, area, address, cadastral value)
- Cadastral value information

pkk.rosreestr.ru is a public service that provides JSON API endpoints.
No API key required.
"""

from __future__ import annotations

import contextlib
from typing import Any

from mcp_russia._shared.http_client import http_get

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


def _parse_obekt(kadastrovyy_nomer: str, data: dict[str, Any]) -> KadastrovyyObekt:
    tip = data.get("type", "").lower()
    tip_code = TIPY_OBEKTA_CODE.get(tip, "")

    adres = ""
    if data.get("address"):
        addr = data["address"]
        adres = addr.get("note", "") or addr.get("formatted", "") or str(addr)

    ploshchad = ""
    if data.get("area"):
        area_data = data["area"]
        if isinstance(area_data, dict):
            ploshchad = str(area_data.get("value", ""))
        else:
            ploshchad = str(area_data)

    stoimost = ""
    if data.get("cad_cost"):
        stoimost = str(data["cad_cost"])
    elif data.get("cadastral_cost"):
        cost = data["cadastral_cost"]
        stoimost = str(cost.get("value", "")) if isinstance(cost, dict) else str(cost)

    data_stoimosti = ""
    if data.get("cad_record_date"):
        data_stoimosti = str(data["cad_record_date"])
    elif data.get("date_cad_cost"):
        data_stoimosti = str(data["date_cad_cost"])

    status = ""
    if data.get("state"):
        st = data["state"]
        if isinstance(st, dict):
            status = STATUSY_UCHE_TA_MAP.get(st.get("code", ""), st.get("name", ""))
        else:
            status = str(st)

    kategoriya = ""
    if data.get("category"):
        cat = data["category"]
        if isinstance(cat, dict):
            kategoriya = KATEGORII_ZEMEL_MAP.get(cat.get("code", ""), cat.get("name", ""))
        else:
            kategoriya = str(cat)

    return KadastrovyyObekt(
        kadastrovyy_nomer=kadastrovyy_nomer,
        tip_obekta=tip_code,
        adreshnye_svedeniya=adres,
        ploshchad=ploshchad,
        kadastrovaya_stoimost=stoimost,
        data_opredeleniya_stoimosti=data_stoimosti,
        status_ucheta=status,
        kategoriya_zemel=kategoriya,
    )


async def poluchit_obekt(kadastrovyy_nomer: str) -> KadastrovyyObekt | None:
    try:
        url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        result = await http_get(url, headers={"Accept": "application/json"})
        feature = result.get("feature", result)
        attrs = feature.get("attrs", feature)
        return _parse_obekt(kadastrovyy_nomer, attrs)
    except Exception:
        return None


async def poluchit_kadastrovnuyu_stoimost(kadastrovyy_nomer: str) -> KadastrovayaStoimost | None:
    try:
        url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        result = await http_get(url, headers={"Accept": "application/json"})
        feature = result.get("feature", result)
        attrs = feature.get("attrs", feature)

        stoimost = None
        if attrs.get("cad_cost"):
            with contextlib.suppress(ValueError, TypeError):
                stoimost = float(attrs["cad_cost"])
        elif attrs.get("cadastral_cost"):
            cost = attrs["cadastral_cost"]
            if isinstance(cost, dict):
                with contextlib.suppress(ValueError, TypeError):
                    stoimost = float(cost.get("value", 0))

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
    try:
        url = f"{PKK_API_BASE}/1/{kadastrovyy_nomer}"
        result = await http_get(url, headers={"Accept": "application/json"})
        feature = result.get("feature", result)
        rights = feature.get("rights", [])
        if not rights:
            return []

        parsed = []
        for r in rights:
            parsed.append(
                {
                    "tip_prava": r.get("type", "") or r.get("name", ""),
                    "sobstvennik": r.get("owner", ""),
                    "data_registratsii": r.get("reg_date", ""),
                    "nomer_registratsii": r.get("reg_number", ""),
                }
            )
        return parsed
    except Exception:
        return []


async def poisk_po_nomeru(zapros: str) -> list[dict[str, Any]]:
    try:
        url = f"{PKK_SEARCH_URL}"
        result = await http_get(
            url,
            params={"sqo": zapros},
            headers={"Accept": "application/json"},
        )
        features = result.get("features", [])
        if not features:
            return []

        found = []
        for f in features[:10]:
            attrs = f.get("attrs", {})
            found.append(
                {
                    "kadastrovyy_nomer": attrs.get("cn", ""),
                    "tip": attrs.get("type", ""),
                    "adres": attrs.get("address", {}).get("note", "")
                    if isinstance(attrs.get("address"), dict)
                    else "",
                    "status": attrs.get("state", {}).get("name", "")
                    if isinstance(attrs.get("state"), dict)
                    else "",
                }
            )
        return found
    except Exception:
        return []
