"""⚠️ DEPRECATED — Legacy-слой Compras внутри mcp-russia — публичные закупки Бразилии (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.zakupki`` (ЕИС — zakupki.gov.ru) для российских госзакупок.
    Данный модуль сохраняет обратную совместимость для бразильских PNCP/Compras.gov.br интеграций.

Sub-packages:
    - pncp: Portal Nacional de Contratações Públicas (Lei 14.133/2021) — ⚠️ DEPRECATED
    - dadosabertos: Dados Abertos Compras.gov.br (SIASG/ComprasNet legado + nova API) — ⚠️ DEPRECATED
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="compras",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Compras внутри mcp-russia: "
        "Публичные закупки Бразилии: PNCP, Dados Abertos Compras.gov.br (тендеры, контракты, "
        "поставщики, CATMAT, CATSER, аукционы, исследование цен). "
        "Для российских госзакупок используйте модуль zakupki (ЕИС)."
    ),
    version="0.2.0-deprecated",
    api_base="https://pncp.gov.br/api/consulta",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "тендеры",
        "контракты",
        "закупки",
        "pncp",
        "поставщики",
        "catmat",
        "catser",
        "бразилия-legacy",
    ],
)
