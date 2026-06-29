"""Инструменты модуля Госдумы.

Инструменты для доступа к данным о депутатах, законопроектах, фракциях и голосованиях Госдумы.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


def _zametka_ob_avtorizatsii() -> str:
    """Заметка о необходимости настройки API-токена при его отсутствии."""
    if not client._poluchit_api_token():
        return "\n\n*Для полного доступа к API настройте MCP_RUSSIA_DUMA_API_TOKEN*"
    return ""


async def spisok_deputatov(sozyv: str = "", ctx: Context | None = None) -> str:
    """Получить список депутатов Государственной Думы.

    Аргументы:
        sozyv: Номер созыва (например, '8'). По умолчанию — текущий.

    Возвращает:
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

    stroki_tablitsy = [
        (str(d.identifikator), f"{d.фамилия} {d.имя} {d.отчество}".strip(), d.фракция, d.комитет)
        for d in deputats[:50]
    ]
    header = f"**Депутаты Государственной Думы (созыв {sozyv or 'текущий'})**\n\n"
    header += f"Найдено: {len(deputats)} депутатов"
    if len(deputats) > 50:
        header += " (показано первых 50)"
    header += "\n\n"
    return (
        header
        + tablitsa_v_markdown(["ID", "ФИО", "Фракция", "Комитет"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def info_deputata(identifikator_deputata: int, ctx: Context) -> str:
    """Получить информацию о конкретном депутате Госдумы.

    Аргументы:
        identifikator_deputata: ID депутата.

    Возвращает:
        Подробная информация о депутате.
    """
    await ctx.info(f"Запрос информации о депутате {identifikator_deputata}...")
    deputat = await client.poluchit_deputata(identifikator_deputata)

    if not deputat:
        return (
            f"Депутат с ID {identifikator_deputata} не найден.\n\n"
            f"Используйте spisok_deputatov() для поиска."
        )

    stroki = [
        f"**{deputat.фамилия} {deputat.имя} {deputat.отчество}**",
        f"- ID: {deputat.identifikator}",
    ]
    if deputat.фракция:
        stroki.append(f"- Фракция: {deputat.фракция}")
    if deputat.комитет:
        stroki.append(f"- Комитет: {deputat.комитет}")
    if deputat.регион:
        stroki.append(f"- Регион: {deputat.регион}")
    if deputat.созыв:
        stroki.append(f"- Созыв: {deputat.созыв}")

    stroki.append("\nИсточник: api.duma.gov.ru / Госдума ФС РФ")

    return "\n".join(stroki)


async def spisok_frakcii(ctx: Context) -> str:
    """Получить список фракций Государственной Думы.

    Возвращает:
        Список фракций.
    """
    await ctx.info("Запрос списка фракций Госдумы...")
    frakcii = client.poluchit_fraktsii()

    stroki_tablitsy = [(f["kod"], f["nazvanie"]) for f in frakcii]
    header = "**Фракции Государственной Думы**\n\n"
    return header + tablitsa_v_markdown(["Код", "Фракция"], stroki_tablitsy)


async def spisok_komitetov(ctx: Context) -> str:
    """Получить список комитетов Государственной Думы.

    Возвращает:
        Список комитетов.
    """
    await ctx.info("Запрос списка комитетов Госдумы...")
    komitety = client.poluchit_komitety()

    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in komitety]
    header = "**Комитеты Государственной Думы**\n\n"
    return header + tablitsa_v_markdown(["Код", "Комитет"], stroki_tablitsy)


async def spisok_sozyvov(ctx: Context) -> str:
    """Получить список созывов Государственной Думы.

    Возвращает:
        Список созывов.
    """
    await ctx.info("Запрос списка созывов Госдумы...")
    sozyvy = client.poluchit_sozyvy()

    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in sozyvy]
    header = "**Созывы Государственной Думы**\n\n"
    return header + tablitsa_v_markdown(["Код", "Созыв"], stroki_tablitsy)


async def zakonoproekty(
    sostoyanie: str = "",
    ogranichenie: int = 20,
    ctx: Context | None = None,
) -> str:
    """Получить список законопроектов Государственной Думы.

    Аргументы:
        sostoyanie: Фильтр по статусу (например, 'принят', 'рассматривается').
        ogranichenie: Максимальное количество результатов (до 50).

    Возвращает:
        Список законопроектов.
    """
    if ctx:
        await ctx.info(f"Запрос законопроектов (статус: {sostoyanie or 'все'})...")
    bills = await client.poluchit_zakonoproekty(sostoyanie=sostoyanie, ogranichenie=ogranichenie)

    if not bills:
        status_label = sostoyanie or "все"
        return (
            f"**Законопроекты Государственной Думы**\n\n"
            f"Не удалось получить данные через API СОЗД.\n\n"
            f"Данные о законопроектах доступны через:\n"
            f"- Система СОЗД: https://sozd.duma.gov.ru\n"
            f"- API: https://api.duma.gov.ru\n\n"
            f"Для поиска законопроектов по статусу '{status_label}' "
            f"используйте API СОЗД."
        )

    stroki_tablitsy = [(b.nomer, b.nazvanie[:80], b.sostoyanie, b.data_vneseniya) for b in bills]
    header = "**Законопроекты Государственной Думы**\n\n"
    header += f"Найдено: {len(bills)} законопроектов\n\n"
    return (
        header
        + tablitsa_v_markdown(["Номер", "Название", "Статус", "Дата внесения"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def golosovaniya(
    sozyv: str = "",
    ogranichenie: int = 20,
    ctx: Context | None = None,
) -> str:
    """Получить результаты голосований Государственной Думы.

    Аргументы:
        sozyv: Номер созыва.
        ogranichenie: Максимальное количество результатов (до 50).

    Возвращает:
        Результаты голосований.
    """
    if ctx:
        await ctx.info(f"Запрос голосований (созыв: {sozyv or 'текущий'})...")
    votes = await client.poluchit_golosovaniya(sozyv=sozyv, ogranichenie=ogranichenie)

    if not votes:
        return (
            "**Голосования Государственной Думы**\n\n"
            "Не удалось получить данные через API Госдумы.\n\n"
            "Результаты голосований доступны на:\n"
            "- https://duma.gov.ru\n"
            "- https://api.duma.gov.ru\n\n"
            "Для доступа к API может потребоваться токен (DUMA_API_TOKEN)."
        )

    stroki_tablitsy = [
        (v.zakonoproekt_identifikator, v.nazvanie[:60], v.data, f"За: {v.za} / Против: {v.protiv}")
        for v in votes
    ]
    header = "**Голосования Государственной Думы**\n\n"
    header += f"Найдено: {len(votes)} голосований\n\n"
    return (
        header
        + tablitsa_v_markdown(["ID", "Тема", "Дата", "Результат"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )
