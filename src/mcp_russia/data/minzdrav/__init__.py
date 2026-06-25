"""Минздрав РФ — данные Министерства здравоохранения и медицинских источников РФ."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="minzdrav",
    opisanie=(
        "Данные здравоохранения РФ: медицинские организации, врачи, показатели здоровья, "
        "заболеваемость, ресурсы Минздрава, Росздравнадзора"
    ),
    versiya="0.2.0",
    baza_api="https://minzdrav.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=["здравоохранение", "медицина", "минздрав", "заболеваемость", "больницы"],
)
