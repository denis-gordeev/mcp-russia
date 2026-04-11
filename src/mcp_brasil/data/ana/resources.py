"""Resources для ANA — уровень обратной совместимости для бразильских гидрологических данных.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные ANA сохраняются для обратной совместимости
с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json

from .constants import TIPOS_ESTACAO


def tipos_estacao() -> str:
    """Типы гидрологических станций ANA (флювиометрические и плювиометрические) (legacy)."""
    data = [
        {"codigo": codigo, "descricao": descricao} for codigo, descricao in TIPOS_ESTACAO.items()
    ]
    return json.dumps(data, ensure_ascii=False)
