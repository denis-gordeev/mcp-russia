"""Resources для TCE-CE — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-CE (Счётная палата штата Сеара) сохраняются для обратной
совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_ce() -> str:
    """Доступные endpoints в API открытых данных TCE-CE (SIM) (legacy, Бразилия).

    Перечисляет основные модули с обязательными параметрами.
    """
    endpoints = [
        {
            "endpoint": "/municipios",
            "descricao": "Список 184 муниципалитетов Сеары с кодом и названием (legacy)",
            "parametros_obrigatorios": [],
        },
        {
            "endpoint": "/licitacoes",
            "descricao": "Процедуры муниципальных закупок (legacy)",
            "parametros_obrigatorios": [
                "codigo_municipio",
                "data_realizacao_autuacao_licitacao",
            ],
        },
        {
            "endpoint": "/contrato",
            "descricao": "Муниципальные контракты (постранично, макс. 100/страница) (legacy)",
            "parametros_obrigatorios": [
                "codigo_municipio",
                "data_contrato",
                "quantidade",
                "deslocamento",
            ],
        },
        {
            "endpoint": "/notas_empenhos",
            "descricao": "Бюджетные обязательства (постранично, макс. 100/страница) (legacy)",
            "parametros_obrigatorios": [
                "codigo_municipio",
                "data_referencia_empenho (yyyymm)",
                "codigo_orgao",
                "quantidade",
                "deslocamento",
            ],
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
