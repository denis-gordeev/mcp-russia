"""Росреестр — данные Федеральной службы государственной регистрации, кадастра и картографии."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rosreestr",
    description=(
        "Данные Росреестра: кадастровая стоимость, объекты недвижимости, "
        "ЕГРН, земельные участки, здания, помещения, границы территорий"
    ),
    version="0.1.0",
    api_base="https://rosreestr.gov.ru",
    requires_auth=False,
    tags=["росреестр", "кадастр", "недвижимость", "егрн", "земля"],
)
