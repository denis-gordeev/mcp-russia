"""⚠️ DEPRECATED — Legacy-слой TCE-SP внутри mcp-russia — Tribunal de Contas do Estado de São Paulo (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-SP.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_sp",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-SP внутри mcp-russia: "
        "Расходы и доходы 645 муниципалитетов штата Сан-Паулу, "
        "с ежемесячными данными с 2014 года по текущий период. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://transparencia.tce.sp.gov.br/api",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "sp", "despesas", "receitas", "municipios", "бразилия-legacy"],
)
