"""HTTP client for Rosstat / EMISS data sources.

Real API integration with:
    - ЕМИСС (fedstat.ru) for statistical indicators
    - Росстат (rosstat.gov.ru) for published data
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    EMISS_API_BASE,
    EMISS_KODY_POKAZATELEY,
    FEDERALNYE_OKRUGA,
    SUBIEKTY_RF,
)
from .schemas import PokazatelRosstata, RegionData

logger = logging.getLogger(__name__)


async def poluchit_indikator(code: str, date_range: str = "") -> list[PokazatelRosstata]:
    """Fetch a statistical indicator from EMISS/Rosstat.

    Args:
        code: Indicator code (e.g. 'cpi', 'population').
        date_range: Date range filter (optional).

    Returns:
        List of indicator values.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get(code, code)
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if date_range:
            params["date"] = date_range
        data = await http_get(url, params=params, timeout=20.0)
        return _parse_indikator_response(data, code)
    except Exception:
        logger.exception("Ошибка при получении индикатора %s", code)
        return []


async def poluchit_dannye_regiona(code: str) -> RegionData | None:
    """Fetch regional data for a Russian federal subject.

    Args:
        code: Region code (OKATO/OKTMO).

    Returns:
        Regional data or None.
    """
    region_info = next((r for r in SUBIEKTY_RF if r["code"] == code), None)
    if not region_info:
        return None
    try:
        url = f"{EMISS_API_BASE}/region/{code}"
        data = await http_get(url, timeout=20.0)
        if isinstance(data, dict):
            return RegionData(
                code=code,
                name=region_info["name"],
                federalny_okrug=region_info.get("okrug", ""),
                population=data.get("population"),
                vrp=data.get("gdp") or data.get("vrp"),
                srednyaya_zp=data.get("avgWage") or data.get("srednyaya_zp"),
            )
    except Exception:
        logger.exception("Ошибка при получении данных региона %s", code)

    return RegionData(
        code=code,
        name=region_info["name"],
        federalny_okrug=region_info.get("okrug", ""),
    )


async def poluchit_federalny_okrug(code: str) -> dict[str, Any]:
    """Fetch data for a federal district.

    Args:
        code: Federal district code.

    Returns:
        Federal district data.
    """
    okrug_info = next((o for o in FEDERALNYE_OKRUGA if o["code"] == code), None)
    if not okrug_info:
        return {"error": f"Федеральный округ '{code}' не найден"}

    regiony = [r for r in SUBIEKTY_RF if r.get("okrug") == code]
    return {
        "code": code,
        "name": okrug_info["name"],
        "kolichestvo_subiektov": len(regiony),
        "subiekty": [r["name"] for r in regiony],
    }


async def poluchit_inflyaciyu(god: str = "") -> list[dict[str, Any]]:
    """Fetch inflation (CPI) data from EMISS.

    Args:
        god: Year filter.

    Returns:
        List of CPI data points.
    """
    try:
        emiss_code = EMISS_KODY_POKAZATELEY.get("cpi", "31088")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            items = data.get("data", [])
            if isinstance(items, list):
                return [
                    {
                        "period": item.get("date", item.get("period", "")),
                        "ipcz_mesyac": item.get("monthlyRate") or item.get("value"),
                        "ipcz_nakoplenny": item.get("cumulativeRate"),
                        "ipcz_god": item.get("yearlyRate"),
                    }
                    for item in items
                    if isinstance(item, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении данных об инфляции")
        return []


async def poluchit_demografiyu(region: str = "") -> list[dict[str, Any]]:
    """Fetch demographic data from EMISS.

    Args:
        region: Region code (optional).

    Returns:
        List of demographic data points.
    """
    try:
        emiss_code = EMISS_KODY_POKAZATELEY.get("population", "24133")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            items = data.get("data", [])
            if isinstance(items, list):
                return [
                    {
                        "period": item.get("date", item.get("period", "")),
                        "naselenie": item.get("population") or item.get("value"),
                        "rozhdaemost": item.get("birthRate"),
                        "smertnost": item.get("deathRate"),
                        "estestvenny_prirost": item.get("naturalGrowth"),
                    }
                    for item in items
                    if isinstance(item, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении демографических данных")
        return []


def _parse_indikator_response(data: Any, code: str) -> list[PokazatelRosstata]:
    """Parse EMISS API response into PokazatelRosstata objects."""
    if not isinstance(data, dict):
        return []

    items = data.get("data", [])
    if not isinstance(items, list):
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            results.append(
                PokazatelRosstata(
                    code=code,
                    name=item.get("name", code),
                    value=float(item.get("value", 0)),
                    unit=item.get("unit", ""),
                    date=item.get("date", ""),
                )
            )
        except (ValueError, TypeError):
            continue
    return results


def get_subiekty_list() -> list[dict[str, str]]:
    """Get list of Russian federal subjects available for queries."""
    return SUBIEKTY_RF


def get_federalny_okruga_list() -> list[dict[str, str]]:
    """Get list of federal districts available for queries."""
    return FEDERALNYE_OKRUGA
