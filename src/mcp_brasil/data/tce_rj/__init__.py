"""Legacy-слой TCE-RJ внутри mcp-russia — Tribunal de Contas do Estado
do Rio de Janeiro (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rj",
    description=(
        "Legacy-слой TCE-RJ внутри mcp-russia: "
        "Тендеры, контракты, прямые закупки, остановленные стройки, "
        "штрафы, отчёты о расходах и публичные концессии штата "
        "и муниципалитетов Рио-де-Жанейро."
    ),
    version="0.1.0",
    api_base="https://dados.tcerj.tc.br/api/v1",
    requires_auth=False,
    tags=["tce", "rj", "licitacoes", "contratos", "obras", "penalidades"],
)
