"""Tool functions for the Zakupki (ЕИС закупок) feature.

Tools for searching procurement data, contracts, suppliers, and customers.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_rub, markdown_table

from . import client


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
        "Данные о закупках доступны через ЕИС:\n"
        "- Портал ЕИС: https://zakupki.gov.ru\n"
        "- Открытые данные: https://data.zakupki.gov.ru\n\n"
        "Для полноценного поиска используйте API ЕИС с параметрами:\n"
        "- `zapros` — предмет закупки\n"
        "- `zakon` — 44-ФЗ или 223-ФЗ\n"
        "- `region` — субъект РФ\n"
        "- `status` — статус закупки"
    )
    return header


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
        f"- Закон: {zakupka.zakon}",
        f"- Способ: {zakupka.sposob}",
        f"- Статус: {zakupka.status}",
        f"- Начальная цена: {format_rub(zakupka.initial_price)}",
        f"- Дата публикации: {zakupka.publish_date}",
        f"-Deadline подачи заявок: {zakupka.deadline}",
        f"- Заказчик: {zakupka.organizer_name}",
        f"- ИНН заказчика: {zakupka.organizer_inn}",
    ]
    return "\n".join(lines)


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
        return (
            f"Заказчик с ИНН {inn} не найден в ЕИС.\n\n"
            f"Проверьте корректность ИНН."
        )

    lines = [
        f"**Заказчик: {zakazchik.name}**",
        f"- ИНН: {zakazchik.inn}",
        f"- КПП: {zakazchik.kpp}",
        f"- Регион: {zakazchik.region}",
        f"- Адрес: {zakazchik.adres}",
        f"- Количество закупок: {zakazchik.zakupki_count}",
        f"- Общая сумма контрактов: {format_rub(zakazchik.total_spent)}",
    ]
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
        return (
            f"Поставщик с ИНН {inn} не найден в ЕИС.\n\n"
            f"Проверьте корректность ИНН."
        )

    status = "Добросовестный" if postavshchik.is_dobrosovestny else "В реестре недобросовестных"
    lines = [
        f"**Поставщик: {postavshchik.name}**",
        f"- ИНН: {postavshchik.inn}",
        f"- Регион: {postavshchik.region}",
        f"- Статус: {status}",
        f"- Выиграно контрактов: {postavshchik.contracts_won}",
        f"- Исполнено контрактов: {postavshchik.contracts_executed}",
        f"- Общая выручка: {format_rub(postavshchik.total_revenue)}",
    ]
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
    return (
        f"**Планы-графики закупок на {god} год**\n\n"
        f"Планы-графики формируются заказчиками до начала финансового года.\n"
        f"Доступны через ЕИС: https://zakupki.gov.ru\n\n"
        f"Для поиска планов по конкретному заказчику укажите ИНН организатора."
    )
