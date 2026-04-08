"""Legacy feature DataJud — переходный слой судебных данных Бразилии."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="datajud",
    description=(
        "Legacy-слой DataJud (CNJ) внутри mcp-russia: "
        "бразильские судебные процессы, движения дел и справочники tribunais"
    ),
    version="0.1.0",
    api_base="https://api-publica.datajud.cnj.jus.br",
    requires_auth=True,
    auth_env_var="DATAJUD_API_KEY",
    tags=["judiciario", "processos", "cnj", "tribunais", "datajud"],
)
