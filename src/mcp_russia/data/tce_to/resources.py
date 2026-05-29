"""Resources для TCE-TO — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-TO (Счётная палата штата Токантинс) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_to() -> str:
    """Каталог доступных endpoints в TCE-TO (legacy, Бразилия)."""
    endpoints = [
        {
            "endpoint": "/pessoas",
            "params": "nome, codigo, pagina, tamanho",
            "descricao": "Поиск лиц с делами (требуется хотя бы один фильтр) (legacy)",
        },
        {
            "endpoint": "/processo/{numero}/{ano}",
            "descricao": "Детали конкретного дела (legacy)",
        },
        {
            "endpoint": "/pautas",
            "params": "ordem, tamanho",
            "descricao": "Повестки заседаний камер и пленума (legacy)",
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
