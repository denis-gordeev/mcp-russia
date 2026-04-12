"""ЕИС (zakupki) — данные Единой информационной системы в сфере закупок."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="zakupki",
    description=(
        "Данные ЕИС закуровок: планы-графики, реестр контрактов, поставщики, "
        "заказчики, способы определения поставщиков, мониторинг закупок"
    ),
    version="0.1.0",
    api_base="https://zakupki.gov.ru",
    requires_auth=False,
    tags=["закупки", "44-фз", "223-фз", "контракты", "тендеры", "еис"],
)
