"""Росгидромет — данные Федеральной службы по гидрометеорологии и мониторингу окружающей среды."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rosgidromet",
    description=(
        "Данные Росгидромета: погода, климат, качество воздуха, загрязнение окружающей среды, "
        "спутниковый мониторинг, гидрологические данные"
    ),
    version="0.1.0",
    api_base="https://meteorf.ru",
    requires_auth=False,
    tags=["погода", "климат", "экология", "гидрометеорология", "росгидромет", "спутники"],
)
