"""Legacy-слой TSE внутри mcp-russia — Tribunal Superior Eleitoral (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tse",
    description=(
        "Legacy-слой TSE внутри mcp-russia: "
        "Высший избирательный суд Бразилии: выборы, кандидаты, "
        "отчёты о расходах, избирательные должности"
    ),
    version="0.1.0",
    api_base="https://divulgacandcontas.tse.jus.br/divulga/rest/v1",
    requires_auth=False,
    tags=["eleitoral", "candidatos", "eleicoes", "tse", "prestacao-contas"],
)
