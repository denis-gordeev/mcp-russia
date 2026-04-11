"""Legacy-слой Dados Abertos внутри mcp-russia — каталог данных
федерального правительства Бразилии (compatibility layer, legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="dados_abertos",
    description=(
        "Legacy-слой Dados Abertos внутри mcp-russia: "
        "Портал открытых данных (dados.gov.br): каталог открытых данных "
        "федерального правительства Бразилии, публикующие организации и доступные ресурсы."
    ),
    version="0.1.0",
    api_base="https://dados.gov.br/dados/api/publico",
    requires_auth=False,
    tags=["открытые-данные", "наборы-данных", "правительство", "прозрачность"],
)
