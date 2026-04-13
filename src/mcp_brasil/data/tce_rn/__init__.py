"""⚠️ DEPRECATED — Legacy-слой TCE-RN внутри mcp-russia — Tribunal de Contas do Rio Grande do Norte (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-RN.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rn",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-RN внутри mcp-russia: "
        "Подконтрольные органы, тендеры, контракты, расходы и доходы "
        "Риу-Гранди-ду-Норти через API SIAI TCE-RN. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://apidadosabertos.tce.rn.gov.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "rn", "licitacoes", "contratos", "despesas", "receitas", "бразилия-legacy"],
)
