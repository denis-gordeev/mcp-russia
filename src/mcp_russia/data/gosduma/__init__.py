"""Госдума — данные Государственной Думы Федерального Собрания РФ."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="gosduma",
    description=(
        "Данные Государственной Думы: депутаты, законопроекты, пленарные заседания, "
        "голосования, комитеты, фракции"
    ),
    version="0.2.0",
    api_base="https://api.duma.gov.ru",
    requires_auth=False,
    auth_env_var="MCP_RUSSIA_DUMA_API_TOKEN",
    tags=["госдума", "депутаты", "законопроекты", "парламент", "голосования"],
)
