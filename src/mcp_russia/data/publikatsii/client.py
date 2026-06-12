"""HTTP-клиент для модуля Официальные публикации РФ.

Официальные российские правовые публикации с открытого API pravo.gov.ru,
КонсультантПлюс (платный) и Российская газета (rg.ru).
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    ISTOCHNIKI_PUBLIKATSIY,
    OTRASLI_ZAKONODATELSTVA,
    PRAVO_DOCUMENT_URL,
    PRAVO_SEARCH_URL,
    STATUSY_DOKUMENTOV,
    TIPY_DOKUMENTOV_PRAVO,
    TIPY_NORMATIVNYKH_AKTOV,
)
from .schemas import (
    IzmenenieAkta,
    NormativnyyAkt,
    OficialnayaPublikatsiya,
    ZakonProekt,
)


async def poluchit_normativnyy_akt(nomer: str, tip: str = "") -> NormativnyyAkt | None:
    """Fetch a normative legal act by number from pravo.gov.ru open data.

    Args:
        nomer: Act number/identifier (e.g. "ФЗ-123", "УП-234").
        tip: Act type code (fz, ukaz, postanovlenie_pr, etc.).

    Returns:
        Act data or None.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
    params: dict[str, str] = {}
    if tip:
        params["tip"] = tip
    try:
        data = await http_get(url, params=params)
        return _parse_normativnyy_akt(data)
    except Exception:
        return None


async def poluchit_zakon_proekt(nomer: str) -> ZakonProekt | None:
    """Fetch a bill by number from pravo.gov.ru open data.

    Args:
        nomer: Bill number.

    Returns:
        Bill data or None.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
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
    """Search official publications via pravo.gov.ru open data.

    Args:
        tip: Document type filter (pravo.gov.ru type code).
        otrysl: Legal branch filter.
        data_from: Start date filter (YYYY-MM-DD).
        data_to: End date filter (YYYY-MM-DD).

    Returns:
        List of publications.
    """
    url = PRAVO_SEARCH_URL
    params: dict[str, str] = {}
    if tip:
        params["type"] = tip
    if otrysl:
        params["branch"] = otrysl
    if data_from:
        params["dateFrom"] = data_from
    if data_to:
        params["dateTo"] = data_to
    try:
        data = await http_get(url, params=params)
        return _parse_publikatsii(data)
    except Exception:
        return []


async def poluchit_izmeneniya_akta(akt_nomer: str) -> list[IzmenenieAkta]:
    """Получение поправок к нормативному акту из открытых данных pravo.gov.ru.

    Args:
        akt_nomer: Номер/идентификатор акта.

    Returns:
        Список поправок.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{akt_nomer}/amendments"
    try:
        data = await http_get(url)
        return _parse_izmeneniya(data)
    except Exception:
        return []


async def poluchit_poisku(tekst: str, tip: str = "") -> list[NormativnyyAkt]:
    """Search legal acts by text via pravo.gov.ru open data.

    Args:
        tekst: Search text.
        tip: Document type filter (pravo.gov.ru type code).

    Returns:
        List of matching acts.
    """
    url = PRAVO_SEARCH_URL
    params: dict[str, str] = {"q": tekst}
    if tip:
        params["type"] = tip
    try:
        data = await http_get(url, params=params)
        return _search_results(data)
    except Exception:
        return []


def get_tipy_aktov_list() -> list[dict[str, str]]:
    """Возвращает список типов нормативных актов."""
    return TIPY_NORMATIVNYKH_AKTOV


def get_otrasli_list() -> list[dict[str, str]]:
    """Возвращает список отраслей права."""
    return OTRASLI_ZAKONODATELSTVA


def get_istochniki_list() -> list[dict[str, str]]:
    """Возвращает список источников публикаций."""
    return ISTOCHNIKI_PUBLIKATSIY


def get_statusy_list() -> list[dict[str, str]]:
    """Возвращает список статусов документов."""
    return STATUSY_DOKUMENTOV


# --- Response parsers ---


