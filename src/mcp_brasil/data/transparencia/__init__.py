"""Legacy-слой Transparencia внутри mcp-russia — Portal da Transparencia (compatibility layer, legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="transparencia",
    description=(
        "Legacy-слой Transparencia внутри mcp-russia: "
        "Портал прозрачности Бразилии: контракты, расходы, служащие, тендеры, санкции"
    ),
    version="0.1.0",
    api_base="https://api.portaldatransparencia.gov.br/api-de-dados",
    requires_auth=True,
    auth_env_var="TRANSPARENCIA_API_KEY",
    tags=["правительство", "контракты", "расходы", "служащие", "тендеры", "санкции"],
)
