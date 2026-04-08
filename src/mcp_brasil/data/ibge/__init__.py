"""Legacy-слой IBGE внутри mcp-russia — Instituto Brasileiro de Geografia
e Estatística (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ibge",
    description=(
        "Legacy-слой IBGE внутри mcp-russia: "
        "данные IBGE: штаты, муниципалитеты, регионы, имена и статистические агрегаты Бразилии"
    ),
    version="0.1.0",
    api_base="https://servicodados.ibge.gov.br/api",
    requires_auth=False,
    tags=["geodados", "censo", "indicadores", "localidades"],
)
