"""ФССП — данные Федеральной службы судебных приставов."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="fssp",
    opisanie=(
        "Данные ФССП России: исполнительные производства, взыскания, "
        "сведения о должниках, розыск, ограничения на выезд и управление транспортом"
    ),
    versiya="0.2.0",
    baza_api="https://fssp.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=["фссп", "приставы", "взыскания", "долги", "исполнительное-производство"],
)
