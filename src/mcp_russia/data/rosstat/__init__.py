"""Росстат — данные Федеральной службы государственной статистики."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rosstat",
    description=(
        "Данные Росстата: демография, инфляция (ИПЦ), промышленное производство, "
        "ВРП регионов, потребительские цены"
    ),
    version="0.2.0",
    api_base="https://rosstat.gov.ru",
    requires_auth=False,
    tags=["статистика", "демография", "инфляция", "ВРП", "росстат"],
)
