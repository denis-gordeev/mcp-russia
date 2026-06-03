"""Tool functions for the RosAPI feature.

Tools for accessing Russian reference data:
- Address lookup via postal code / ФИАС (Dadata)
- Organization lookup by INN/OGRN (ЕГРЮЛ/ЕГРИП через Dadata)
- Bank directory (ЦБ РФ через Dadata)
- Russian national holidays
- Tax rates

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
    - Uses Context for structured logging and progress reporting
"""

from __future__ import annotations

from datetime import datetime

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import NALOGOVYE_STAVKI, OSNOVNYE_BANKI


async def konsul_adres_po_indeksu(indeks: str, ctx: Context) -> str:
    """Найти адрес по почтовому индексу РФ.

    Args:
        indeks: Почтовый индекс (6 цифр, например 101000).

    Returns:
        Адресная информация или сообщение об ошибке.
    """
    await ctx.info(f"Поиск адреса по индексу {indeks}...")
    result = await client.consult_address_by_postal(indeks)

    if isinstance(result, dict) and "error" in result:
        return (
            f"**Почтовый индекс: {indeks}**\n\n"
            f"{result['error']}\n\n"
            f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/address/"
        )

    lines = [
        f"**Почтовый индекс:** {result.postal_code}",
        f"**Полный адрес:** {result.full_address or 'Н/Д'}",
    ]
    if result.region:
        lines.append(f"**Регион:** {result.region}")
    if result.city:
        lines.append(f"**Город:** {result.city}")
    if result.street:
        lines.append(f"**Улица:** {result.street}")
    if result.house:
        lines.append(f"**Дом:** {result.house}")

    lines.append("\nИсточник: ФИАС / Dadata")
    return "\n".join(lines)


async def poisk_adresa(zapros: str, ctx: Context) -> str:
    """Найти адрес по свободному запросу через ФИАС.

    Args:
        zapros: Строка запроса (например, "Москва, Красная площадь").

    Returns:
        Список найденных адресов.
    """
    await ctx.info(f"Поиск адреса: {zapros}...")
    results = await client.search_address(zapros)

    if not results:
        return (
            f"Адреса по запросу '{zapros}' не найдены.\n\n"
            "Используйте более точный запрос или проверьте MCP_RUSSIA_DADATA_API_KEY."
        )

    rows = []
    for i, addr in enumerate(results[:10], 1):
        rows.append(
            (
                str(i),
                addr.get("value", ""),
                addr.get("postal_code", ""),
            )
        )

    header = f"**Результаты поиска: {zapros}**\n\n"
    header += "Источник: ФИАС / Dadata\n\n"
    return header + markdown_table(["#", "Адрес", "Индекс"], rows)


async def poisk_org_po_inn(inn: str, ctx: Context) -> str:
    """Найти организацию по ИНН.

    Args:
        inn: ИНН организации (10 или 12 цифр).

    Returns:
        Данные организации.
    """
    await ctx.info(f"Поиск организации по ИНН {inn}...")
    result = await client.find_org_by_inn(inn)

    if isinstance(result, dict) and "error" in result:
        return (
            f"**ИНН: {inn}**\n\n"
            f"{result['error']}\n\n"
            f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/party/"
        )

    lines = [
        f"**{result.name_short or result.name_full or 'Организация'}**",
        f"- ИНН: {result.inn}",
    ]
    if result.kpp:
        lines.append(f"- КПП: {result.kpp}")
    if result.ogrn:
        lines.append(f"- ОГРН: {result.ogrn}")
    if result.status:
        status_map = {
            "ACTIVE": "Действующая",
            "LIQUIDATING": "Ликвидируется",
            "LIQUIDATED": "Ликвидирована",
            "BANKRUPT": "Банкрот",
        }
        lines.append(f"- Статус: {status_map.get(result.status, result.status)}")
    if result.address:
        lines.append(f"- Адрес: {result.address}")
    if result.director:
        lines.append(f"- Руководитель: {result.director}")
    if result.registration_date:
        lines.append(f"- Дата регистрации: {result.registration_date}")

    lines.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
    return "\n".join(lines)


