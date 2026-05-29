"""⚠️ DEPRECATED — Legacy-слой TCE-TO внутри mcp-russia — Tribunal de Contas do Tocantins (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-TO.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_to",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-TO внутри mcp-russia: "
        "Процессы, повестки и поиск персон "
        "в API e-Contas Tribunal de Contas do Tocantins. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://api.tceto.tc.br/econtas/api",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "to", "processos", "pautas", "бразилия-legacy"],
)
