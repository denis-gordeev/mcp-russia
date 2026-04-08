"""Legacy-слой Redator внутри mcp-russia — geração de documentos oficiais
brasileiros (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="redator",
    description=(
        "Legacy-слой Redator внутри mcp-russia: "
        "Официальная переписка Бразилии: ofício, despacho, portaria, parecer, nota técnica "
        "на основе Manual de Redação da Presidência da República (бразильский стандарт)"
    ),
    version="0.1.0",
    requires_auth=False,
    tags=["documentos", "redacao-oficial", "govtech"],
)
