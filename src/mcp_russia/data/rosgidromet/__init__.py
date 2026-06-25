"""Росгидромет — данные Федеральной службы по гидрометеорологии и мониторингу окружающей среды."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rosgidromet",
    opisanie=(
        "Данные Росгидромета: погода, климат, качество воздуха, загрязнение окружающей среды, "
        "спутниковый мониторинг, гидрологические данные"
    ),
    versiya="0.2.0",
    baza_api="https://api.open-meteo.com/v1/forecast",
    trebuet_autentifikatsii=False,
    tegi=["погода", "климат", "экология", "гидрометеорология", "росгидромет", "спутники"],
)
