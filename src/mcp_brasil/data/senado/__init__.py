"""Legacy-слой Senado внутри mcp-russia — Senado Federal.

.. deprecated::
    Этот модуль содержит только данные Федерального сената Бразилии для обратной совместимости.
    Для работы с данными Совета Федерации используйте модуль ``gosduma``.
    Модуль ``gosduma`` предоставляет данные российского парламента, включая Совет Федерации.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="senado",
    description=(
        "⚠️ DEPRECATED: Legacy-слой Senado Federal (Федеральный сенат Бразилии). "
        "Для данных Совета Федерации используйте модуль 'gosduma'. "
        "Данные Федерального сената Бразилии: сенаторы, материалы, голосования, комиссии, повестка."
    ),
    version="0.1.0-deprecated",
    api_base="https://legis.senado.leg.br/dadosabertos",
    requires_auth=False,
    tags=[
        "устаревший",
        "бразилия-legacy",
        "законодательный",
        "сенаторы",
        "материалы",
        "голосования",
        "комиссии",
        "повестка",
    ],
)
