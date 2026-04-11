"""Resources для TCE-RS — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-RS (Счётная палата штата Риу-Гранди-ду-Сул) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_rs() -> str:
    """Каталог endpoints и доступных данных на портале TCE-RS (legacy, Бразилия)."""
    endpoints = [
        {
            "grupo": "Вспомогательные данные",
            "url": "dados/auxiliar/municipios.json",
            "descricao": "Список муниципалитетов RS с кодами TCE и IBGE (legacy)",
        },
        {
            "grupo": "Образование",
            "url": "dados/municipal/educacao-indice/{ano}.json",
            "descricao": "Индекс расходов на образование (MDE) по муниципалитету и году (legacy)",
        },
        {
            "grupo": "Здравоохранение",
            "url": "dados/municipal/saude-indice/{ano}.json",
            "descricao": "Индекс расходов на здравоохранение (ASPS) по муниципалитету и году (legacy)",
        },
        {
            "grupo": "Фискальное управление",
            "url": "dados/municipal/gastos-lrf-mde-asps/{ano}.json",
            "descricao": "Данные фискального управления (LRF) муниципальной исполнительной власти (legacy)",
        },
        {
            "grupo": "Расходы",
            "url": "dados/municipal/balancete-despesa/{ano}.json",
            "descricao": "Сводный баланс расходов (большой файл, >100 МБ) (legacy)",
        },
        {
            "grupo": "Доходы",
            "url": "dados/municipal/balancete-receita/{ano}.json",
            "descricao": "Сводный баланс доходов (большой файл) (legacy)",
        },
        {
            "grupo": "Закупки",
            "url": "dados/licitacon/licitacao/ano/{ano}.csv.zip",
            "descricao": "Сводные закупки LicitaCon (ZIP с CSV) (legacy)",
        },
        {
            "grupo": "Контракты",
            "url": "dados/licitacon/contrato/ano/{ano}.csv.zip",
            "descricao": "Сводные контракты LicitaCon (ZIP с CSV) (legacy)",
        },
        {
            "grupo": "CKAN API",
            "url": "api/3/action/package_search",
            "descricao": "Поиск наборов данных по тексту и группе (16 групп, ~69 тыс. наборов) (legacy)",
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
