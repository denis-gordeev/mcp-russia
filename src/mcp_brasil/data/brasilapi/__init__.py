"""Совместимый слой BrasilAPI внутри публичного контура mcp-russia.

.. deprecated::
    Этот модуль содержит только данные BrasilAPI для обратной совместимости.
    Для работы с российскими справочными данными используйте модуль ``rosapi``.
    Модуль ``rosapi`` предоставляет:
    - Поиск адреса по почтовому индексу РФ (ФИАС)
    - Поиск организации по ИНН/ОГРН
    - Справочник банков с БИК
    - Праздники РФ
    - Налоговые ставки РФ
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="brasilapi",
    description=(
        "⚠️ DEPRECATED: Legacy-слой BrasilAPI. "
        "Для российских справочных данных используйте модуль 'rosapi'. "
        "Бразильские справочные данные: CEP, CNPJ, DDD, банки, валюты, "
        "праздники, ставки, FIPE, ISBN, NCM, PIX, Registro.br."
    ),
    version="0.1.0-deprecated",
    api_base="https://brasilapi.com.br/api",
    requires_auth=False,
    tags=[
        "устаревший",
        "бразилия-legacy",
        "cep",
        "cnpj",
        "bancos",
        "cambio",
        "fipe",
        "feriados",
        "isbn",
        "ncm",
        "pix",
    ],
)
