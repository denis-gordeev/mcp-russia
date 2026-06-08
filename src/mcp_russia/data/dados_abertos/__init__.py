"""⚠️ DEPRECATED — Legacy-слой Dados Abertos внутри mcp-russia — каталог данных федерального правительства Бразилии (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и будущий модуль открытых данных РФ
    для российских статистических и открытых данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных Dados Abertos.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="dados_abertos",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Dados Abertos внутри mcp-russia: "
        "Портал открытых данных (dados.gov.br): каталог открытых данных "
        "федерального правительства Бразилии, публикующие организации и доступные ресурсы. "
        "Для российских открытых данных используйте модуль rosstat."
    ),
    version="0.1.0-deprecated",
    api_base="https://dados.gov.br/dados/api/publico",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "открытые-данные",
        "наборы-данных",
        "правительство",
        "прозрачность",
        "бразилия-legacy",
    ],
    enabled=False,
)
