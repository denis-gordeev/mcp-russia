"""Resources для TCE-RJ — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-RJ (Счётная палата штата Рио-де-Жанейро) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_disponiveis() -> str:
    """Доступные endpoints в API открытых данных TCE-RJ (legacy, Бразилия).

    Перечисляет модули открытых данных с описанием и доступными фильтрами.
    """
    endpoints = [
        {
            "modulo": "Закупки",
            "descricao": "Процедуры закупок 92 муниципалитетов штата Рио-де-Жанейро (legacy)",
            "filtros": ["ano", "municipio"],
            "paginacao": True,
        },
        {
            "modulo": "Муниципальные контракты",
            "descricao": "Контракты, заключённые муниципалитетами с поставщиками (legacy)",
            "filtros": ["ano", "municipio"],
            "paginacao": True,
        },
        {
            "modulo": "Прямые закупки",
            "descricao": "Отказания от закупок и требования (муниципальный и штатный уровень) (legacy)",
            "filtros": ["ano", "municipio"],
            "paginacao": True,
        },
        {
            "modulo": "Приостановленные работы",
            "descricao": "Приостановленные общественные работы (штат и муниципалитеты) (legacy)",
            "filtros": [],
            "paginacao": False,
        },
        {
            "modulo": "Штрафы",
            "descricao": "Штрафы и задолженности, наложенные TCE-RJ на муниципальных управленцев (legacy)",
            "filtros": ["tipo"],
            "paginacao": False,
        },
        {
            "modulo": "Отчётность",
            "descricao": "Заключения TCE-RJ по отчётам мэров (legacy)",
            "filtros": [],
            "paginacao": False,
        },
        {
            "modulo": "Публичные концессии",
            "descricao": "ГЧП и концессии муниципальных общественных услуг (legacy)",
            "filtros": ["municipio"],
            "paginacao": False,
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
