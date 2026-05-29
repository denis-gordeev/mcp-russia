"""Resources для TCE-SC — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-SC (Счётная палата штата Санта-Катарина) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_sc() -> str:
    """Каталог доступных endpoints в TCE-SC (legacy, Бразилия)."""
    endpoints = [
        {
            "endpoint": "municipios.php",
            "descricao": "Список муниципалитетов SC с кодом IBGE (295 муниципалитетов) (legacy)",
        },
        {
            "endpoint": "unidades-gestoras.php",
            "descricao": "Управляющие единицы с кодом, названием, аббревиатурой и муниципалитетом (~2768 единиц) (legacy)",
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
