"""Legacy-слой Camara внутри mcp-russia — Câmara dos Deputados.

.. deprecated::
    Этот модуль содержит только данные Палаты депутатов Бразилии для обратной совместимости.
    Для работы с данными Государственной Думы используйте модуль ``gosduma``.
    Модуль ``gosduma`` предоставляет:
    - Депутаты Госдумы
    - Фракции
    - Комитеты
    - Созывы
    - Законопроекты
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="camara",
    description=(
        "⚠️ DEPRECATED: Legacy-слой Câmara dos Deputados (Палата депутатов Бразилии). "
        "Для данных Госдумы используйте модуль 'gosduma'. "
        "Данные Палаты депутатов Бразилии: депутаты, законопроекты, голосования, расходы, комиссии."
    ),
    version="0.1.0-deprecated",
    api_base="https://dadosabertos.camara.leg.br/api/v2",
    requires_auth=False,
    tags=[
        "устаревший",
        "бразилия-legacy",
        "законодательный",
        "депутаты",
        "законопроекты",
        "голосования",
        "расходы",
        "комиссии",
    ],
)
