"""Legacy-слой Senado внутри mcp-russia — Senado Federal (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="senado",
    description=(
        "Legacy-слой Senado внутри mcp-russia: "
        "Федеральный сенат Бразилии: сенаторы, материалы, голосования, комиссии, повестка"
    ),
    version="0.1.0",
    api_base="https://legis.senado.leg.br/dadosabertos",
    requires_auth=False,
    tags=["legislativo", "senadores", "matérias", "votações", "comissões", "agenda"],
)
