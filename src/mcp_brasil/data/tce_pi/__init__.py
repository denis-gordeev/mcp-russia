"""Legacy-слой TCE-PI внутри mcp-russia — Tribunal de Contas do Piauí (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_pi",
    description=(
        "Legacy-слой TCE-PI внутри mcp-russia: "
        "Префектуры, расходы, доходы и органы штата Пиауи "
        "через API портала гражданского участия TCE-PI."
    ),
    version="0.1.0",
    api_base="https://sistemas.tce.pi.gov.br/api/portaldacidadania",
    requires_auth=False,
    tags=["tce", "pi", "prefeituras", "despesas", "receitas", "orgaos"],
)
