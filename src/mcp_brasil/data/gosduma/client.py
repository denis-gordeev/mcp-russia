"""HTTP client for the Gosduma (State Duma) API.

Endpoints:
    - https://download.data.duma.gov.ru — открытые данные
    - https://sozd.duma.gov.ru — система законопроектной деятельности
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import DUMA_DEPUTATS, FRAKCII, SOZYVY
from .schemas import Deputat, Frakciya, Zakonoproekt


async def buscar_deputats(sozyv: str = "") -> list[Deputat]:
    """Fetch list of State Duma deputies.

    Args:
        sozyv: Convocation number (e.g., '8' for VIII созыв).

    Returns:
        List of deputies.
    """
    # The actual Duma API structure may vary
    url = f"{DUMA_DEPUTATS}"
    params: dict[str, str] = {}
    if sozyv:
        params["sozyv"] = sozyv

    try:
        data = await http_get(url, params=params)
        return _parse_deputats(data)
    except Exception:
        return []


def _parse_deputats(data: Any) -> list[Deputat]:
    """Parse deputies from API response."""
    if not isinstance(data, list):
        return []
    return [
        Deputat(
            id=d.get("id", 0),
            фамилия=d.get("familia", ""),
            имя=d.get("imya", ""),
            отчество=d.get("otchestvo", ""),
            фракция=d.get("frakciya", ""),
            комитет=d.get("komitet", ""),
            регион=d.get("region", ""),
            созыв=d.get("sozyv", ""),
            foto_url=d.get("foto", ""),
        )
        for d in data
    ]


async def buscar_deputat(id: int) -> Deputat | None:
    """Fetch a specific deputy by ID.

    Args:
        id: Deputy ID.

    Returns:
        Deputy data or None.
    """
    deputats = await buscar_deputats()
    for d in deputats:
        if d.id == id:
            return d
    return None


async def buscar_zakonoproekty(status: str = "", limit: int = 20) -> list[Zakonoproekt]:
    """Fetch legislative bills.

    Args:
        status: Filter by status (optional).
        limit: Maximum number of results.

    Returns:
        List of bills.
    """
    # Placeholder — SOZD API integration
    return []


async def buscar_frakcii() -> list[Frakciya]:
    """Fetch current Duma factions.

    Returns:
        List of factions.
    """
    return [
        Frakciya(code=f["code"], name=f["name"])
        for f in FRAKCII
    ]


def get_sozyvy() -> list[dict[str, str]]:
    """Get list of State Duma convocations."""
    return SOZYVY


def get_frakcii() -> list[dict[str, str]]:
    """Get list of current factions."""
    return FRAKCII


def get_komitety() -> list[dict[str, str]]:
    """Get list of Duma committees."""
    from .constants import KOMITETY
    return KOMITETY
