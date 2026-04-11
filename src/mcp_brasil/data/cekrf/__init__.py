"""ЦИК РФ — данные Центральной избирательной комиссии Российской Федерации."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="cekrf",
    description=(
        "Данные ЦИК РФ: выборы, кандидаты, референдумы, "
        "результаты голосования, избирательные округа"
    ),
    version="0.1.0",
    api_base="https://cikrf.ru/api",
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
