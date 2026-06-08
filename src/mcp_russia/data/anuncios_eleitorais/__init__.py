"""⚠️ DEPRECATED — Legacy-слой Anuncios Eleitorais внутри mcp-russia — Meta Ad Library для политической рекламы (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.cekrf`` (ЦИК РФ) для российских избирательных данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных Meta Ad Library.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="anuncios_eleitorais",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Meta Ad Library внутри mcp-russia: "
        "Поиск и анализ политической и общественно значимой рекламы, показанной в Бразилии. "
        "Для российских избирательных данных используйте модуль cekrf."
    ),
    version="0.1.0-deprecated",
    api_base="https://graph.facebook.com/v25.0",
    requires_auth=True,
    auth_env_var="META_ACCESS_TOKEN",
    tags=[
        "⚠️ DEPRECATED",
        "выборы",
        "политика",
        "реклама",
        "meta",
        "facebook",
        "instagram",
        "прозрачность",
        "бразилия-legacy",
    ],
    enabled=False,
)
