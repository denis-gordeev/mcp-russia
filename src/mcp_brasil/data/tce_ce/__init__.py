"""Legacy-слой TCE-CE внутри mcp-russia — Tribunal de Contas do Estado
do Ceará (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_ce",
    description=(
        "Legacy-слой TCE-CE внутри mcp-russia: "
        "Тендеры, контракты и обязательства муниципалитетов Сеары "
        "через API данных SIM (муниципальная информационная система) TCE-CE."
    ),
    version="0.1.0",
    api_base="https://api-dados-abertos.tce.ce.gov.br",
    requires_auth=False,
    tags=["tce", "ce", "licitacoes", "contratos", "empenhos"],
)
