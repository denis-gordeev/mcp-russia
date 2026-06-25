"""Росреестр — данные Федеральной службы государственной регистрации, кадастра и картографии."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rosreestr",
    opisanie=(
        "Данные Росреестра: кадастровая стоимость, объекты недвижимости, "
        "ЕГРН, земельные участки, здания, помещения, границы территорий"
    ),
    versiya="0.2.0",
    baza_api="https://pkk.rosreestr.ru",
    trebuet_autentifikatsii=False,
    tegi=["росреестр", "кадастр", "недвижимость", "егрн", "земля"],
)
