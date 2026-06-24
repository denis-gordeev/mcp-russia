"""ЦИК РФ — данные Центральной избирательной комиссии Российской Федерации."""

from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta

FEATURE_META = FeatureMeta(
    name="cekrf",
    description=(
        "Данные ЦИК РФ: выборы, кандидаты, референдумы, "
        "результаты голосования, избирательные округа"
    ),
    version="0.2.0",
    api_base="https://vybory.izbirkom.ru",
    requires_auth=False,
    tags=[
        "выборы",
        "кандидаты",
        "референдум",
        "цик-рф",
        "голосование",
        "избирательные-округа",
    ],
)
