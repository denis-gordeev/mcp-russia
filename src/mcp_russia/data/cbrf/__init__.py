"""ЦБ РФ — данные Банка России (ключевая ставка, курсы валют, инфляция)."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="cbrf",
    opisanie=(
        "Данные Центрального банка РФ: ключевая ставка, официальные курсы валют, "
        "инфляция, золотовалютные резервы, статистика"
    ),
    versiya="0.1.0",
    baza_api="https://www.cbr-xml-daily.ru/daily_json.js",
    trebuet_autentifikatsii=False,
    tegi=["экономика", "ключевая-ставка", "курс-валют", "инфляция", "цб-рф"],
)
