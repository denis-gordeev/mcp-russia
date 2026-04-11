"""Legacy-слой Diário Oficial внутри mcp-russia — поиск в официальных
муниципальных газетах через Querido Diário (compatibility layer, legacy)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="diario_oficial",
    description=(
        "Legacy-слой Querido Diário внутри mcp-russia: "
        "Текстовый поиск в официальных муниципальных газетах 5000+ городов Бразилии. "
        "Контракты, назначения, санкции, тендеры и административные акты."
    ),
    version="0.1.0",
    api_base="https://queridodiario.ok.org.br",
    requires_auth=False,
    tags=["официальная-газета", "прозрачность", "муниципалитеты", "тендеры", "контракты"],
)
