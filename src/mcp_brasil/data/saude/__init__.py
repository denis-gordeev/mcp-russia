"""Legacy feature Saúde — переходный слой CNES/DataSUS внутри mcp-russia."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="saude",
    description=(
        "Legacy-слой CNES/DataSUS внутри mcp-russia: учреждения, "
        "медперсонал, типы организаций и больничные койки в бразильском контуре."
    ),
    version="0.1.0",
    api_base="https://apidadosabertos.saude.gov.br/cnes",
    requires_auth=False,
    tags=["saude", "sus", "cnes", "hospitais", "leitos"],
)
