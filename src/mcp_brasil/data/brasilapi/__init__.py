"""Совместимый слой BrasilAPI внутри публичного контура mcp-russia."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="brasilapi",
    description=(
        "Переходный data-layer с BrasilAPI: CEP, CNPJ, DDD, банки, валюты, "
        "праздники, ставки, FIPE, ISBN, NCM, PIX и Registro.br."
    ),
    version="0.1.0",
    api_base="https://brasilapi.com.br/api",
    requires_auth=False,
    tags=["cep", "cnpj", "bancos", "cambio", "fipe", "feriados", "isbn", "ncm", "pix"],
)
