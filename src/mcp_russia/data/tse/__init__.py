"""⚠️ DEPRECATED — Legacy-слой TSE внутри mcp-russia — Tribunal Superior Eleitoral (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.cekrf`` (ЦИК РФ — vybory.izbirkom.ru)
    для российских избирательных данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных TSE.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tse",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TSE внутри mcp-russia: "
        "Высший избирательный суд Бразилии: выборы, кандидаты, "
        "отчёты о расходах, избирательные должности. "
        "Для российских избирательных данных используйте модуль cekrf."
    ),
    version="0.1.0-deprecated",
    api_base="https://divulgacandcontas.tse.jus.br/divulga/rest/v1",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "избирательный",
        "кандидаты",
        "выборы",
        "tse",
        "отчёты-о-расходах",
        "бразилия-legacy",
    ],
)
