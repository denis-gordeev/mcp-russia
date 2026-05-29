"""HTTP client for the Portal Dados Abertos API."""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get
from mcp_russia.exceptions import HttpClientError

from .constants import CONJUNTOS_URL, DEFAULT_PAGE_SIZE, ORGANIZACOES_URL, RECURSOS_URL
from .schemas import (
    ConjuntoDados,
    ConjuntoResultado,
    Organizacao,
    OrganizacaoResultado,
    RecursoDados,
    RecursoResultado,
)

logger = logging.getLogger(__name__)


def _parse_conjunto(item: dict[str, Any]) -> ConjuntoDados:
    org = item.get("organizacao", {}) or {}
    temas = item.get("temas", []) or []
    tema_nomes = [t.get("titulo", t) if isinstance(t, dict) else str(t) for t in temas]
    tags = item.get("tags", []) or []
    tag_nomes = [t.get("nome", t) if isinstance(t, dict) else str(t) for t in tags]
    return ConjuntoDados(
        id=item.get("id"),
        titulo=item.get("titulo"),
        descricao=item.get("descricao"),
        organizacao_nome=org.get("nome") if isinstance(org, dict) else str(org),
        temas=tema_nomes,
        tags=tag_nomes,
        data_criacao=item.get("dataCriacao"),
        data_atualizacao=item.get("dataAtualizacao"),
    )


def _parse_organizacao(item: dict[str, Any]) -> Organizacao:
    return Organizacao(
        id=item.get("id"),
        nome=item.get("nome"),
        descricao=item.get("descricao"),
        total_conjuntos=item.get("totalConjuntoDados"),
    )


def _parse_recurso(item: dict[str, Any]) -> RecursoDados:
    return RecursoDados(
        id=item.get("id"),
        titulo=item.get("titulo"),
        link=item.get("link"),
        formato=item.get("formato"),
        descricao=item.get("descricao"),
    )


async def buscar_conjuntos(
    query: str,
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> ConjuntoResultado:
    """Search datasets in the Portal Dados Abertos catalog.

    Args:
        query: Search term.
        pagina: Page number (1-based).
        tamanho: Page size.

    Returns:
        Paginated result with matching datasets.
    """
    params: dict[str, str] = {
        "isQuerySearch": "true",
        "q": query,
        "pagina": str(pagina),
        "tamanhoPagina": str(tamanho),
    }
    try:
        data: dict[str, Any] = await http_get(CONJUNTOS_URL, params=params)
    except (HttpClientError, Exception) as exc:
        logger.warning("Dados Abertos API error for '%s': %s", query, exc)
        return ConjuntoResultado(total=0, conjuntos=[])

    if not data or not isinstance(data, dict):
        return ConjuntoResultado(total=0, conjuntos=[])

    items = data.get("registros", [])
    conjuntos = [_parse_conjunto(i) for i in items] if isinstance(items, list) else []
    return ConjuntoResultado(
        total=data.get("totalRegistros", len(conjuntos)),
        conjuntos=conjuntos,
    )


async def detalhar_conjunto(conjunto_id: str) -> ConjuntoDados | None:
    """Get full details of a specific dataset.

    Args:
        conjunto_id: Dataset ID.

    Returns:
        Dataset details or None if not found.
    """
    url = f"{CONJUNTOS_URL}/{conjunto_id}"
    try:
        data: dict[str, Any] = await http_get(url)
    except (HttpClientError, Exception) as exc:
        logger.warning("Dados Abertos API error for dataset '%s': %s", conjunto_id, exc)
        return None
    if not data or not isinstance(data, dict):
        return None
    return _parse_conjunto(data)


async def listar_organizacoes(
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> OrganizacaoResultado:
    """List organizations that publish datasets.

    Args:
        pagina: Page number (1-based).
        tamanho: Page size.

    Returns:
        Paginated result with organizations.
    """
    params: dict[str, str] = {
        "pagina": str(pagina),
        "tamanhoPagina": str(tamanho),
    }
    try:
        data: dict[str, Any] = await http_get(ORGANIZACOES_URL, params=params)
    except (HttpClientError, Exception) as exc:
        logger.warning("Dados Abertos API error listing orgs: %s", exc)
        return OrganizacaoResultado(total=0, organizacoes=[])

    if not data or not isinstance(data, dict):
        return OrganizacaoResultado(total=0, organizacoes=[])

    items = data.get("registros", [])
    orgs = [_parse_organizacao(i) for i in items] if isinstance(items, list) else []
    return OrganizacaoResultado(
        total=data.get("totalRegistros", len(orgs)),
        organizacoes=orgs,
    )


async def buscar_recursos(
    conjunto_id: str,
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> RecursoResultado:
    """List resources (files/APIs) of a dataset.

    Args:
        conjunto_id: Dataset ID.
        pagina: Page number (1-based).
        tamanho: Page size.

    Returns:
        Paginated result with resources.
    """
    params: dict[str, str] = {
        "idConjuntoDados": conjunto_id,
        "pagina": str(pagina),
        "tamanhoPagina": str(tamanho),
    }
    try:
        data: dict[str, Any] = await http_get(RECURSOS_URL, params=params)
    except (HttpClientError, Exception) as exc:
        logger.warning("Dados Abertos API error for resources '%s': %s", conjunto_id, exc)
        return RecursoResultado(total=0, recursos=[])

    if not data or not isinstance(data, dict):
        return RecursoResultado(total=0, recursos=[])

    items = data.get("registros", [])
    recursos = [_parse_recurso(i) for i in items] if isinstance(items, list) else []
    return RecursoResultado(
        total=data.get("totalRegistros", len(recursos)),
        recursos=recursos,
    )
