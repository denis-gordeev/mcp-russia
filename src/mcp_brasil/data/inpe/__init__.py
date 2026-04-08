"""Legacy-слой INPE внутри mcp-russia — Instituto Nacional de Pesquisas
Espaciais (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="inpe",
    description=(
        "Legacy-слой INPE внутри mcp-russia: "
        "Национальный институт космических исследований Бразилии: очаги пожаров, "
        "оповещения о вырубке DETER, исторические данные PRODES и спутники."
    ),
    version="0.1.0",
    api_base="https://terrabrasilis.dpi.inpe.br",
    requires_auth=False,
    tags=["queimadas", "desmatamento", "amazonia", "meio-ambiente", "inpe"],
)
