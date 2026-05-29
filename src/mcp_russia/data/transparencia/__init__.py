"""⚠️ DEPRECATED — Legacy-слой Transparencia внутри mcp-russia — Portal da Transparencia (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.zakupki`` (ЕИС) и будущий модуль Минфина РФ
    для российских данных о госрасходах и прозрачности.
    Данный модуль сохраняет обратную совместимость для бразильских данных Portal da Transparencia.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="transparencia",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Transparencia внутри mcp-russia: "
        "Портал прозрачности Бразилии: контракты, расходы, служащие, тендеры, санкции. "
        "Для российских данных о госрасходах используйте модуль zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://api.portaldatransparencia.gov.br/api-de-dados",
    requires_auth=True,
    auth_env_var="TRANSPARENCIA_API_KEY",
    tags=[
        "⚠️ DEPRECATED",
        "правительство",
        "контракты",
        "расходы",
        "служащие",
        "тендеры",
        "санкции",
        "бразилия-legacy",
    ],
)
