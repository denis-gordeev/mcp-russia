"""Legacy-слой Camara внутри mcp-russia — Câmara dos Deputados (compatibility layer, legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="camara",
    description=(
        "Legacy-слой Camara внутри mcp-russia: "
        "Палата депутатов Бразилии: депутаты, законопроекты, голосования, расходы, комиссии"
    ),
    version="0.1.0",
    api_base="https://dadosabertos.camara.leg.br/api/v2",
    requires_auth=False,
    tags=["законодательный", "депутаты", "законопроекты", "голосования", "расходы", "комиссии"],
)
