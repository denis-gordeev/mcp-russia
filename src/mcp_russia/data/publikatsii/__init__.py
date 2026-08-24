"""Официальные публикации РФ — нормативные акты и публикации на pravo.gov.ru."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="publikatsii",
    opisanie=(
        "Официальные публикации Российской Федерации: федеральные законы, "
        "указы Президента, постановления Правительства, нормативные акты, "
        "официальные публикации в Российской газете и на портале pravo.gov.ru"
    ),
    versiya="0.2.0",
    baza_api="https://pravo.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=[
        "законодательство",
        "нормативные-акты",
        "законы",
        "указы",
        "постановления",
        "публикации",
    ],
)
