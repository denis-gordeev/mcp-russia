"""ФССП — данные Федеральной службы судебных приставов."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="fssp",
    description=(
        "Данные ФССП России: исполнительные производства, взыскания, "
        "сведения о должниках, розыск, ограничения на выезд и управление транспортом"
    ),
    version="0.1.0",
    api_base="https://fssp.gov.ru",
    requires_auth=False,
    tags=["фссп", "приставы", "взыскания", "долги", "исполнительное-производство"],
)
