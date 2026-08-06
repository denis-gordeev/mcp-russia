"""Ростехнадзор — Федеральная служба по экологическому, технологическому
и атомному надзору."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rostekhnadzor",
    opisanie=(
        "Данные Ростехнадзора: промышленная безопасность, атомный надзор, "
        "лицензирование, инциденты, радиационная обстановка объектов"
    ),
    versiya="0.1.0",
    baza_api="https://rostechnadzor.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=[
        "промышленная-безопасность",
        "атомный-надзор",
        "лицензии",
        "инциденты",
        "ростехнадзор",
    ],
)
