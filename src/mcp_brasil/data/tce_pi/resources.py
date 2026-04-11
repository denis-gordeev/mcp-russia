"""Resources для TCE-PI — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-PI (Счётная палата штата Пиауи) сохраняются для обратной
совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

import json


def endpoints_tce_pi() -> str:
    """JSON-описание всех endpoints TCE-PI (legacy, Бразилия)."""
    return json.dumps(
        {
            "api_base": "https://sistemas.tce.pi.gov.br/api/portaldacidadania",
            "auth": "Отсутствует",
            "endpoints": [
                {
                    "path": "/prefeituras",
                    "descricao": "Список всех 224 префектур Пиауи (legacy)",
                },
                {
                    "path": "/prefeituras/:nome",
                    "descricao": "Поиск префектур по названию (legacy)",
                },
                {
                    "path": "/prefeituras/:id/gestor",
                    "descricao": "Запрос текущего мэра (legacy)",
                },
                {
                    "path": "/despesas/:id",
                    "descricao": "История расходов муниципалитета по годам (legacy)",
                },
                {
                    "path": "/despesas/:id/:exercicio/porFuncao",
                    "descricao": "Расходы по функциям управления (legacy)",
                },
                {
                    "path": "/despesas/total",
                    "descricao": "Общие расходы штата по годам (legacy)",
                },
                {
                    "path": "/receitas/:id/:exercicio",
                    "descricao": "Детализированные доходы муниципалитета (legacy)",
                },
                {
                    "path": "/receitas/total",
                    "descricao": "Общие доходы штата по годам (legacy)",
                },
                {
                    "path": "/orgaos/lista/:exercicio",
                    "descricao": "Список штатных органов по финансовому году (legacy)",
                },
                {
                    "path": "/credores/:id/:exercicio",
                    "descricao": "Топ-10 кредиторов муниципалитета (legacy)",
                },
            ],
        },
        ensure_ascii=False,
    )
