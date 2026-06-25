"""Роспотребнадзор — данные Федеральной службы по надзору в сфере защиты
прав потребителей и благополучия человека."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rospotrebnadzor",
    opisanie=(
        "Данные Роспотребнадзора: санитарно-эпидемиологический надзор, "
        "защита прав потребителей, проверки объектов, нарушения, показатели безопасности"
    ),
    versiya="0.2.0",
    baza_api="https://proverki.rospotrebnadzor.ru",
    trebuet_autentifikatsii=False,
    tegi=["роспотребнадзор", "санитарный-надзор", "потребители", "проверки", "санпин"],
)
