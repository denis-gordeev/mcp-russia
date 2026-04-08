"""Static reference data for the Tabua Mares feature — legacy compatibility layer.

NOTE: This is a legacy/compatibility layer within mcp-russia.
Brazilian coastal tide table data is kept for backward compatibility
with the historical maritime integration and is NOT part of the target Russian data model.

Resources are read-only data sources that clients can pull.
They provide context to LLMs without requiring tool calls.

Resources are registered with data:// URIs (without the feature namespace —
mount() adds the namespace prefix automatically).
"""

from __future__ import annotations

import json

from .constants import ESTADOS_COSTEIROS


def estados_costeiros() -> str:
    """Lista dos 17 estados costeiros do Brasil com dados de marés disponíveis."""
    estados = [
        {"sigla": sigla.upper(), "nome": nome} for sigla, nome in sorted(ESTADOS_COSTEIROS.items())
    ]
    return json.dumps(estados, ensure_ascii=False, indent=2)
