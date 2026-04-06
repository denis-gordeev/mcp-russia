"""Переходный слой TCE-TO внутри публичного контура mcp-russia."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_to",
    description=(
        "Переходный data-layer TCE-TO: процессы, повестки и поиск персон "
        "в API e-Contas Tribunal de Contas do Tocantins."
    ),
    version="0.1.0",
    api_base="https://api.tceto.tc.br/econtas/api",
    requires_auth=False,
    tags=["tce", "to", "processos", "pautas"],
)
