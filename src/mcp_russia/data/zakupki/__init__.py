"""ЕИС (zakupki) — данные Единой информационной системы в сфере закупок."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="zakupki",
    opisanie=(
        "Данные ЕИС закупок: планы-графики, реестр контрактов, поставщики, "
        "заказчики, способы определения поставщиков, мониторинг закупок"
    ),
    versiya="0.2.0",
    baza_api="https://zakupki.gov.ru",
    trebuet_autentifikatsii=False,
    peremennaya_avt_env="MCP_RUSSIA_ZAKUPKI_API_TOKEN",
    tegi=["закупки", "44-фз", "223-фз", "контракты", "тендеры", "еис"],
    operatsii_trebuyut_avtorizatsii=[
        "poisk_zakupok",
        "poisk_kontraktov",
        "info_zakupki",
        "plany_zakupok",
        "poisk_rnp",
    ],
)
