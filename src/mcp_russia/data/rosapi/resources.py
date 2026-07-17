"""Справочные ресурсы модуля РосАПИ."""

from __future__ import annotations

from .constants import NALOGOVYE_STAVKI


async def dostupnye_servisy() -> dict[str, str]:
    """Список доступных российских справочных сервисов."""
    return {
        "fias": "ФИАС — Федеральная информационная адресная система (fias.nalog.ru)",
        "dadata_adresa": "API адресов Dadata — поиск адресов (dadata.ru/api/address)",
        "dadata_organizatsii": "API организаций Dadata — поиск организаций (dadata.ru/api/party)",
        "dadata_banki": "API банков Dadata — справочник банков (dadata.ru/api/bank)",
        "cbr_kreditnye": "Справочник кредитных организаций ЦБ РФ (cbr.ru/credit)",
        "nalog_ru": "ФНС России — проверка контрагентов (nalog.ru)",
        "pochtovyy_api": "API почтовых индексов (postal-api.ru)",
    }


async def nalogovye_stavki_resurs() -> dict[str, str]:
    """Справочник основных налоговых ставок РФ."""
    return NALOGOVYE_STAVKI
