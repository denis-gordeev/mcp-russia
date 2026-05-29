"""Resources для TCE-SP — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-SP (Счётная палата штата Сан-Паулу) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_sp() -> str:
    """Доступные endpoints в API прозрачности TCE-SP (legacy, Бразилия).

    Описывает 3 JSON-endpoint'а с параметрами и форматом данных.
    """
    endpoints = [
        {
            "endpoint": "municipios",
            "descricao": "Список 645 муниципалитетов Сан-Паулу с slug и названием (legacy)",
            "parametros": [],
        },
        {
            "endpoint": "despesas/{municipio}/{exercicio}/{mes}",
            "descricao": "Муниципальные расходы: бюджетные обязательства, платежи, ликвидация и аннулирования (legacy)",
            "parametros": ["municipio (slug)", "exercicio (2014+)", "mes (1-12)"],
            "eventos": ["Empenhado", "Valor Pago", "Valor Liquidado", "Anulação"],
        },
        {
            "endpoint": "receitas/{municipio}/{exercicio}/{mes}",
            "descricao": "Муниципальные доходы по источнику ресурса и классификации (legacy)",
            "parametros": ["municipio (slug)", "exercicio (2014+)", "mes (1-12)"],
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
