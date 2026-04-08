"""Legacy-слой TCE-SC внутри mcp-russia — Tribunal de Contas de Santa
Catarina (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_sc",
    description=(
        "Legacy-слой TCE-SC внутри mcp-russia: "
        "Муниципалитеты и управляющие единицы Санта-Катарины "
        "через портал прозрачности TCE-SC."
    ),
    version="0.1.0",
    api_base="https://servicos.tcesc.tc.br/endpoints-portal-transparencia",
    requires_auth=False,
    tags=["tce", "sc", "municipios", "unidades-gestoras"],
)