def _parse_normativnyy_akt(data: Any) -> NormativnyyAkt | None:
    """Parse pravo.gov.ru open data response into NormativnyyAkt."""
    if not isinstance(data, dict):
        return None
    tip_code = str(data.get("type", data.get("tip", "")) or "")
    tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
    return NormativnyyAkt(
        nomer=data.get("number", data.get("nomer", "")) or "",
        nazvanie=data.get("title", data.get("nazvanie", "")) or "",
        tip=tip_name,
        data_prinyatiya=data.get("date", data.get("data_prinyatiya", "")) or "",
        data_publikatsii=data.get("publishDate", data.get("data_publikatsii", "")) or "",
        istochnik=data.get("source", data.get("istochnik", "pravo.gov.ru")) or "",
        status=data.get("status", "") or "",
        otrysl=data.get("branch", data.get("otrysl", "")) or "",
        kratkoe_opisanie=data.get("description", data.get("kratkoe_opisanie", "")) or "",
        tekst_url=data.get("url", data.get("tekst_url", "")) or "",
        izmeneniya=data.get("amendments", data.get("izmeneniya", [])) or [],
    )


def _parse_zakon_proekt(data: Any) -> ZakonProekt | None:
    """Parse pravo.gov.ru open data response into ZakonProekt."""
    if not isinstance(data, dict):
        return None
    return ZakonProekt(
        nomer=data.get("number", data.get("nomer", "")) or "",
        nazvanie=data.get("title", data.get("nazvanie", "")) or "",
        stadnya=data.get("stage", data.get("stadnya", "")) or "",
        data_vneseniya=data.get("introducedDate", data.get("data_vneseniya", "")) or "",
        vnesen_subiekt=data.get("introducedBy", data.get("vnesen_subiekt", "")) or "",
        otvetstvennyy_komitet=data.get("committee", data.get("otvetstvennyy_komitet", "")) or "",
        chteniya=data.get("readings", data.get("chteniya", [])) or [],
        tekst_url=data.get("url", data.get("tekst_url", "")) or "",
    )


def _parse_publikatsii(data: Any) -> list[OficialnayaPublikatsiya]:
    """Parse pravo.gov.ru open data search response into list of OficialnayaPublikatsiya."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("documents", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        tip_code = str(item.get("type", item.get("tip_dokumenta", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        results.append(
            OficialnayaPublikatsiya(
                nazvanie=item.get("title", item.get("nazvanie", "")),
                tip_dokumenta=tip_name,
                data_publikatsii=item.get("publishDate", item.get("data_publikatsii", "")),
                nomer_vypuska=item.get("issueNumber", item.get("nomer_vypuska", "")),
                istochnik=item.get("source", item.get("istochnik", "pravo.gov.ru")),
                rubrika=item.get("rubric", item.get("rubrika", "")),
                annotaciya=item.get("annotation", item.get("annotaciya", "")),
                tekst_url=item.get("url", item.get("tekst_url", "")),
            )
        )
    return results


def _parse_izmeneniya(data: Any) -> list[IzmenenieAkta]:
    """Parse pravo.gov.ru open data amendments response into list of IzmenenieAkta."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("amendments", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        results.append(
            IzmenenieAkta(
                akt_nomer=item.get("actNumber", item.get("akt_nomer", "")),
                akt_nazvanie=item.get("actTitle", item.get("akt_nazvanie", "")),
                izmenenie_nomer=item.get("amendmentNumber", item.get("izmenenie_nomer", "")),
                izmenenie_data=item.get("amendmentDate", item.get("izmenenie_data", "")),
                izmenenie_opisanie=item.get(
                    "amendmentDescription", item.get("izmenenie_opisanie", "")
                ),
                data_vstupleniya_v_silu=item.get(
                    "effectiveDate", item.get("data_vstupleniya_v_silu", "")
                ),
                tekst_url=item.get("url", item.get("tekst_url", "")),
            )
        )
    return results


def _search_results(data: Any) -> list[NormativnyyAkt]:
    """Parse pravo.gov.ru open data search results into NormativnyyAkt list."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("documents", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        tip_code = str(item.get("type", item.get("tip", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        results.append(
            NormativnyyAkt(
                nomer=item.get("number", item.get("nomer", "")),
                nazvanie=item.get("title", item.get("nazvanie", "")),
                tip=tip_name,
                data_prinyatiya=item.get("date", item.get("data_prinyatiya", "")),
                status=item.get("status", ""),
                otrysl=item.get("branch", item.get("otrysl", "")),
                kratkoe_opisanie=item.get("description", item.get("kratkoe_opisanie", "")),
                tekst_url=item.get("url", item.get("tekst_url", "")),
            )
        )
    return results
