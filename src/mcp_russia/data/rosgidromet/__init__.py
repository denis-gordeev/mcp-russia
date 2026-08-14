"""Росгидромет — погодные данные по России через Open-Meteo."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rosgidromet",
    opisanie=(
        "Погодные и климатические данные по России через Open-Meteo: "
        "погода, прогноз, качество воздуха, гидрология "
        "(Росгидромет — профиль ведомства)"
    ),
    versiya="0.2.0",
    baza_api="https://api.open-meteo.com/v1/forecast",
    trebuet_autentifikatsii=False,
    tegi=["погода", "климат", "экология", "гидрометеорология", "open-meteo", "качество-воздуха"],
)
