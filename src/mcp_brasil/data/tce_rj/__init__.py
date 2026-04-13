"""⚠️ DEPRECATED — Legacy-слой TCE-RJ внутри mcp-russia — Tribunal de Contas do Estado do Rio de Janeiro (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-RJ.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rj",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-RJ внутри mcp-russia: "
        "Тендеры, контракты, прямые закупки, остановленные стройки, "
        "штрафы, отчёты о расходах и публичные концессии штата "
        "и муниципалитетов Рио-де-Жанейро. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://dados.tcerj.tc.br/api/v1",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "rj", "licitacoes", "contratos", "obras", "penalidades", "бразилия-legacy"],
)