async def poisk_org_po_ogrn(ogrn: str, ctx: Context) -> str:
    """Найти организацию по ОГРН.

    Args:
        ogrn: ОГРН организации (13 или 15 цифр).

    Returns:
        Данные организации.
    """
    await ctx.info(f"Поиск организации по ОГРН {ogrn}...")
    result = await client.find_org_by_ogrn(ogrn)

    if isinstance(result, dict) and "error" in result:
        return f"**ОГРН: {ogrn}**\n\n{result['error']}"

    lines = [
        f"**{result.name_short or result.name_full or 'Организация'}**",
        f"- ОГРН: {result.ogrn or ogrn}",
    ]
    if result.inn:
        lines.append(f"- ИНН: {result.inn}")
    if result.kpp:
        lines.append(f"- КПП: {result.kpp}")
    if result.address:
        lines.append(f"- Адрес: {result.address}")

    lines.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
    return "\n".join(lines)


async def spisok_bankov(ctx: Context) -> str:
    """Получить справочник банков России.

    Returns:
        Список банков с БИК и названиями.
    """
    await ctx.info("Запрос справочника банков...")

    rows = []
    for bank in OSNOVNYE_BANKI:
        rows.append(
            (
                bank["bik"],
                bank["name"],
            )
        )

    header = "**Основные банки России** (справочник)\n\n"
    header += (
        "Для полного справочника всех банков ЦБ РФ "
        "используйте konsul_bank_po_bik или подключите API Dadata.\n\n"
    )
    return header + markdown_table(["БИК", "Название"], rows)


async def konsul_bank_po_bik(bik: str, ctx: Context) -> str:
    """Получить информацию о банке по БИК.

    Args:
        bik: БИК банка (9 цифр).

    Returns:
        Данные банка.
    """
    await ctx.info(f"Поиск банка по БИК {bik}...")

    result = await client.find_bank_by_bik(bik)

    if isinstance(result, dict) and "error" in result:
        found = None
        for bank in OSNOVNYE_BANKI:
            if bank["bik"] == bik:
                found = bank
                break

        if found:
            return f"**{found['name']}**\n\n- БИК: {found['bik']}\n- Источник: Справочник ЦБ РФ"

        return (
            f"Банк с БИК {bik} не найден.\n\n"
            f"Для поиска подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/bank/"
        )

    lines = [
        f"**{result.name}**",
        f"- БИК: {result.bik}",
    ]
    if result.name_short:
        lines.append(f"- Краткое название: {result.name_short}")
    if result.city:
        lines.append(f"- Город: {result.city}")
    if result.swift:
        lines.append(f"- SWIFT: {result.swift}")

    lines.append("- Источник: ЦБ РФ через Dadata")
    return "\n".join(lines)


async def prazdniki_rf(god: int | None = None, ctx: Context | None = None) -> str:
    """Получить список национальных праздников РФ.

    Args:
        god: Год запроса (например, 2025). По умолчанию — текущий.

    Returns:
        Список праздников с датами.
    """
    if god is None:
        god = datetime.now().year

    await ctx.info(f"Запрос праздников на {god} год...")
    holidays = client.get_holidays(god)

    rows = []
    for h in holidays:
        date_str = h["date"][5:]
        rows.append((date_str, h["name"], h["type"]))

    header = f"**Национальные праздники РФ ({god})**\n\n"
    return header + markdown_table(["Дата", "Праздник", "Тип"], rows)


async def nalogovye_stavki(ctx: Context) -> str:
    """Получить основные налоговые ставки РФ.

    Returns:
        Справочная информация о налогах.
    """
    await ctx.info("Запрос налоговых ставок...")

    stavki_info = {
        "NDS": "20% (базовая), 10% (льготная), 0% (экспорт)",
        "NP": "20% (базовая)",
        "NDFL": "13% (резидент), 30% (нерезидент)",
        "USN_D": "6% (может быть снижен регионом до 1%)",
        "USN_DR": "15% (может быть снижен регионом до 5%)",
        "ESN": "6% (от дохода)",
    }

    rows = []
    for code, name in NALOGOVYE_STAVKI.items():
        stavka = stavki_info.get(code, "Уточняйте в ФНС")
        rows.append((code, name, stavka))

    header = "**Основные налоговые ставки РФ**\n\n"
    header += "⚠️ Актуальные ставки уточняйте на сайте ФНС: https://www.nalog.ru\n\n"
    return header + markdown_table(["Код", "Налог", "Ставка"], rows)
