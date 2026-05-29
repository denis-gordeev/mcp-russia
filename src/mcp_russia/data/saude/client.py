"""HTTP client for the CNES/DataSUS API.

Endpoints:
    - /estabelecimentos     → buscar_estabelecimentos
    - /profissionais        → buscar_profissionais
    - /tipodeestabelecimento → listar_tipos_estabelecimento
    - /leitos               → consultar_leitos
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    DEFAULT_LIMIT,
    ESTABELECIMENTOS_URL,
    LEITOS_URL,
    MAX_LIMIT,
    PROFISSIONAIS_URL,
    TIPOS_URL,
)
from .schemas import Estabelecimento, Leito, Profissional, TipoEstabelecimento


def _parse_estabelecimento(raw: dict[str, Any]) -> Estabelecimento:
    """Parse a raw establishment dict into an Estabelecimento model."""
    return Estabelecimento(
        codigo_cnes=str(raw.get("codigo_cnes", "") or ""),
        nome_fantasia=raw.get("nome_fantasia"),
        nome_razao_social=raw.get("nome_razao_social"),
        natureza_organizacao=raw.get("natureza_organizacao"),
        tipo_gestao=raw.get("tipo_gestao"),
        codigo_tipo=str(raw.get("codigo_tipo_estabelecimento", "") or ""),
        descricao_tipo=raw.get("descricao_tipo_estabelecimento"),
        codigo_municipio=str(raw.get("codigo_municipio", "") or ""),
        codigo_uf=str(raw.get("codigo_uf", "") or ""),
        endereco=raw.get("endereco"),
    )


def _parse_profissional(raw: dict[str, Any]) -> Profissional:
    """Parse a raw professional dict into a Profissional model."""
    return Profissional(
        codigo_cnes=str(raw.get("codigo_cnes", "") or ""),
        nome=raw.get("nome"),
        cns=raw.get("cns"),
        cbo=raw.get("cbo"),
        descricao_cbo=raw.get("descricao_cbo"),
    )


def _parse_tipo(raw: dict[str, Any]) -> TipoEstabelecimento:
    """Parse a raw type dict into a TipoEstabelecimento model."""
    return TipoEstabelecimento(
        codigo=str(raw.get("codigo_tipo_estabelecimento", "") or ""),
        descricao=raw.get("descricao_tipo_estabelecimento"),
    )


def _parse_leito(raw: dict[str, Any]) -> Leito:
    """Parse a raw bed dict into a Leito model."""
    return Leito(
        codigo_cnes=str(raw.get("codigo_cnes", "") or ""),
        tipo_leito=raw.get("tipo_leito"),
        especialidade=raw.get("especialidade"),
        existente=raw.get("existente"),
        sus=raw.get("sus"),
    )


async def buscar_estabelecimentos(
    *,
    codigo_municipio: str | None = None,
    codigo_uf: str | None = None,
    status: int | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> list[Estabelecimento]:
    """Search health establishments from CNES.

    API: GET /estabelecimentos

    Args:
        codigo_municipio: IBGE municipality code (e.g. "355030").
        codigo_uf: IBGE state code (e.g. "35").
        status: 1 for active, 0 for inactive.
        limit: Max results per page.
        offset: Pagination offset.
    """
    params: dict[str, Any] = {
        "limit": min(limit, MAX_LIMIT),
        "offset": offset,
    }
    if codigo_municipio:
        params["codigo_municipio"] = codigo_municipio
    if codigo_uf:
        params["codigo_uf"] = codigo_uf
    if status is not None:
        params["status"] = status

    data: list[dict[str, Any]] = await http_get(ESTABELECIMENTOS_URL, params=params)
    return [_parse_estabelecimento(item) for item in data]


async def buscar_profissionais(
    *,
    codigo_municipio: str | None = None,
    cnes: str | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> list[Profissional]:
    """Search health professionals from CNES.

    API: GET /profissionais

    Args:
        codigo_municipio: IBGE municipality code.
        cnes: CNES establishment code.
        limit: Max results per page.
        offset: Pagination offset.
    """
    params: dict[str, Any] = {
        "limit": min(limit, MAX_LIMIT),
        "offset": offset,
    }
    if codigo_municipio:
        params["codigo_municipio"] = codigo_municipio
    if cnes:
        params["cnes"] = cnes

    data: list[dict[str, Any]] = await http_get(PROFISSIONAIS_URL, params=params)
    return [_parse_profissional(item) for item in data]


async def listar_tipos_estabelecimento() -> list[TipoEstabelecimento]:
    """Fetch all establishment types from CNES.

    API: GET /tipodeestabelecimento
    """
    data: list[dict[str, Any]] = await http_get(TIPOS_URL)
    return [_parse_tipo(item) for item in data]


async def consultar_leitos(
    *,
    codigo_municipio: str | None = None,
    cnes: str | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> list[Leito]:
    """Search hospital beds from CNES.

    API: GET /leitos

    Args:
        codigo_municipio: IBGE municipality code.
        cnes: CNES establishment code.
        limit: Max results per page.
        offset: Pagination offset.
    """
    params: dict[str, Any] = {
        "limit": min(limit, MAX_LIMIT),
        "offset": offset,
    }
    if codigo_municipio:
        params["codigo_municipio"] = codigo_municipio
    if cnes:
        params["cnes"] = cnes

    data: list[dict[str, Any]] = await http_get(LEITOS_URL, params=params)
    return [_parse_leito(item) for item in data]
