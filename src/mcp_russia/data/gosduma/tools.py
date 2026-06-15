"""Инструменты модуля Госдумы.

Инструменты для доступа к данным о депутатах, законопроектах, фракциях и голосованиях Госдумы.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client


def _auth_note() -> str:
    """Заметка о необходимости настройки API-токена при его отсутствии."""
    if not client._get_api_token():
        return "\n\n*Для полного доступа к API настройте MCP_RUSSIA_DUMA_API_TOKEN*"
    return ""


async def spisok_deputatov(sozyv: str = "", ctx: Context | None = None) -> str:
    """Получить список депутатов Государственной Думы.

    Args:
        sozyv: Номер созыва (например, '8'). По умолчанию — текущий.

    Returns:
        Список депутатов.
    """
    if ctx:
        await ctx.info(f"Запрос депутатов Госдумы (созыв: {sozyv or 'текущий'})...")
    deputats = await client.poluchit_deputatov(sozyv)

    if not deputats:
        sozyv_label = sozyv or "текущего"
        return (
            f"**Депутаты Государственной Думы ({sozyv_label} созыв)**\n\n"
            f"Не удалось получить данные через API Госдумы.\n\n"
            f"Открытые данные доступны на:\n"
            f"- https://api.duma.gov.ru\n"
            f"- https://download.data.duma.gov.ru\n\n"
            f"Для доступа к API может потребоваться токен (DUMA_API_TOKEN)."
        )

    rows = [
        (str(d.id), f"{d.фамилия} {d.имя} {d.отчество}".strip(), d.фракция, d.комитет)
        for d in deputats[:50]
    ]
    header = f"**Депутаты Государственной Думы (созыв {sozyv or 'текущий'})**\n\n"
    header += f"Найдено: {len(deputats)} депутатов"
    if len(deputats) > 50:
        header += " (показано первых 50)"
    header += "\n\n"
    return header + markdown_table(["ID", "ФИО", "Фракция", "Комитет"], rows) + _auth_note()


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

    lines.append("\nИсточник: api.duma.gov.ru / Госдума ФС РФ")

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


async def zakonoproekty(
    status: str = "",
    limit: int = 20,
    ctx: Context | None = None,
) -> str:
    """Получить список законопроектов Государственной Думы.

    Args:
        status: Фильтр по статусу (например, 'принят', 'рассматривается').
        limit: Максимальное количество результатов (до 50).

    Returns:
        Список законопроектов.
    """
    if ctx:
        await ctx.info(f"Запрос законопроектов (статус: {status or 'все'})...")
    bills = await client.poluchit_zakonoproekty(status=status, limit=limit)

    if not bills:
        status_label = status or "все"
        return (
            f"**Законопроекты Государственной Думы**\n\n"
            f"Не удалось получить данные через API СОЗД.\n\n"
            f"Данные о законопроектах доступны через:\n"
            f"- Система СОЗД: https://sozd.duma.gov.ru\n"
            f"- API: https://api.duma.gov.ru\n\n"
            f"Для поиска законопроектов по статусу '{status_label}' "
            f"используйте API СОЗД."
        )

    rows = [(b.number, b.title[:80], b.status, b.date_vnesen) for b in bills]
    header = "**Законопроекты Государственной Думы**\n\n"
    header += f"Найдено: {len(bills)} законопроектов\n\n"
    return (
        header
        + markdown_table(["Номер", "Название", "Статус", "Дата внесения"], rows)
        + _auth_note()
    )


async def golosovaniya(
    sozyv: str = "",
    limit: int = 20,
    ctx: Context | None = None,
) -> str:
    """Получить результаты голосований Государственной Думы.

    Args:
        sozyv: Номер созыва.
        limit: Максимальное количество результатов (до 50).

    Returns:
        Результаты голосований.
    """
    if ctx:
        await ctx.info(f"Запрос голосований (созыв: {sozyv or 'текущий'})...")
    votes = await client.poluchit_golosovaniya(sozyv=sozyv, limit=limit)

    if not votes:
        return (
            "**Голосования Государственной Думы**\n\n"
            "Не удалось получить данные через API Госдумы.\n\n"
            "Результаты голосований доступны на:\n"
            "- https://duma.gov.ru\n"
            "- https://api.duma.gov.ru\n\n"
            "Для доступа к API может потребоваться токен (DUMA_API_TOKEN)."
        )

    rows = [
        (v.zakonoproekt_id, v.title[:60], v.date, f"За: {v.za} / Против: {v.protiv}")
        for v in votes
    ]
    header = "**Голосования Государственной Думы**\n\n"
    header += f"Найдено: {len(votes)} голосований\n\n"
    return header + markdown_table(["ID", "Тема", "Дата", "Результат"], rows) + _auth_note()
