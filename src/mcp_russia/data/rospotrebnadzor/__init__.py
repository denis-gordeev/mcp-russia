"""Роспотребнадзор — данные Федеральной службы по надзору в сфере защиты
прав потребителей и благополучия человека."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rospotrebnadzor",
    description=(
        "Данные Роспотребнадзора: санитарно-эпидемиологический надзор, "
        "защита прав потребителей, проверки объектов, нарушения, показатели безопасности"
    ),
    version="0.1.0",
    api_base="https://rospotrebnadzor.ru",
    requires_auth=False,
    tags=["роспотребнадзор", "санитарный-надзор", "потребители", "проверки", "санпин"],
)
