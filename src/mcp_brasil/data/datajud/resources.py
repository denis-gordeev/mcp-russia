"""Resources for the DataJud feature — legacy compatibility layer for Brazilian judicial data.

NOTE: This is a legacy/compatibility layer within mcp-russia.
Brazilian judicial reference data is kept for backward compatibility
with the historical CNJ DataJud integration and is NOT part of the target Russian data model.
"""

from __future__ import annotations

import json

from .constants import CLASSES_PROCESSUAIS, DATAJUD_API_BASE, TRIBUNAIS, TRIBUNAL_NOMES


def tribunais_disponiveis() -> str:
    """Lista de tribunais disponíveis na API DataJud com siglas e nomes."""
    data = [
        {"sigla": sigla, "nome": TRIBUNAL_NOMES.get(sigla, sigla.upper())}
        for sigla in sorted(TRIBUNAIS.keys())
    ]
    return json.dumps(data, ensure_ascii=False)


def classes_processuais() -> str:
    """Classes processuais comuns para busca no DataJud."""
    return json.dumps(CLASSES_PROCESSUAIS, ensure_ascii=False)


def info_api() -> str:
    """Informações gerais sobre a API DataJud (CNJ)."""
    data = {
        "nome": "API Pública DataJud — Conselho Nacional de Justiça",
        "url_base": DATAJUD_API_BASE,
        "autenticacao": "Requer API Key (cadastro em datajud.cnj.jus.br)",
        "formato": "Elasticsearch (POST com body JSON)",
        "documentacao": "https://datajud-wiki.cnj.jus.br/api-publica/",
        "cobertura": "Processos de todos os tribunais brasileiros (legacy/compatibility layer)",
        "total_tribunais": len(TRIBUNAIS),
    }
    return json.dumps(data, ensure_ascii=False)
