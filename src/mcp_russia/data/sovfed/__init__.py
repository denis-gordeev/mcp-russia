"""Совет Федерации РФ — данные верхней палаты Федерального Собрания Российской Федерации."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="sovfed",
    opisanie=(
        "Данные Совета Федерации РФ: сенаторы, комитеты и комиссии, "
        "законопроекты, рассмотренные палатой, заседания и повестка, "
        "региональное представительство"
    ),
    versiya="0.2.0",
    baza_api="https://sovfed.ru",
    trebuet_autentifikatsii=False,
    tegi=["совет-федерации", "сенаторы", "законодательство", "комитеты", "регионы"],
)
