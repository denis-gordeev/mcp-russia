"""Минздрав РФ — данные Министерства здравоохранения и медицинских источников РФ."""

from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta

FEATURE_META = FeatureMeta(
    name="minzdrav",
    description=(
        "Данные здравоохранения РФ: медицинские организации, врачи, показатели здоровья, "
        "заболеваемость, ресурсы Минздрава, Росздравнадзора"
    ),
    version="0.2.0",
    api_base="https://minzdrav.gov.ru",
    requires_auth=False,
    tags=["здравоохранение", "медицина", "минздрав", "заболеваемость", "больницы"],
)
