"""⚠️ DEPRECATED — Legacy-слой Tabua Mares внутри mcp-russia — данные о приливах для бразильского побережья (compatibility layer, legacy).

.. deprecated::
    Используйте будущий модуль Росгидромета для российских гидрометеорологических данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных Tabua Mares.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tabua_mares",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Tabua Mares внутри mcp-russia: "
        "Прогноз приливов для портов бразильского побережья. "
        "Для российских гидрометеорологических данных используйте будущий модуль Росгидромета."
    ),
    version="0.1.0-deprecated",
    api_base="https://tabuademares.com/api/v2",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "mares",
        "portos",
        "litoral",
        "navegacao",
        "oceanografia",
        "бразилия-legacy",
    ],
    enabled=False,
)
