"""ЦБ РФ — данные Банка России (ключевая ставка, курсы валют, инфляция)."""

from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta

FEATURE_META = FeatureMeta(
    name="cbrf",
    description=(
        "Данные Центрального банка РФ: ключевая ставка, официальные курсы валют, "
        "инфляция, золотовалютые резервы, статистика"
    ),
    version="0.1.0",
    api_base="https://www.cbr-xml-daily.ru/daily_json.js",
    requires_auth=False,
    tags=["экономика", "ключевая-ставка", "курс-валют", "инфляция", "цб-рф"],
)
