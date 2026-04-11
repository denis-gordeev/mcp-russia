"""Resources для TCE-RN — уровень обратной совместимости для бразильских данных аудита.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TCE-RN (Счётная палата штата Риу-Гранди-ду-Норти) сохраняются для
обратной совместимости с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def endpoints_tce_rn() -> str:
    """Каталог доступных endpoints в TCE-RN (legacy, Бразилия)."""
    endpoints = [
        {
            "grupo": "Основная информация",
            "endpoint": "/InformacoesBasicasApi/JurisdicionadosTCE/{formato}",
            "descricao": "Список подконтрольных TCE-RN организаций (~914) (legacy)",
        },
        {
            "grupo": "Бюджетный баланс",
            "endpoint": "/BalancoOrcamentarioApi/Despesa/{fmt}/{ano}/{bimestre}/{id}",
            "descricao": "Бюджетные расходы по единице, году и двухмесячному периоду (legacy)",
        },
        {
            "grupo": "Бюджетный баланс",
            "endpoint": "/BalancoOrcamentarioApi/Receita/{fmt}/{ano}/{bimestre}/{id}",
            "descricao": "Бюджетные доходы по единице, году и двухмесячному периоду (legacy)",
        },
        {
            "grupo": "Процедуры закупок",
            "endpoint": "/ProcedimentosLicitatoriosApi/LicitacaoPublica/{fmt}/{id}/{di}/{df}",
            "descricao": "Публичные закупки по единице и периоду (legacy)",
        },
        {
            "grupo": "Контракты",
            "endpoint": "/ContratosApi/Contratos/{fmt}/{id}/{hierarquia}",
            "descricao": "Контракты по подконтрольной единице (legacy)",
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
