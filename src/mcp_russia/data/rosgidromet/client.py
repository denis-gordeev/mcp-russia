"""HTTP client for the Росгидромет data sources.

Rosgidromet provides weather, climate, and environmental monitoring data.
This module provides placeholder client functions for future API integration.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    ROSGIDROMET_API_BASE,
    STANCII_MONITORINGA,
    TIPY_EKODANNYKH,
    TIPY_METEODANNYKH,
    TIPY_PREDUPREZHDENIY,
)
from .schemas import (
    EkologiyaData,
    PogodaData,
    Preduprezhdenie,
    PrognozData,
    SputnikMonitoring,
)


async def poluchit_pogodu(stanciya: str = "77") -> PogodaData | None:
    """Fetch current weather data for a monitoring station.

    Args:
        stanciya: Station code (default: Moscow).

    Returns:
        Current weather data or None.
    """
    url = f"{ROSGIDROMET_API_BASE}/pogoda/{stanciya}"
    try:
        data = await http_get(url)
        return _parse_pogoda(data)
    except Exception:
        return None


async def poluchit_prognoz(
    stanciya: str = "77",
    dni: int = 3,
) -> list[PrognozData]:
    """Fetch weather forecast for a station.

    Args:
        stanciya: Station code.
        dni: Number of forecast days.

    Returns:
        List of forecast data.
    """
    url = f"{ROSGIDROMET_API_BASE}/prognoz/{stanciya}"
    params = {"dni": str(dni)}
    try:
        data = await http_get(url, params=params)
        return _parse_prognoz(data)
    except Exception:
        return []


async def poluchit_ekologiyu(
    gorod: str = "",
    tip: str = "",
) -> list[EkologiyaData]:
    """Fetch environmental monitoring data.

    Args:
        gorod: City name filter.
        tip: Data type (vozdukh, voda, pochva, radiaciya, shum).

    Returns:
        List of environmental data.
    """
    url = f"{ROSGIDROMET_API_BASE}/ekologiya"
    params: dict[str, str] = {}
    if gorod:
        params["gorod"] = gorod
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _parse_ekologiya(data)
    except Exception:
        return []


async def poluchit_preduprezhdeniya(region: str = "") -> list[Preduprezhdenie]:
    """Fetch active weather warnings for a region.

    Args:
        region: Region code or name.

    Returns:
        List of active warnings.
    """
    url = f"{ROSGIDROMET_API_BASE}/preduprezhdeniya"
    params: dict[str, str] = {}
    if region:
        params["region"] = region
    try:
        data = await http_get(url, params=params)
        return _parse_preduprezhdeniya(data)
    except Exception:
        return []


async def poluchit_sputnik_dannye(
    region: str = "",
    tip: str = "",
) -> list[SputnikMonitoring]:
    """Fetch satellite monitoring data.

    Args:
        region: Region filter.
        tip: Data type (lesa, voda, pozhary, snezhnyy_pokrov).

    Returns:
        List of satellite monitoring data.
    """
    url = f"{ROSGIDROMET_API_BASE}/sputnik"
    params: dict[str, str] = {}
    if region:
        params["region"] = region
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _parse_sputnik(data)
    except Exception:
        return []


def get_stancii_list() -> list[dict[str, str]]:
    """Get list of monitoring stations."""
    return STANCII_MONITORINGA


def get_tipy_meteo_list() -> list[dict[str, str]]:
    """Get list of meteorological data types."""
    return TIPY_METEODANNYKH


def get_tipy_eko_list() -> list[dict[str, str]]:
    """Get list of environmental data types."""
    return TIPY_EKODANNYKH


def get_tipy_preduprezhdeniy_list() -> list[dict[str, str]]:
    """Get list of warning types."""
    return TIPY_PREDUPREZHDENIY


# --- Response parsers ---


def _parse_pogoda(data: Any) -> PogodaData | None:
    """Parse API response into PogodaData."""
    if not isinstance(data, dict):
        return None
    return PogodaData(
        stanciya=data.get("stanciya", ""),
        gorod=data.get("gorod", ""),
        region=data.get("region", ""),
        temperatura=data.get("temperatura"),
        feels_like=data.get("feels_like"),
        vlazhnost=data.get("vlazhnost"),
        davlenie=data.get("davlenie"),
        veter_skorost=data.get("veter_skorost"),
        veter_napravlenie=data.get("veter_napravlenie", ""),
        osadki=data.get("osadki"),
        vidimost=data.get("vidimost"),
        opisaniye=data.get("opisaniye", ""),
        data_vremya=data.get("data_vremya", ""),
    )


def _parse_prognoz(data: Any) -> list[PrognozData]:
    """Parse API response into list of PrognozData."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            PrognozData(
                gorod=item.get("gorod", ""),
                data=item.get("data", ""),
                temperatura_dnem=item.get("temperatura_dnem"),
                temperatura_nochyu=item.get("temperatura_nochyu"),
                osadki_veroyatnost=item.get("osadki_veroyatnost"),
                veter_skorost=item.get("veter_skorost"),
                opisaniye=item.get("opisaniye", ""),
            )
        )
    return results


def _parse_ekologiya(data: Any) -> list[EkologiyaData]:
    """Parse API response into list of EkologiyaData."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            EkologiyaData(
                gorod=item.get("gorod", ""),
                stanciya=item.get("stanciya", ""),
                tip=item.get("tip", ""),
                pokazatel=item.get("pokazatel", ""),
                znachenie=item.get("znachenie"),
                norma_max=item.get("norma_max"),
                norma_min=item.get("norma_min"),
                prevyshenie=item.get("prevyshenie", False),
                data_izmereniya=item.get("data_izmereniya", ""),
            )
        )
    return results


def _parse_preduprezhdeniya(data: Any) -> list[Preduprezhdenie]:
    """Parse API response into list of Preduprezhdenie."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            Preduprezhdenie(
                tip=item.get("tip", ""),
                region=item.get("region", ""),
                gorod=item.get("gorod", ""),
                opisanie=item.get("opisanie", ""),
                data_nachala=item.get("data_nachala", ""),
                data_okonchaniya=item.get("data_okonchaniya", ""),
                uroven_opasnosti=item.get("uroven_opasnosti", ""),
            )
        )
    return results


def _parse_sputnik(data: Any) -> list[SputnikMonitoring]:
    """Parse API response into list of SputnikMonitoring."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            SputnikMonitoring(
                sputnik=item.get("sputnik", ""),
                data_syomki=item.get("data_syomki", ""),
                region=item.get("region", ""),
                tip_dannykh=item.get("tip_dannykh", ""),
                razreshenie=item.get("razreshenie", ""),
                izobrazhenie_url=item.get("izobrazhenie_url", ""),
            )
        )
    return results
