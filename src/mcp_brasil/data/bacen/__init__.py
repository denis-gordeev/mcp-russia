"""Legacy feature Bacen — переходный слой данных Banco Central do Brasil."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="bacen",
    description=(
        "Legacy-слой BCB внутри mcp-russia: "
        "ставки, инфляция, курс, активность и другие макроиндикаторы Бразилии"
    ),
    version="0.1.0",
    api_base="https://api.bcb.gov.br/dados/serie/bcdata.sgs",
    requires_auth=False,
    tags=["economia", "juros", "inflacao", "cambio", "pib", "selic"],
)
