"""Legacy-слой Compras внутри mcp-russia — публичные закупки Бразилии (compatibility layer, legacy).

Sub-packages:
    - pncp: Portal Nacional de Contratações Públicas (Lei 14.133/2021)
    - dadosabertos: Dados Abertos Compras.gov.br (SIASG/ComprasNet legado + nova API)
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="compras",
    description=(
        "Legacy-слой Compras внутри mcp-russia: "
        "Публичные закупки Бразилии: PNCP, Dados Abertos Compras.gov.br (тендеры, контракты, "
        "поставщики, CATMAT, CATSER, аукционы, исследование цен)."
    ),
    version="0.2.0",
    api_base="https://pncp.gov.br/api/consulta",
    requires_auth=False,
    tags=["тендеры", "контракты", "закупки", "pncp", "поставщики", "catmat", "catser"],
)
