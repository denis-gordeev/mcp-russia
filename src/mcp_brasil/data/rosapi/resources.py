"""Resources for the RosAPI feature."""

from __future__ import annotations

from .constants import NALOGOVYE_STAVKI


async def dostupnye_servisy() -> dict[str, str]:
    """Список доступных российских справочных сервисов."""
    return {
        "fias": "ФИАС — Федеральная информационная адресная система (fias.nalog.ru)",
        "dadata_address": "Dadata Address API — поиск адресов (dadata.ru/api/address)",
        "dadata_party": "Dadata Party API — поиск организаций (dadata.ru/api/party)",
        "dadata_bank": "Dadata Bank API — справочник банков (dadata.ru/api/bank)",
        "cbr_credit": "Справочник кредитных организаций ЦБ РФ (cbr.ru/credit)",
        "nalog_ru": "ФНС России — проверка контрагентов (nalog.ru)",
        "postal_api": "API почтовых индексов (postal-api.ru)",
    }


async def nalogovye_stavki_resurs() -> dict[str, str]:
    """Справочник основных налоговых ставок РФ."""
    return NALOGOVYE_STAVKI
