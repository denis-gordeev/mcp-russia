"""Инструменты модуля ЕИС Закупок.

Инструменты для поиска данных о закупках, контрактах, поставщиках и заказчиках.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_rub, markdown_table

from . import client


def _auth_note() -> str:
    """Заметка о необходимости настройки API-токена при его отсутствии."""
    if not client._get_api_token():
        return "\n\n*Для полного доступа к API настройте MCP_RUSSIA_ZAKUPKI_API_TOKEN*"
    return ""


async def poisk_zakupok(
    zapros: str = "",
    zakon: str = "",
    region: str = "",
    status: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск закупок в Единой информационной системе.

    Args:
        zapros: Поисковый запрос (предмет закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        region: Регион заказчика.
        status: Статус закупки.

    Returns:
        Результаты поиска закупок.
    """
    if ctx:
        await ctx.info(f"Поиск закупок: {zapros or 'все'}...")

    zakupki = await client.poisk_zakupok(
        query=zapros,
        zakon=zakon,
        region=region,
        status=status,
    )

    if not zakupki:
        header = "**Результаты поиска в ЕИС закупок**\n\n"
        filters = []
        if zapros:
            filters.append(f"Запрос: {zapros}")
        if zakon:
            filters.append(f"Закон: {zakon}")
        if region:
            filters.append(f"Регион: {region}")
        if status:
            filters.append(f"Статус: {status}")
        if filters:
            header += "Фильтры: " + ", ".join(filters) + "\n\n"

        header += (
            "Не удалось получить данные через API ЕИС.\n\n"
            "Данные о закупках доступны через:\n"
            "- Портал ЕИС: https://zakupki.gov.ru\n"
            "- Открытые данные: https://data.zakupki.gov.ru\n\n"
            "Для поиска используйте параметры:\n"
            "- `zapros` — предмет закупки\n"
            "- `zakon` — 44-ФЗ или 223-ФЗ\n"
            "- `region` — субъект РФ\n"
            "- `status` — статус закупки"
        )
        return header

    rows = [
        (z.number, z.title[:60], z.zakon, z.status, format_rub(z.initial_price))
        for z in zakupki[:30]
    ]
    header = "**Результаты поиска в ЕИС закупок**\n\n"
    header += f"Найдено: {len(zakupki)} закупок\n\n"
    return (
        header
        + markdown_table(["Номер", "Название", "Закон", "Статус", "Цена"], rows)
        + _auth_note()
    )


async def info_zakupki(
    nomer_zakupki: str,
    ctx: Context,
) -> str:
    """Получить подробную информацию о конкретной закупке по номеру.

    Args:
        nomer_zakupki: Номер закупки в ЕИС.

    Returns:
        Подробная информация о закупке.
    """
    await ctx.info(f"Запрос информации о закупке {nomer_zakupki}...")
    zakupka = await client.poluchit_zakupku(nomer_zakupki)

    if not zakupka:
        return (
            f"Закупка с номером {nomer_zakupki} не найдена.\n\n"
            f"Используйте poisk_zakupok() для поиска."
        )

    lines = [
        f"**Закупка {zakupka.number}**",
        f"- Название: {zakupka.title}",
    ]
    if zakupka.zakon:
        lines.append(f"- Закон: {zakupka.zakon}")
    if zakupka.sposob:
        lines.append(f"- Способ: {zakupka.sposob}")
    if zakupka.status:
        lines.append(f"- Статус: {zakupka.status}")
    if zakupka.initial_price:
        lines.append(f"- Начальная цена: {format_rub(zakupka.initial_price)}")
    if zakupka.publish_date:
        lines.append(f"- Дата публикации: {zakupka.publish_date}")
    if zakupka.deadline:
        lines.append(f"- Срок подачи заявок: {zakupka.deadline}")
    if zakupka.organizer_name:
        lines.append(f"- Заказчик: {zakupka.organizer_name}")
    if zakupka.organizer_inn:
        lines.append(f"- ИНН заказчика: {zakupka.organizer_inn}")

    lines.append("\nИсточник: ЕИС закупок / zakupki.gov.ru")
    return "\n".join(lines)


