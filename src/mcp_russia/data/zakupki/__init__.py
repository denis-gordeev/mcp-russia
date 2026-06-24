"""ЕИС (zakupki) — данные Единой информационной системы в сфере закупок."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    name="zakupki",
    description=(
        "Данные ЕИС закупок: планы-графики, реестр контрактов, поставщики, "
        "заказчики, способы определения поставщиков, мониторинг закупок"
    ),
    version="0.2.0",
    api_base="https://zakupki.gov.ru",
    requires_auth=False,
    auth_env_var="MCP_RUSSIA_ZAKUPKI_API_TOKEN",
    tags=["закупки", "44-фз", "223-фз", "контракты", "тендеры", "еис"],
)
