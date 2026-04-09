"""Госдума — данные Государственной Думы Федерального Собрания РФ."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="gosduma",
    description=(
        "Данные Государственной Думы: депутаты, законопроекты, пленарные заседания, "
        "голосования, комитеты, фракции"
    ),
    version="0.1.0",
    api_base="https://download.data.duma.gov.ru",
    requires_auth=False,
    tags=["госдума", "депутаты", "законопроекты", "парламент", "голосования"],
)
