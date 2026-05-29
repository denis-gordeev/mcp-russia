"""HTTP client for the Querido Diário API.

Endpoints:
    - /gazettes?querystring=...        → buscar_diarios
    - /gazettes/{territory_id}?...     → buscar_diarios (por município)
    - /cities?city_name=...            → buscar_cidades
    - /cities                          → listar_cidades
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get
from mcp_russia.exceptions import HttpClientError

from .constants import CITIES_URL, DEFAULT_PAGE_SIZE, EXCERPTS_URL, GAZETTES_URL
from .schemas import (
    CidadeQueridoDiario,
    DiarioOficial,
    DiarioResultado,
    Excerto,
    ExcertoResultado,
)

logger = logging.getLogger(__name__)


async def buscar_diarios(
    querystring: str,
    territory_id: str | None = None,
    since: str | None = None,
    until: str | None = None,
    offset: int = 0,
    size: int = DEFAULT_PAGE_SIZE,
) -> DiarioResultado:
    """Search gazettes by keyword, optionally filtered by territory and date range."""
    url = f"{GAZETTES_URL}/{territory_id}" if territory_id else GAZETTES_URL

    params: dict[str, str] = {
        "querystring": querystring,
        "offset": str(offset),
        "size": str(size),
    }
    if since:
        params["since"] = since
    if until:
        params["until"] = until

    try:
        data: dict[str, Any] = await http_get(url, params=params)
    except HttpClientError as exc:
        logger.warning("Querido Diário API error for '%s': %s", querystring, exc)
        return DiarioResultado(total_gazettes=0, gazettes=[])

    if not data or not isinstance(data, dict):
        return DiarioResultado(total_gazettes=0, gazettes=[])

    gazettes = [DiarioOficial(**g) for g in data.get("gazettes", [])]
    return DiarioResultado(
        total_gazettes=data.get("total_gazettes", len(gazettes)),
        gazettes=gazettes,
    )


async def buscar_trechos(
    territory_id: str,
    querystring: str,
    since: str | None = None,
    until: str | None = None,
    offset: int = 0,
    size: int = DEFAULT_PAGE_SIZE,
) -> ExcertoResultado:
    """Search excerpts within a specific territory's gazettes."""
    url = EXCERPTS_URL.format(territory_id=territory_id)

    params: dict[str, str] = {
        "querystring": querystring,
        "offset": str(offset),
        "size": str(size),
    }
    if since:
        params["since"] = since
    if until:
        params["until"] = until

    try:
        data: dict[str, Any] = await http_get(url, params=params)
    except HttpClientError as exc:
        logger.warning("Querido Diário API error for '%s': %s", querystring, exc)
        return ExcertoResultado(total_excerpts=0, excerpts=[])

    if not data or not isinstance(data, dict):
        return ExcertoResultado(total_excerpts=0, excerpts=[])

    excerpts = [Excerto(**e) for e in data.get("excerpts", [])]
    return ExcertoResultado(
        total_excerpts=data.get("total_excerpts", len(excerpts)),
        excerpts=excerpts,
    )


async def buscar_cidades(nome_cidade: str) -> list[CidadeQueridoDiario]:
    """Search cities available in Querido Diário by name."""
    try:
        data: list[dict[str, Any]] = await http_get(CITIES_URL, params={"city_name": nome_cidade})
    except (HttpClientError, Exception) as exc:
        logger.warning("Querido Diário API error searching cities '%s': %s", nome_cidade, exc)
        return []

    if not data or not isinstance(data, list):
        return []
    return [CidadeQueridoDiario(**c) for c in data]


async def listar_cidades() -> list[CidadeQueridoDiario]:
    """List all cities available in Querido Diário."""
    try:
        data: list[dict[str, Any]] = await http_get(CITIES_URL)
    except (HttpClientError, Exception) as exc:
        logger.warning("Querido Diário API error listing cities: %s", exc)
        return []

    if not data or not isinstance(data, list):
        return []
    return [CidadeQueridoDiario(**c) for c in data]
