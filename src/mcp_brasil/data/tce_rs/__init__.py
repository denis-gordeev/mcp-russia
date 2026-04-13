"""⚠️ DEPRECATED — Legacy-слой TCE-RS внутри mcp-russia — Tribunal de Contas do Rio Grande do Sul (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCE-RS.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rs",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCE-RS внутри mcp-russia: "
        "Индексы образования и здравоохранения, фискальное управление (LRF) "
        "и каталог данных муниципалитетов Риу-Гранди-ду-Сул "
        "через портал CKAN TCE-RS. "
        "Для российских аналогов используйте модули rosstat и zakupki."
    ),
    version="0.1.0-deprecated",
    api_base="https://dados.tce.rs.gov.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tce", "rs", "educacao", "saude", "gestao-fiscal", "ckan", "бразилия-legacy"],
)
