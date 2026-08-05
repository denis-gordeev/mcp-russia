"""Госдума — данные Государственной Думы Федерального Собрания РФ."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="gosduma",
    opisanie=(
        "Данные Государственной Думы: депутаты, законопроекты, пленарные заседания, "
        "голосования, комитеты, фракции"
    ),
    versiya="0.2.0",
    baza_api="https://api.duma.gov.ru",
    trebuet_autentifikatsii=False,
    peremennaya_avt_env="MCP_RUSSIA_DUMA_API_TOKEN",
    tegi=["госдума", "депутаты", "законопроекты", "парламент", "голосования"],
    operatsii_trebuyut_avtorizatsii=["spisok_deputatov", "zakonoproekty", "golosovaniya"],
)
