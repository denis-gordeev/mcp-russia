"""Static reference data for the Diário Oficial feature — legacy compatibility layer.

NOTE: This is a legacy/compatibility layer within mcp-russia.
Brazilian municipal gazetteer data is kept for backward compatibility
with the historical Querido Diário integration and is NOT part of the target Russian data model.
"""

from __future__ import annotations

import json

from .constants import CAPITAIS_COBERTAS


def capitais_cobertas() -> str:
    """Capitais brasileiras com cobertura confirmada no Querido Diário."""
    data = [
        {"codigo_ibge": k, "cidade": v}
        for k, v in sorted(CAPITAIS_COBERTAS.items(), key=lambda x: x[1])
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)
