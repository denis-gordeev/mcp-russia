"""Legacy-слой IBGE внутри mcp-russia — Instituto Brasileiro de Geografia e Estatística.

.. deprecated::
    Этот модуль содержит только данные статистического института Бразилии
    для обратной совместимости.
    Для работы с данными Росстата используйте модуль ``rosstat``.
    Модуль ``rosstat`` предоставляет:
    - Справочник субъектов РФ
    - Федеральные округа
    - Основные показатели (население, ВРП, ИПЦ, безработица)
    - Интеграцию с ЕМИСС (fedstat.ru)
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ibge",
    description=(
        "⚠️ DEPRECATED: Legacy-слой IBGE (статистический институт Бразилии). "
        "Для данных Росстата используйте модуль 'rosstat'. "
        "Данные Бразилии: штаты, муниципалитеты, регионы, имена, статистические агрегаты."
    ),
    version="0.1.0-deprecated",
    api_base="https://servicodados.ibge.gov.br/api",
    requires_auth=False,
    tags=[
        "устаревший",
        "бразилия-legacy",
        "geodados",
        "censo",
        "indicadores",
        "localidades",
    ],
)
