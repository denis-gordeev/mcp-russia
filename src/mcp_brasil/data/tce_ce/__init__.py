"""⚠️ DEPRECATED — Legacy-слой TCE-CE внутри mcp-russia — Tribunal de Contas do Estado do Ceará (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-CE.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_ce",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-CE внутри mcp-russia: "
        "Тендеры, контракты и обязательства муниципалитетов Сеары "
        "через API данных SIM (муниципальная информационная система) TCE-CE. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://api-dados-abertos.tce.ce.gov.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "ce", "licitacoes", "contratos", "empenhos", "бразилия-legacy"],
)
