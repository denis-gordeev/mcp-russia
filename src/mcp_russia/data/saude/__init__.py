"""⚠️ DEPRECATED — Legacy feature Saúde — переходный слой CNES/DataSUS внутри mcp-russia.

.. deprecated::
    Используйте модуль ``mcp_russia.data.minzdrav`` (Минздрав РФ) для российских медицинских данных.
    Данный модуль сохраняет обратную совместимость для бразильских DataSUS/CNES интеграций.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="saude",
    description=(
        "⚠️ DEPRECATED — Legacy-слой CNES/DataSUS внутри mcp-russia: учреждения, "
        "медперсонал, типы организаций и больничные койки в бразильском контуре. "
        "Для российских медицинских данных используйте модуль minzdrav (Минздрав РФ)."
    ),
    version="0.1.0-deprecated",
    api_base="https://apidadosabertos.saude.gov.br/cnes",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "saude", "sus", "cnes", "hospitais", "leitos", "бразилия-legacy"],
    enabled=False,
)
