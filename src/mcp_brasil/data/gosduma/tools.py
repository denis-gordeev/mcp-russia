"""Tool functions for the Gosduma (State Duma) feature.

Tools for accessing State Duma deputies, bills, factions, and votes.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import markdown_table

from . import client


async def spisok_deputatov(sozyv: str = "", ctx: Context | None = None) -> str:
    """Получить список депутатов Государственной Думы.

    Args:
        sozyv: Номер созыва (например, '8'). По умолчанию — текущий.

    Returns:
        Список депутатов.
    """
    # Placeholder — actual API integration needed
    header = "**Депутаты Государственной Думы**\n\n"
    header += (
        f"Данные о депутатах доступны через открытые данные Госдумы:\n"
        f"https://download.data.duma.gov.ru\n\n"
        f"Для запроса депутатов созыва {sozyv or 'текущего'} "
        f"используйте API Государственной Думы."
    )
    return header


async def info_deputata(id_deputata: int, ctx: Context) -> str:
    """Получить информацию о конкретном депутате Госдумы.

    Args:
        id_deputata: ID депутата.

    Returns:
        Подробная информация о депутате.
    """
    await ctx.info(f"Запрос информации о депутате {id_deputata}...")
    deputat = await client.poluchit_deputata(id_deputata)

    if not deputat:
        return (
            f"Депутат с ID {id_deputata} не найден.\n\nИспользуйте spisok_deputatov() для поиска."
        )

    lines = [
        f"**{deputat.фамилия} {deputat.имя} {deputat.отчество}**",
        f"- ID: {deputat.id}",
    ]
    if deputat.фракция:
        lines.append(f"- Фракция: {deputat.фракция}")
    if deputat.комитет:
        lines.append(f"- Комитет: {deputat.комитет}")
    if deputat.регион:
        lines.append(f"- Регион: {deputat.регион}")
    if deputat.созыв:
        lines.append(f"- Созыв: {deputat.созыв}")

    return "\n".join(lines)


async def spisok_frakcii(ctx: Context) -> str:
    """Получить список фракций Государственной Думы.

    Returns:
        Список фракций.
    """
    await ctx.info("Запрос списка фракций Госдумы...")
    frakcii = client.get_frakcii()

    rows = [(f["code"], f["name"]) for f in frakcii]
    header = "**Фракции Государственной Думы**\n\n"
    return header + markdown_table(["Код", "Фракция"], rows)


async def spisok_komitetov(ctx: Context) -> str:
    """Получить список комитетов Государственной Думы.

    Returns:
        Список комитетов.
    """
    await ctx.info("Запрос списка комитетов Госдумы...")
    komitety = client.get_komitety()

    rows = [(k["code"], k["name"]) for k in komitety]
    header = "**Комитеты Государственной Думы**\n\n"
    return header + markdown_table(["Код", "Комитет"], rows)


async def spisok_sozyvov(ctx: Context) -> str:
    """Получить список созывов Государственной Думы.

    Returns:
        Список созывов.
    """
    await ctx.info("Запрос списка созывов Госдумы...")
    sozyvy = client.get_sozyvy()

    rows = [(s["code"], s["name"]) for s in sozyvy]
    header = "**Созывы Государственной Думы**\n\n"
    return header + markdown_table(["Код", "Созыв"], rows)


async def zakonoproekty(status: str = "", ctx: Context | None = None) -> str:
    """Получить список законопроектов Государственной Думы.

    Args:
        status: Фильтр по статусу (например, 'принят', 'рассматривается').

    Returns:
        Список законопроектов.
    """
    return (
        f"**Законопроекты Государственной Думы**\n\n"
        f"Данные о законопроектах доступны через:\n"
        f"- Система СОЗД: https://sozd.duma.gov.ru\n"
        f"- Открытые данные: https://download.data.duma.gov.ru\n\n"
        f"Для поиска законопроектов по статусу '{status or 'все'}' "
        f"используйте API СОЗД."
    )
