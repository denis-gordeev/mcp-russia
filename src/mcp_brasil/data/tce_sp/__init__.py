"""Legacy-слой TCE-SP внутри mcp-russia — Tribunal de Contas do Estado
de São Paulo (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_sp",
    description=(
        "Legacy-слой TCE-SP внутри mcp-russia: "
        "Расходы и доходы 645 муниципалитетов штата Сан-Паулу, "
        "с ежемесячными данными с 2014 года по текущий период."
    ),
    version="0.1.0",
    api_base="https://transparencia.tce.sp.gov.br/api",
    requires_auth=False,
    tags=["tce", "sp", "despesas", "receitas", "municipios"],
)
