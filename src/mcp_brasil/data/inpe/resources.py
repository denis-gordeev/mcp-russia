"""Resources for the INPE feature — legacy compatibility layer for Brazilian environmental data.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian environmental reference datasets are kept for backward compatibility
with the historical INPE integration and are NOT part of the target Russian data model.
"""

from __future__ import annotations

import json

from .constants import BIOMAS, ESTADOS_AMAZONIA_LEGAL


def biomas_brasileiros() -> str:
    """Lista dos 6 biomas brasileiros monitorados pelo INPE."""
    data = [{"codigo": k, "nome": v} for k, v in BIOMAS.items()]
    return json.dumps(data, ensure_ascii=False)


def estados_amazonia_legal() -> str:
    """Lista dos 9 estados da Amazônia Legal."""
    data = [{"sigla": uf} for uf in ESTADOS_AMAZONIA_LEGAL]
    return json.dumps(data, ensure_ascii=False)
