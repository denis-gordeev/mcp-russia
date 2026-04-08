"""Legacy-слой TCU внутри mcp-russia — Tribunal de Contas da União (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tcu",
    description=(
        "Legacy-слой TCU внутри mcp-russia: "
        "Tribunal de Contas da União: решения, недопущенные поставщики, "
        "лишённые права занимать публичные должности, консолидированные сертификаты (APF), "
        "расчёт задолженности, запросы Конгресса, контракты TCU и CADIRREG."
    ),
    version="0.1.0",
    api_base="https://dados-abertos.apps.tcu.gov.br",
    requires_auth=False,
    tags=["tcu", "acordaos", "inidoneos", "inabilitados", "certidoes", "contratos"],
)
