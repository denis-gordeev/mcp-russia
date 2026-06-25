"""Инструменты модуля РосАПИ.

Инструменты для доступа к российским справочным данным:
- Поиск адресов по почтовому индексу / ФИАС (Дадата)
- Поиск организаций по ИНН/ОГРН (ЕГРЮЛ/ЕГРИП через Дадату)
- Справочник банков (ЦБ РФ через Дадату)
- Праздничные дни России
- Ставки налогов

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
    - Использует Context для структурированного логирования и отчётов о прогрессе
"""

from __future__ import annotations

from datetime import datetime

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import NALOGOVYE_STAVKI, OSNOVNYE_BANKI


async def konsul_adres_po_indeksu(indeks: str, ctx: Context) -> str:
    """Найти адрес по почтовому индексу РФ.

    Аргументы:
        indeks: Почтовый индекс (6 цифр, например 101000).

    Возвращает:
        Адресная информация или сообщение об ошибке.
    """
    await ctx.info(f"Поиск адреса по индексу {indeks}...")
    result = await client.konsultirovat_adres_po_pochtovomu(indeks)

    if isinstance(result, dict) and "oshibka" in result:
        return (
            f"**Почтовый индекс: {indeks}**\n\n"
            f"{result['oshibka']}\n\n"
            f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/address/"
        )

    lines = [
        f"**Почтовый индекс:** {result.pochtovyy_indeks}",
        f"**Полный адрес:** {result.polnyy_adres or 'Н/Д'}",
    ]
    if result.region:
        lines.append(f"**Регион:** {result.region}")
    if result.gorod:
        lines.append(f"**Город:** {result.gorod}")
    if result.ulitsa:
        lines.append(f"**Улица:** {result.ulitsa}")
    if result.dom:
        lines.append(f"**Дом:** {result.dom}")

    lines.append("\nИсточник: ФИАС / Dadata")
    return "\n".join(lines)


async def poisk_adresa(zapros: str, ctx: Context) -> str:
    """Найти адрес по свободному запросу через ФИАС.

    Аргументы:
        zapros: Строка запроса (например, "Москва, Красная площадь").

    Возвращает:
        Список найденных адресов.
    """
    await ctx.info(f"Поиск адреса: {zapros}...")
    results = await client.poisk_adresa(zapros)

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
                addr.get("pochtovyy_indeks", ""),
            )
        )

    header = f"**Результаты поиска: {zapros}**\n\n"
    header += "Источник: ФИАС / Dadata\n\n"
    return header + tablitsa_v_markdown(["#", "Адрес", "Индекс"], rows)


async def poisk_org_po_inn(inn: str, ctx: Context) -> str:
    """Найти организацию по ИНН.

    Аргументы:
        inn: ИНН организации (10 или 12 цифр).

    Возвращает:
        Данные организации.
    """
    await ctx.info(f"Поиск организации по ИНН {inn}...")
    result = await client.nayti_organizatsiyu_po_inn(inn)

    if isinstance(result, dict) and "oshibka" in result:
        return (
            f"**ИНН: {inn}**\n\n"
            f"{result['oshibka']}\n\n"
            f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/party/"
        )

    lines = [
        f"**{result.nazvanie_kratkoe or result.nazvanie_polnoe or 'Организация'}**",
        f"- ИНН: {result.inn}",
    ]
    if result.kpp:
        lines.append(f"- КПП: {result.kpp}")
    if result.ogrn:
        lines.append(f"- ОГРН: {result.ogrn}")
    if result.status:
        karta_statusov = {
            "ACTIVE": "Действующая",
            "LIQUIDATING": "Ликвидируется",
            "LIQUIDATED": "Ликвидирована",
            "BANKRUPT": "Банкрот",
        }
        lines.append(f"- Статус: {karta_statusov.get(result.status, result.status)}")
    if result.adres:
        lines.append(f"- Адрес: {result.adres}")
    if result.rukovoditel:
        lines.append(f"- Руководитель: {result.rukovoditel}")
    if result.data_registratsii:
        lines.append(f"- Дата регистрации: {result.data_registratsii}")

    lines.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
    return "\n".join(lines)


