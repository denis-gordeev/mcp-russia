"""HTTP client for the Счётная палата РФ data sources.

The Accounts Chamber of Russia (Счётная палата РФ) publishes audit reports
and budget execution analysis on ach.gov.ru.

This module provides placeholder client functions for future API integration.
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    ACH_API_BASE,
    NAPRAVLENIYA_KONTROLYA,
    SUBIEKTY_AUDITA,
    TIPY_MEROPRIYATIY,
)
from .schemas import (
    AuditorskoeZaklyuchenie,
    ByudzhetIspolnenie,
    KontrolnoeMeropriyatie,
    Narushenie,
)


async def poluchit_kontrolnoe_meropriyatie(nomer: str) -> KontrolnoeMeropriyatie | None:
    """Fetch a specific control measure by number.

    Args:
        nomer: Control measure number/identifier.

    Returns:
        Control measure data or None.
    """
    url = f"{ACH_API_BASE}/kontrol/{nomer}"
    try:
        data = await http_get(url)
        return _parse_kontrolnoe_meropriyatie(data)
    except Exception:
        return None


async def poluchit_auditorskoe_zaklyuchenie(nomer: str) -> AuditorskoeZaklyuchenie | None:
    """Fetch a specific audit conclusion by number.

    Args:
        nomer: Audit conclusion number.

    Returns:
        Audit conclusion data or None.
    """
    url = f"{ACH_API_BASE}/zaklyuchenie/{nomer}"
    try:
        data = await http_get(url)
        return _parse_auditorskoe_zaklyuchenie(data)
    except Exception:
        return None


async def poluchit_byudzhet_ispolnenie(
    period: str = "",
) -> ByudzhetIspolnenie | None:
    """Fetch federal budget execution data for a period.

    Args:
        period: Period (e.g., '2024', '2024-Q1').

    Returns:
        Budget execution data or None.
    """
    url = f"{ACH_API_BASE}/byudzhet"
    params: dict[str, str] = {}
    if period:
        params["period"] = period
    try:
        data = await http_get(url, params=params)
        return _parse_byudzhet_ispolnenie(data)
    except Exception:
        return None


async def poluchit_narusheniya(
    organizaciya: str = "",
    tip: str = "",
) -> list[Narushenie]:
    """Search for violations by organization or type.

    Args:
        organizaciya: Organization name filter.
        tip: Violation type filter.

    Returns:
        List of violations found.
    """
    url = f"{ACH_API_BASE}/narusheniya"
    params: dict[str, str] = {}
    if organizaciya:
        params["organizaciya"] = organizaciya
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _parse_narusheniya(data)
    except Exception:
        return []


def get_napravleniya_list() -> list[dict[str, str]]:
    """Get list of audit directions available for queries."""
    return NAPRAVLENIYA_KONTROLYA


def get_tipy_meropriyatiy_list() -> list[dict[str, str]]:
    """Get list of control measure types."""
    return TIPY_MEROPRIYATIY


def get_subiekty_audita_list() -> list[dict[str, str]]:
    """Get list of external government audit subjects."""
    return SUBIEKTY_AUDITA


# --- Response parsers ---


def _parse_kontrolnoe_meropriyatie(data: Any) -> KontrolnoeMeropriyatie | None:
    """Parse API response into KontrolnoeMeropriyatie."""
    if not isinstance(data, dict):
        return None
    return KontrolnoeMeropriyatie(
        nomer=data.get("nomer", ""),
        nazvanie=data.get("nazvanie", ""),
        tip=data.get("tip", ""),
        napravlenie=data.get("napravlenie", ""),
        data_nachala=data.get("data_nachala", ""),
        data_okonchaniya=data.get("data_okonchaniya", ""),
        status=data.get("status", ""),
        obiem_sredstv=data.get("obiem_sredstv"),
    )


def _parse_auditorskoe_zaklyuchenie(data: Any) -> AuditorskoeZaklyuchenie | None:
    """Parse API response into AuditorskoeZaklyuchenie."""
    if not isinstance(data, dict):
        return None
    return AuditorskoeZaklyuchenie(
        nomer=data.get("nomer", ""),
        nazvanie=data.get("nazvanie", ""),
        data_publikacii=data.get("data_publikacii", ""),
        obekt_audita=data.get("obekt_audita", ""),
        napravlenie=data.get("napravlenie", ""),
        vyavleno_narusheniy=data.get("vyavleno_narusheniy", 0),
        summa_narusheniy=data.get("summa_narusheniy"),
        rekomendacii=data.get("rekomendacii", []),
        ispolnenie=data.get("ispolnenie", ""),
    )


def _parse_byudzhet_ispolnenie(data: Any) -> ByudzhetIspolnenie | None:
    """Parse API response into ByudzhetIspolnenie."""
    if not isinstance(data, dict):
        return None
    return ByudzhetIspolnenie(
        period=data.get("period", ""),
        dohody=data.get("dohody"),
        raskhody=data.get("raskhody"),
        deficit=data.get("deficit"),
    )


def _parse_narusheniya(data: Any) -> list[Narushenie]:
    """Parse API response into list of Narushenie."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            Narushenie(
                opisanie=item.get("opisanie", ""),
                summa=item.get("summa"),
                tip_narusheniya=item.get("tip_narusheniya", ""),
                organizaciya=item.get("organizaciya", ""),
                norma_prava=item.get("norma_prava", ""),
            )
        )
    return results
