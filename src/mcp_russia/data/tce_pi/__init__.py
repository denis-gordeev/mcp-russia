"""⚠️ DEPRECATED — Legacy-слой TCE-PI внутри mcp-russia — Tribunal de Contas do Piauí (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-PI.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_pi",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-PI внутри mcp-russia: "
        "Префектуры, расходы, доходы и органы штата Пиауи "
        "через API портала гражданского участия TCE-PI. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://sistemas.tce.pi.gov.br/api/portaldacidadania",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "tce",
        "pi",
        "prefeituras",
        "despesas",
        "receitas",
        "orgaos",
        "бразилия-legacy",
    ],
    enabled=False,
)
