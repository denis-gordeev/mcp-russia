"""Официальные публикации РФ — нормативные акты и публикации на pravo.gov.ru."""

from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta

FEATURE_META = FeatureMeta(
    name="publikatsii",
    description=(
        "Официальные публикации Российской Федерации: федеральные законы, "
        "указы Президента, постановления Правительства, нормативные акты, "
        "официальные публикации в Российская газете и на портале pravo.gov.ru"
    ),
    version="0.2.0",
    api_base="https://pravo.gov.ru",
    requires_auth=False,
    tags=[
        "законодательство",
        "нормативные-акты",
        "законы",
        "указы",
        "постановления",
        "публикации",
    ],
)
