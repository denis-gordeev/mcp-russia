"""Совместимый слой Meta Ad Library для политической рекламы (legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="anuncios_eleitorais",
    description=(
        "Legacy-слой Meta Ad Library внутри mcp-russia: поиск и анализ политической и "
        "общественно значимой рекламы, показанной в Бразилии."
    ),
    version="0.1.0",
    api_base="https://graph.facebook.com/v25.0",
    requires_auth=True,
    auth_env_var="META_ACCESS_TOKEN",
    tags=["выборы", "политика", "реклама", "meta", "facebook", "instagram", "прозрачность"],
)
