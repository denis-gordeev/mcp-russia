"""⚠️ DEPRECATED — Legacy-слой TCE-PE внутри mcp-russia — Tribunal de Contas de Pernambuco (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-PE.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_pe",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-PE внутри mcp-russia: "
        "Тендеры, контракты, расходы и поставщики "
        "муниципалитетов и органов штата Пернамбуку через API SAGRES/LICON. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://sistemas.tce.pe.gov.br/DadosAbertos",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "tce",
        "pe",
        "licitacoes",
        "contratos",
        "despesas",
        "fornecedores",
        "бразилия-legacy",
    ],
    enabled=False,
)
