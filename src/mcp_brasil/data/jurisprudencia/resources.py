"""Resources для Jurisprudencia — уровень обратной совместимости для бразильских судебных данных.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные судебной практики сохраняются для обратной совместимости
с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json

from .constants import OPERADORES_BUSCA, TRIBUNAIS_SUPERIORES


def tribunais_superiores() -> str:
    """Информация о высших судах Бразилии (STF, STJ, TST) (legacy)."""
    return json.dumps(TRIBUNAIS_SUPERIORES, ensure_ascii=False)


def operadores_busca() -> str:
    """Доступные операторы поиска по судам для поиска судебной практики (legacy)."""
    return json.dumps(OPERADORES_BUSCA, ensure_ascii=False)


def info_api() -> str:
    """Общая информация об API судебной практики Бразилии (legacy)."""
    data = {
        "nome": "API судебной практики — STF, STJ и TST (Бразилия, legacy)",
        "tribunais": ["STF", "STJ", "TST"],
        "autenticacao": "Не требует аутентификации",
        "formato": "REST (JSON) — неофициальные API (reverse-engineered)",
        "tipos_busca": [
            "Решения коллегий (acordaos)",
            "Суммарные положения (связывающие и несвязывающие)",
            "Общая реперкуссия (темы общего охвата — STF)",
            "Информационные бюллетени (периодические резюме решений)",
        ],
        "observacao": (
            "API основаны на системах поиска судов. "
            "Результаты могут варьироваться в зависимости от доступности сервисов. "
            "Данные относятся к бразильской судебной системе (legacy)."
        ),
    }
    return json.dumps(data, ensure_ascii=False)