async def poisk_kontraktov(
    inn_postavshchika: str = "",
    inn_zakazchika: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск контрактов в реестре контрактов.

    Args:
        inn_postavshchika: ИНН поставщика.
        inn_zakazchika: ИНН заказчика.

    Returns:
        Результаты поиска контрактов.
    """
    if ctx:
        await ctx.info("Поиск контрактов в ЕИС...")

    kontrakty = await client.poisk_kontraktov(
        contractor_inn=inn_postavshchika,
        zakazchik_inn=inn_zakazchika,
    )

    if not kontrakty:
        return (
            "**Результаты поиска контрактов**\n\n"
            "Не удалось получить данные через API ЕИС.\n\n"
            "Реестр контрактов доступен на: https://zakupki.gov.ru"
        )

    rows = [
        (k.number, k.contractor_name[:40], format_rub(k.price), k.status, k.sign_date)
        for k in kontrakty[:30]
    ]
    header = f"**Контракты в ЕИС**\n\nНайдено: {len(kontrakty)}\n\n"
    return (
        header
        + markdown_table(["Номер", "Поставщик", "Цена", "Статус", "Дата"], rows)
        + _auth_note()
    )


async def info_zakazchika(
    inn: str,
    ctx: Context,
) -> str:
    """Получить информацию о заказчике по ИНН.

    Args:
        inn: ИНН заказчика.

    Returns:
        Информация о заказчике.
    """
    await ctx.info(f"Запрос информации о заказчике ИНН {inn}...")
    zakazchik = await client.info_zakazchika(inn)

    if not zakazchik:
        return f"Заказчик с ИНН {inn} не найден в ЕИС.\n\nПроверьте корректность ИНН."

    lines = [
        f"**Заказчик: {zakazchik.name}**",
        f"- ИНН: {zakazchik.inn}",
    ]
    if zakazchik.kpp:
        lines.append(f"- КПП: {zakazchik.kpp}")
    if zakazchik.region:
        lines.append(f"- Регион: {zakazchik.region}")
    if zakazchik.adres:
        lines.append(f"- Адрес: {zakazchik.adres}")
    if zakazchik.zakupki_count:
        lines.append(f"- Количество закупок: {zakazchik.zakupki_count}")
    if zakazchik.total_spent:
        lines.append(f"- Общая сумма контрактов: {format_rub(zakazchik.total_spent)}")

    lines.append("\nИсточник: ЕГРЮЛ / egrul.nalog.ru")
    return "\n".join(lines)


async def info_postavshchika(
    inn: str,
    ctx: Context,
) -> str:
    """Получить информацию о поставщике по ИНН.

    Args:
        inn: ИНН поставщика.

    Returns:
        Информация о поставщике.
    """
    await ctx.info(f"Запрос информации о поставщике ИНН {inn}...")
    postavshchik = await client.info_postavshchika(inn)

    if not postavshchik:
        return f"Поставщик с ИНН {inn} не найден.\n\nПроверьте корректность ИНН."

    status = "Добросовестный" if postavshchik.is_dobrosovestny else "В реестре недобросовестных"
    lines = [
        f"**Поставщик: {postavshchik.name}**",
        f"- ИНН: {postavshchik.inn}",
    ]
    if postavshchik.region:
        lines.append(f"- Регион: {postavshchik.region}")
    lines.append(f"- Статус: {status}")
    if postavshchik.contracts_won:
        lines.append(f"- Выиграно контрактов: {postavshchik.contracts_won}")
    if postavshchik.contracts_executed:
        lines.append(f"- Исполнено контрактов: {postavshchik.contracts_executed}")
    if postavshchik.total_revenue:
        lines.append(f"- Общая выручка: {format_rub(postavshchik.total_revenue)}")

    lines.append("\nИсточник: ЕГРЮЛ/ЕГРИП / egrul.nalog.ru")
    return "\n".join(lines)


async def statusy_zakupok(ctx: Context) -> str:
    """Получить справочник статусов закупок.

    Returns:
        Справочник статусов.
    """
    await ctx.info("Запрос справочника статусов закупок...")
    statusy = client.get_statusy_zakupok()

    rows = [(s["code"], s["name"]) for s in statusy]
    header = "**Статусы закупок в ЕИС**\n\n"
    return header + markdown_table(["Код", "Статус"], rows)


async def sposoby_zakupok(ctx: Context) -> str:
    """Получить справочник способов определения поставщиков.

    Returns:
        Справочник способов.
    """
    await ctx.info("Запрос справочника способов закупок...")
    sposoby = client.get_sposoby_zakupok()

    rows = [(s["code"], s["name"]) for s in sposoby]
    header = "**Способы определения поставщиков**\n\n"
    return header + markdown_table(["Код", "Способ закупки"], rows)


async def plany_zakupok(
    god: int = 2026,
    ctx: Context | None = None,
) -> str:
    """Получить планы-графики закупок на указанный год.

    Args:
        god: Год плана-графика.

    Returns:
        Информация о планах-графиках.
    """
    if ctx:
        await ctx.info(f"Запрос планов закупок на {god} год...")

    plany = await client.plany_zakupok(year=god)

    if not plany:
        return (
            f"**Планы-графики закупок на {god} год**\n\n"
            f"Не удалось получить данные через API ЕИС.\n\n"
            f"Планы-графики формируются заказчиками до начала финансового года.\n"
            f"Доступны через ЕИС: https://zakupki.gov.ru\n\n"
            f"Для поиска планов по конкретному заказчику укажите ИНН организатора."
        )

    rows = [
        (p.organizer_name[:40], p.organizer_inn, str(p.items_count), format_rub(p.total_budget))
        for p in plany[:30]
    ]
    header = f"**Планы-графики закупок на {god} год**\n\n"
    header += f"Найдено: {len(plany)}\n\n"
    return header + markdown_table(["Заказчик", "ИНН", "Позиций", "Бюджет"], rows) + _auth_note()
