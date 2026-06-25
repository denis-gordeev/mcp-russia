"""ЦИК РФ — данные Центральной избирательной комиссии Российской Федерации."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="cekrf",
    opisanie=(
        "Данные ЦИК РФ: выборы, кандидаты, референдумы, "
        "результаты голосования, избирательные округа"
    ),
    versiya="0.2.0",
    baza_api="https://vybory.izbirkom.ru",
    trebuet_autentifikatsii=False,
    tegi=[
        "выборы",
        "кандидаты",
        "референдум",
        "цик-рф",
        "голосование",
        "избирательные-округа",
    ],
)