async def poisk_org_po_ogrn(ogrn: str, ctx: Context) -> str:
    """Найти организацию по ОГРН.

    Аргументы:
        ogrn: ОГРН организации (13 или 15 цифр).

    Возвращает:
        Данные организации.
    """
    await ctx.info(f"Поиск организации по ОГРН {ogrn}...")
    result = await client.nayti_organizatsiyu_po_ogrn(ogrn)

    if isinstance(result, dict) and "oshibka" in result:
        return f"**ОГРН: {ogrn}**\n\n{result['oshibka']}"

    lines = [
        f"**{result.nazvanie_kratkoe or result.nazvanie_polnoe or 'Организация'}**",
        f"- ОГРН: {result.ogrn or ogrn}",
    ]
    if result.inn:
        lines.append(f"- ИНН: {result.inn}")
    if result.kpp:
        lines.append(f"- КПП: {result.kpp}")
    if result.adres:
        lines.append(f"- Адрес: {result.adres}")

    lines.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
    return "\n".join(lines)


async def spisok_bankov(ctx: Context) -> str:
    """Получить справочник банков России.

    Возвращает:
        Список банков с БИК и названиями.
    """
    await ctx.info("Запрос справочника банков...")

    rows = []
    for bank in OSNOVNYE_BANKI:
        rows.append(
            (
                bank["bik"],
                bank["nazvanie"],
            )
        )

    header = "**Основные банки России** (справочник)\n\n"
    header += (
        "Для полного справочника всех банков ЦБ РФ "
        "используйте konsul_bank_po_bik или подключите API Dadata.\n\n"
    )
    return header + tablitsa_v_markdown(["БИК", "Название"], rows)


async def konsul_bank_po_bik(bik: str, ctx: Context) -> str:
    """Получить информацию о банке по БИК.

    Аргументы:
        bik: БИК банка (9 цифр).

    Возвращает:
        Данные банка.
    """
    await ctx.info(f"Поиск банка по БИК {bik}...")

    result = await client.nayti_bank_po_bik(bik)

    if isinstance(result, dict) and "oshibka" in result:
        found = None
        for bank in OSNOVNYE_BANKI:
            if bank["bik"] == bik:
                found = bank
                break

        if found:
            return (
                f"**{found['nazvanie']}**\n\n- БИК: {found['bik']}\n- Источник: Справочник ЦБ РФ"
            )

        return (
            f"Банк с БИК {bik} не найден.\n\n"
            f"Для поиска подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
            f"https://dadata.ru/api/bank/"
        )

    lines = [
        f"**{result.nazvanie}**",
        f"- БИК: {result.bik}",
    ]
    if result.nazvanie_kratkoe:
        lines.append(f"- Краткое название: {result.nazvanie_kratkoe}")
    if result.gorod:
        lines.append(f"- Город: {result.gorod}")
    if result.svift:
        lines.append(f"- SWIFT: {result.svift}")

    lines.append("- Источник: ЦБ РФ через Dadata")
    return "\n".join(lines)


async def prazdniki_rf(god: int | None = None, ctx: Context | None = None) -> str:
    """Получить список национальных праздников РФ.

    Аргументы:
        god: Год запроса (например, 2025). По умолчанию — текущий.

    Возвращает:
        Список праздников с датами.
    """
    if god is None:
        god = datetime.now().year

    await ctx.info(f"Запрос праздников на {god} год...")
    holidays = client.poluchit_prazdniki(god)

    rows = []
    for h in holidays:
        date_str = h["data"][5:]
        rows.append((date_str, h["nazvanie"], h["tip"]))

    header = f"**Национальные праздники РФ ({god})**\n\n"
    return header + tablitsa_v_markdown(["Дата", "Праздник", "Тип"], rows)


async def nalogovye_stavki(ctx: Context) -> str:
    """Получить основные налоговые ставки РФ.

    Возвращает:
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
    return header + tablitsa_v_markdown(["Код", "Налог", "Ставка"], rows)
