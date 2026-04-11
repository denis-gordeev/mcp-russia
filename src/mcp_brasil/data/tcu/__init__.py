"""Legacy-слой TCU внутри mcp-russia — Tribunal de Contas da Uniao (compatibility layer, legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tcu",
    description=(
        "Legacy-слой TCU внутри mcp-russia: "
        "Tribunal de Contas da Uniao: решения, недопущенные поставщики, "
        "лишённые права занимать публичные должности, консолидированные сертификаты (APF), "
        "расчёт задолженности, запросы Конгресса, контракты TCU и CADIRREG."
    ),
    version="0.1.0",
    api_base="https://dados-abertos.apps.tcu.gov.br",
    requires_auth=False,
    tags=["tcu", "решения", "недопущенные", "лишённые-прав", "сертификаты", "контракты"],
)
