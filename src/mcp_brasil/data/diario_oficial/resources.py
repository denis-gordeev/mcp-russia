"""Справочные данные для слоя Diario Oficial (legacy) — слой обратной совместимости.

NOTE: Это слой обратной совместимости (legacy/compatibility layer) в рамках mcp-russia.
Данные бразильских муниципальных официальных вестников сохранены для обратной совместимости
с исторической интеграцией Querido Diário и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import CAPITAIS_COBERTAS


def capitais_cobertas() -> str:
    """(legacy) Бразильские столицы с подтверждённым покрытием в Querido Diário."""
    data = [
        {"codigo_ibge": k, "cidade": v}
        for k, v in sorted(CAPITAIS_COBERTAS.items(), key=lambda x: x[1])
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)
