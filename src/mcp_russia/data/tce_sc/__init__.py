"""⚠️ DEPRECATED — Legacy-слой TCE-SC внутри mcp-russia — Tribunal de Contas de Santa Catarina (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-SC.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_sc",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-SC внутри mcp-russia: "
        "Муниципалитеты и управляющие единицы Санта-Катарины "
        "через портал прозрачности TCE-SC. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://servicos.tcesc.tc.br/endpoints-portal-transparencia",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "sc", "municipios", "unidades-gestoras", "бразилия-legacy"],
)
