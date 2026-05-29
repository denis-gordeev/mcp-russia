"""HTTP client for the Официальные публикации РФ data sources.

Official Russian legal publications from pravo.gov.ru, consultant.ru,
and Russian Gazette (rg.ru).

This module provides placeholder client functions for future API integration.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    CONSULTANT_API_BASE,
    ISTOCHNIKI_PUBLIKATSIY,
    OTRASLI_ZAKONODATELSTVA,
    PRAVO_API_BASE,
    STATUSY_DOKUMENTOV,
    TIPY_NORMATIVNYKH_AKTOV,
)
from .schemas import (
    IzmenenieAkta,
    NormativnyyAkt,
    OficialnayaPublikatsiya,
    ZakonProekt,
)


async def poluchit_normativnyy_akt(nomer: str, tip: str = "") -> NormativnyyAkt | None:
    """Fetch a normative legal act by number.

    Args:
        nomer: Act number/identifier.
        tip: Act type (fz, ukaz, postanovlenie_pr, etc.).

    Returns:
        Act data or None.
    """
    url = f"{PRAVO_API_BASE}/akt/{nomer}"
    params: dict[str, str] = {}
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _parse_normativnyy_akt(data)
    except Exception:
        return None


async def poluchit_zakon_proekt(nomer: str) -> ZakonProekt | None:
    """Fetch a bill by number.

    Args:
        nomer: Bill number.

    Returns:
        Bill data or None.
    """
    url = f"{PRAVO_API_BASE}/zakonproekt/{nomer}"
    try:
        data = await http_get(url)
        return _parse_zakon_proekt(data)
    except Exception:
        return None


async def poluchit_publikatsii(
    tip: str = "",
    otrysl: str = "",
    data_from: str = "",
    data_to: str = "",
) -> list[OficialnayaPublikatsiya]:
    """Search official publications.

    Args:
        tip: Document type filter.
        otrysl: Legal branch filter.
        data_from: Start date filter.
        data_to: End date filter.

    Returns:
        List of publications.
    """
    url = f"{PRAVO_API_BASE}/publikatsii"
    params: dict[str, str] = {}
    if tip:
        params["tip"] = tip
    if otrysl:
        params["otrysl"] = otrysl
    if data_from:
        params["data_from"] = data_from
    if data_to:
        params["data_to"] = data_to
    try:
        data = await http_get(url, params=params)
        return _parse_publikatsii(data)
    except Exception:
        return []


async def poluchit_izmeneniya_akta(akt_nomer: str) -> list[IzmenenieAkta]:
    """Fetch amendments to a legal act.

    Args:
        akt_nomer: Act number.

    Returns:
        List of amendments.
    """
    url = f"{PRAVO_API_BASE}/izmeneniya/{akt_nomer}"
    try:
        data = await http_get(url)
        return _parse_izmeneniya(data)
    except Exception:
        return []


async def poluchit_poisku(tekst: str, tip: str = "") -> list[NormativnyyAkt]:
    """Search legal acts by text.

    Args:
        tekst: Search text.
        tip: Document type filter.

    Returns:
        List of matching acts.
    """
    url = f"{CONSULTANT_API_BASE}/search"
    params: dict[str, str] = {"q": tekst}
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _search_results(data)
    except Exception:
        return []


def get_tipy_aktov_list() -> list[dict[str, str]]:
    """Get list of normative act types."""
    return TIPY_NORMATIVNYKH_AKTOV


def get_otrasli_list() -> list[dict[str, str]]:
    """Get list of legal branches."""
    return OTRASLI_ZAKONODATELSTVA


def get_istochniki_list() -> list[dict[str, str]]:
    """Get list of publication sources."""
    return ISTOCHNIKI_PUBLIKATSIY


def get_statusy_list() -> list[dict[str, str]]:
    """Get list of document statuses."""
    return STATUSY_DOKUMENTOV


# --- Response parsers ---


def _parse_normativnyy_akt(data: Any) -> NormativnyyAkt | None:
    """Parse API response into NormativnyyAkt."""
    if not isinstance(data, dict):
        return None
    return NormativnyyAkt(
        nomer=data.get("nomer", ""),
        nazvanie=data.get("nazvanie", ""),
        tip=data.get("tip", ""),
        data_prinyatiya=data.get("data_prinyatiya", ""),
        data_publikatsii=data.get("data_publikatsii", ""),
        istochnik=data.get("istochnik", ""),
        status=data.get("status", ""),
        otrysl=data.get("otrysl", ""),
        kratkoe_opisanie=data.get("kratkoe_opisanie", ""),
        tekst_url=data.get("tekst_url", ""),
        izmeneniya=data.get("izmeneniya", []),
    )


def _parse_zakon_proekt(data: Any) -> ZakonProekt | None:
    """Parse API response into ZakonProekt."""
    if not isinstance(data, dict):
        return None
    return ZakonProekt(
        nomer=data.get("nomer", ""),
        nazvanie=data.get("nazvanie", ""),
        stadnya=data.get("stadnya", ""),
        data_vneseniya=data.get("data_vneseniya", ""),
        vnesen_subiekt=data.get("vnesen_subiekt", ""),
        otvetstvennyy_komitet=data.get("otvetstvennyy_komitet", ""),
        chteniya=data.get("chteniya", []),
        tekst_url=data.get("tekst_url", ""),
    )


def _parse_publikatsii(data: Any) -> list[OficialnayaPublikatsiya]:
    """Parse API response into list of OficialnayaPublikatsiya."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            OficialnayaPublikatsiya(
                nazvanie=item.get("nazvanie", ""),
                tip_dokumenta=item.get("tip_dokumenta", ""),
                data_publikatsii=item.get("data_publikatsii", ""),
                nomer_vypuska=item.get("nomer_vypuska", ""),
                istochnik=item.get("istochnik", ""),
                rubrika=item.get("rubrika", ""),
                annotaciya=item.get("annotaciya", ""),
                tekst_url=item.get("tekst_url", ""),
            )
        )
    return results


def _parse_izmeneniya(data: Any) -> list[IzmenenieAkta]:
    """Parse API response into list of IzmenenieAkta."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            IzmenenieAkta(
                akt_nomer=item.get("akt_nomer", ""),
                akt_nazvanie=item.get("akt_nazvanie", ""),
                izmenenie_nomer=item.get("izmenenie_nomer", ""),
                izmenenie_data=item.get("izmenenie_data", ""),
                izmenenie_opisanie=item.get("izmenenie_opisanie", ""),
                data_vstupleniya_v_silu=item.get("data_vstupleniya_v_silu", ""),
                tekst_url=item.get("tekst_url", ""),
            )
        )
    return results


def _search_results(data: Any) -> list[NormativnyyAkt]:
    """Parse search results into NormativnyyAkt list."""
    if not isinstance(data, list):
        return []
    results = []
    for item in data:
        results.append(
            NormativnyyAkt(
                nomer=item.get("nomer", ""),
                nazvanie=item.get("nazvanie", ""),
                tip=item.get("tip", ""),
                data_prinyatiya=item.get("data_prinyatiya", ""),
                status=item.get("status", ""),
                otrysl=item.get("otrysl", ""),
                kratkoe_opisanie=item.get("kratkoe_opisanie", ""),
                tekst_url=item.get("tekst_url", ""),
            )
        )
    return results
