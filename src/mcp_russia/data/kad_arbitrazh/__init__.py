"""Кадр Арбитраж — данные Картотеки арбитражных дел."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="kad_arbitrazh",
    opisanie=(
        "Данные Картотеки арбитражных дел (КАД): судебные дела, решения, определения, "
        "постановления арбитражных судов РФ, судьи, участники дел"
    ),
    versiya="0.2.0",
    baza_api="https://kad.arbitr.ru",
    trebuet_autentifikatsii=False,
    tegi=["арбитраж", "суд", "судебные-дела", "картотека", "кад"],
)
