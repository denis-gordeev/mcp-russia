"""Legacy-слой Camara внутри mcp-russia — Câmara dos Deputados (compatibility layer)."""

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
    tags=["legislativo", "deputados", "proposições", "votações", "despesas", "comissões"],
)
