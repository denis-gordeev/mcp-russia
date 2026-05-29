"""Resources для Tabua Mares — уровень обратной совместимости для бразильских данных о приливах.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские данные о таблицах приливов для прибрежных зон сохраняются для обратной совместимости
с исторической морской интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json

from .constants import ESTADOS_COSTEIROS


def estados_costeiros() -> str:
    """Список 17 бразильских прибрежных штатов с доступными данными о приливах (legacy)."""
    estados = [
        {"sigla": sigla.upper(), "nome": nome} for sigla, nome in sorted(ESTADOS_COSTEIROS.items())
    ]
    return json.dumps(estados, ensure_ascii=False, indent=2)
