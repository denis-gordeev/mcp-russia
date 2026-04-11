"""Legacy Bacen — переходный слой данных Banco Central do Brasil.

.. deprecated::
    Этот модуль содержит только данные Центрального банка Бразилии для обратной совместимости.
    Для работы с данными Центрального банка РФ используйте модуль ``cbrf``.
    Модуль ``cbrf`` предоставляет:
    - Курсы валют ЦБ РФ (USD, EUR, CNY и др.)
    - Ключевую ставку
    - Конвертацию валют
    - Сравнение курсов
    - Справочник валют по странам-партнёрам
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="bacen",
    description=(
        "⚠️ DEPRECATED: Legacy-слой BCB (Центральный банк Бразилии). "
        "Для данных ЦБ РФ используйте модуль 'cbrf'. "
        "Макроэкономические показатели Бразилии: ставки, инфляция, курс, ВВП."
    ),
    version="0.1.0-deprecated",
    api_base="https://api.bcb.gov.br/dados/serie/bcdata.sgs",
    requires_auth=False,
    tags=[
        "устаревший",
        "бразилия-legacy",
        "экономика",
        "juros",
        "inflacao",
        "cambio",
        "pib",
        "selic",
    ],
)
