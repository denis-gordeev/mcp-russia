"""Legacy-слой TransfereGov внутри mcp-russia — парламентские поправки
pix (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="transferegov",
    description=(
        "Legacy-слой TransfereGov внутри mcp-russia — "
        "парламентские поправки pix (специальные трансферты): "
        "поиск по автору, муниципалитету, году и детализации."
    ),
    version="0.1.0",
    api_base="https://api.transferegov.gestao.gov.br",
    requires_auth=False,
    tags=["emendas", "pix", "transferencias", "parlamentar", "municipio"],
)
