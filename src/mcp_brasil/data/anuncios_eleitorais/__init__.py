"""Совместимый слой Meta Ad Library для политической рекламы."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="anuncios_eleitorais",
    description=(
        "Переходный слой Meta Ad Library: поиск и анализ политической и "
        "общественно значимой рекламы, показанной в Бразилии."
    ),
    version="0.1.0",
    api_base="https://graph.facebook.com/v25.0",
    requires_auth=True,
    auth_env_var="META_ACCESS_TOKEN",
    tags=["eleicoes", "politica", "anuncios", "meta", "facebook", "instagram", "transparencia"],
)
