"""Legacy-слой TCE-PE внутри mcp-russia — Tribunal de Contas de
Pernambuco (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_pe",
    description=(
        "Legacy-слой TCE-PE внутри mcp-russia: "
        "Тендеры, контракты, расходы и поставщики "
        "муниципалитетов и органов штата Пернамбуку через API SAGRES/LICON."
    ),
    version="0.1.0",
    api_base="https://sistemas.tce.pe.gov.br/DadosAbertos",
    requires_auth=False,
    tags=["tce", "pe", "licitacoes", "contratos", "despesas", "fornecedores"],
)
