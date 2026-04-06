"""Переходный слой с данными о приливах для бразильского побережья."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tabua_mares",
    description=(
        "Переходный data-layer: прогноз приливов для портов бразильского "
        "побережья, сохраненный как legacy-совместимая feature."
    ),
    version="0.1.0",
    api_base="https://tabuademares.com/api/v2",
    requires_auth=False,
    tags=["mares", "portos", "litoral", "navegacao", "oceanografia"],
)
