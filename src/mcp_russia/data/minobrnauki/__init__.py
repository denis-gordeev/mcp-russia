"""Минобрнауки/Рособрнадзор — данные об образовании и науке в РФ."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="minobrnauki",
    opisanie=(
        "Данные Минобрнауки и Рособрнадзора: вузы, аккредитация, лицензии, "
        "рейтинги, гранты, контроль деятельности, эксперты"
    ),
    versiya="0.3.0",
    baza_api="https://obrnadzor.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=["минобрнауки", "рособрнадзор", "образование", "вузы", "лицензии"],
)
