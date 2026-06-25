"""Минобрнауки — данные Министерства науки и высшего образования РФ."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="minobrnauki",
    opisanie=(
        "Данные Минобрнауки России: вузы, научные исследования, "
        "образовательные программы, рейтинги, гранты, аспирантура"
    ),
    versiya="0.2.0",
    baza_api="https://obrnadzor.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=["минобрнауки", "образование", "наука", "вузы", "исследования"],
)
