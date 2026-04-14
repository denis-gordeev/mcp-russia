"""HTTP client for the Росводресурсы data sources.

Federal Agency for Water Resources manages water bodies, hydrological monitoring,
and water usage data in Russia.

This module provides placeholder client functions for future API integration.
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    BASSEYNOVYE_OKRUGA,
    KRUPNYE_VODOKHRANILISHCHA,
    ROSVODRESURSY_API_BASE,
    TIPY_GIDRO_DANNYKH,
    TIPY_VODNYKH_OBIEKTOV,
)
from .schemas import (
    GidroData,
    VodnyyObekt,
    VodokhranilishcheData,
    Vodopolzovanie,
)


async def buscar_vodnyy_obekt(code: str) -> VodnyyObekt | None:
    """Fetch a water body by code.

    Args:
        code: Water body code from the State Water Registry.

    Returns:
        Water body data or None.
    """
    url = f"{ROSVODRESURSY_API_BASE}/vodnyy_obekt/{code}"
    try:
        data = await http_get(url)
        return _parse_vodnyy_obekt(data)
    except Exception:
        return None


async def buscar_gidro_post(post: str) -> GidroData | None:
    """Fetch hydrological data from a monitoring post.

    Args:
        post: Hydrological post code.

    Returns:
        Hydrological data or None.
    """
    url = f"{ROSVODRESURSY_API_BASE}/gidro/{post}"
    try:
        data = await http_get(url)
        return _parse_gidro(data)
    except Exception:
        return None


async def buscar_vodokhranilishche(code: str) -> VodokhranilishcheData | None:
    """Fetch reservoir data by code.

    Args:
        code: Reservoir code.

    Returns:
        Reservoir data or None.
    """
    url = f"{ROSVODRESURSY_API_BASE}/vodokhranilishche/{code}"
    try:
        data = await http_get(url)
        return _parse_vodokhranilishche(data)
    except Exception:
        return None


async def buscar_vodopolzovanie(
    region: str = "",
    god: str = "",
) -> list[Vodopolzovanie]:
    """Fetch water usage data by region and year.

    Args:
        region: Region filter.
        god: Year filter.

    Returns:
        List of water usage data.
    """
    url = f"{ROSVODRESURSY_API_BASE}/vodopolzovanie"
    params: dict[str, str] = {}
    if region:
        params["region"] = region
    if god:
        params["god"] = god
    try:
        data = await http_get(url, params=params)
        return _parse_vodopolzovanie(data)
    except Exception:
        return []


def get_basseynovye_okruga_list() -> list[dict[str, str]]:
    """Get list of basin districts."""
    return BASSEYNOVYE_OKRUGA


def get_tipy_vodnykh_obektov_list() -> list[dict[str, str]]:
    """Get list of water body types."""
    return TIPY_VODNYKH_OBIEKTOV


def get_tipy_gidro_list() -> list[dict[str, str]]:
    """Get list of hydrological data types."""
    return TIPY_GIDRO_DANNYKH


def get_vodokhranilishcha_list() -> list[dict[str, str]]:
    """Get list of major reservoirs."""
    return KRUPNYE_VODOKHRANILISHCHA


# --- Response parsers ---


def _parse_vodnyy_obekt(data: Any) -> VodnyyObekt | None:
    """Parse API response into VodnyyObekt."""
    if not isinstance(data, dict):
        return None
    return VodnyyObekt(
        code=data.get("code", ""),
        name=data.get("name", ""),
        tip=data.get("tip", ""),
        basseyn=data.get("basseyn", ""),
        dlinna_km=data.get("dlinna_km"),
        ploshchad_km2=data.get("ploshchad_km2"),
        region=data.get("region", ""),
        opisaniye=data.get("opisaniye", ""),
    )


def _parse_gidro(data: Any) -> GidroData | None:
    """Parse API response into GidroData."""
    if not isinstance(data, dict):
        return None
    return GidroData(
        post=data.get("post", ""),
        vodnyy_obekt=data.get("vodnyy_obekt", ""),
        data_izmereniya=data.get("data_izmereniya", ""),
        uroven=data.get("uroven"),
        raskhod=data.get("raskhod"),
        temperatura=data.get("temperatura"),
        ledovaya_obstanovka=data.get("ledovaya_obstanovka", ""),
        preduprezhdenie=data.get("preduprezhdenie", ""),
    )


def _parse_vodokhranilishche(data: Any) -> VodokhranilishcheData | None:
    """Parse API response into VodokhranilishcheData."""
    if not isinstance(data, dict):
        return None
    return VodokhranilishcheData(
        code=data.get("code", ""),
        name=data.get("name", ""),
        region=data.get("region", ""),
        obiem_km3=data.get("obiem_km3"),
        ploshchad_km2=data.get("ploshchad_km2"),
        uroven_m=data.get("uroven_m"),
        priznak_napolneniya=data.get("priznak_napolneniya", ""),
        data_izmereniya=data.get("data_izmereniya", ""),
    )


def _parse_vodopolzovanie(data: Any) -> list[Vodopolzovanie]:
    """Parse API response into list of Vodopolzovanie."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            Vodopolzovanie(
                region=item.get("region", ""),
                god=item.get("god", ""),
                zabrano_vody_km3=item.get("zabrano_vody_km3"),
                ispolzovano_vody_km3=item.get("ispolzovano_vody_km3"),
                sbrosheno_stokov_km3=item.get("sbrosheno_stokov_km3"),
                istochnik=item.get("istochnik", ""),
                naznachenie=item.get("naznachenie", ""),
            )
        )
    return results
