"""HTTP client for Rosstat / EMISS data sources.

Rosstat does not provide a single unified public REST API.
This module uses available data sources:
    - EMISS (fedstat.ru) for statistical indicators
    - Direct data parsing where possible
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import EMISS_API_BASE, FEDERALNYE_OKRUGA, SUBIEKTY_RF
from .schemas import PokazatelRosstata, RegionData


async def buscar_indikator(code: str, date_range: str = "") -> list[PokazatelRosstata]:
    """Fetch a statistical indicator from EMISS/Rosstat.

    Args:
        code: Indicator code.
        date_range: Date range filter (optional).

    Returns:
        List of indicator values.
    """
    # EMISS API structure varies; this is a placeholder for the pattern
    url = f"{EMISS_API_BASE}/data/{code}"
    params: dict[str, str] = {}
    if date_range:
        params["date"] = date_range

    try:
        data = await http_get(url, params=params)
        return _parse_indikator_response(data, code)
    except Exception:
        return []


def _parse_indikator_response(data: Any, code: str) -> list[PokazatelRosstata]:
    """Parse EMISS API response into PokazatelRosstata objects."""
    if not isinstance(data, dict):
        return []

    results = []
    for item in data.get("data", []):
        results.append(
            PokazatelRosstata(
                code=code,
                name=item.get("name", code),
                value=float(item.get("value", 0)),
                unit=item.get("unit", ""),
                date=item.get("date", ""),
            )
        )
    return results


async def buscar_region_data(code: str) -> RegionData | None:
    """Fetch regional data for a Russian federal subject.

    Args:
        code: Region code (OKATO).

    Returns:
        Regional data or None.
    """
    # Placeholder — real implementation would query EMISS regional endpoints
    region_info = next((r for r in SUBIEKTY_RF if r["code"] == code), None)
    if not region_info:
        return None

    return RegionData(
        code=code,
        name=region_info["name"],
    )


async def buscar_federalny_okrug(code: str) -> dict[str, Any]:
    """Fetch data for a federal district.

    Args:
        code: Federal district code.

    Returns:
        Federal district data.
    """
    okrug_info = next((o for o in FEDERALNYE_OKRUGA if o["code"] == code), None)
    if not okrug_info:
        return {"error": f"Федеральный округ '{code}' не найден"}

    return {
        "code": code,
        "name": okrug_info["name"],
        "note": "Данные по федеральным округам доступны через ЕМИСС (fedstat.ru)",
    }


def get_subiekty_list() -> list[dict[str, str]]:
    """Get list of Russian federal subjects available for queries."""
    return SUBIEKTY_RF


def get_federalny_okruga_list() -> list[dict[str, str]]:
    """Get list of federal districts available for queries."""
    return FEDERALNYE_OKRUGA
