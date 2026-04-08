"""Legacy-слой TCE-RN внутри mcp-russia — Tribunal de Contas do Rio
Grande do Norte (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rn",
    description=(
        "Legacy-слой TCE-RN внутри mcp-russia: "
        "Подконтрольные органы, тендеры, контракты, расходы и доходы "
        "Риу-Гранди-ду-Норти через API SIAI TCE-RN."
    ),
    version="0.1.0",
    api_base="https://apidadosabertos.tce.rn.gov.br",
    requires_auth=False,
    tags=["tce", "rn", "licitacoes", "contratos", "despesas", "receitas"],
)
