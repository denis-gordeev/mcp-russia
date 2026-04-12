"""Кадр Арбитраж — данные Картотеки арбитражных дел."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="kad_arbitrazh",
    description=(
        "Данные Картотеки арбитражных дел (КАД): судебные дела, решения, определения, "
        "постановления арбитражных судов РФ, судьи, участники дел"
    ),
    version="0.1.0",
    api_base="https://kad.arbitr.ru",
    requires_auth=False,
    tags=["арбитраж", "суд", "судебные-дела", "картотека", "кад"],
)
