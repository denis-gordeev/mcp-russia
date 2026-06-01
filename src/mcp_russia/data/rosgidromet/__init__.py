"""Росгидромет — данные Федеральной службы по гидрометеорологии и мониторингу окружающей среды."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rosgidromet",
    description=(
        "Данные Росгидромета: погода, климат, качество воздуха, загрязнение окружающей среды, "
        "спутниковый мониторинг, гидрологические данные"
    ),
    version="0.2.0",
    api_base="https://api.open-meteo.com/v1/forecast",
    requires_auth=False,
    tags=["погода", "климат", "экология", "гидрометеорология", "росгидромет", "спутники"],
)
