"""Роспотребнадзор — данные Федеральной службы по надзору в сфере защиты
прав потребителей и благополучия человека."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    name="rospotrebnadzor",
    description=(
        "Данные Роспотребнадзора: санитарно-эпидемиологический надзор, "
        "защита прав потребителей, проверки объектов, нарушения, показатели безопасности"
    ),
    version="0.2.0",
    api_base="https://proverki.rospotrebnadzor.ru",
    requires_auth=False,
    tags=["роспотребнадзор", "санитарный-надзор", "потребители", "проверки", "санпин"],
)
