"""Resources для TCE-PE — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-PE (Счётная палата штата Пернамбуку) сохраняются для обратной
совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_pe() -> str:
    """Доступные endpoints в API открытых данных TCE-PE (legacy, Бразилия).

    Перечисляет основные модули с типичными параметрами.
    """
    endpoints = [
        {
            "endpoint": "UnidadesJurisdicionadas",
            "descricao": "Подконтрольные единицы (префектуры, камеры и т.д.) (legacy)",
            "parametros": ["NATUREZA", "MUNICIPIO"],
        },
        {
            "endpoint": "LicitacaoUG",
            "descricao": "Закупки по управляющей единице (legacy)",
            "parametros": ["ANOLICITACAO", "MUNICIPIO", "MODALIDADE"],
        },
        {
            "endpoint": "Contratos",
            "descricao": "Муниципальные и штатные контракты (legacy)",
            "parametros": ["ANOREFERENCIA", "MUNICIPIO", "CPFCNPJ"],
        },
        {
            "endpoint": "DespesasMunicipais",
            "descricao": "Муниципальные расходы (бюджетные обязательства, ликвидация, платежи) (legacy)",
            "parametros": [
                "ANOREFERENCIA",
                "MESREFERENCIA",
                "CODIGO_MUNICIPIO",
            ],
        },
        {
            "endpoint": "Fornecedores",
            "descricao": "Поставщики, зарегистрированные в SAGRES (legacy)",
            "parametros": ["NOME", "CPFCNPJ"],
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
