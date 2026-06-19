"""Инструменты модуля Совета Федерации РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client


async def spisok_senatorov(ctx: Context) -> str:
    """Получить список сенаторов Совета Федерации."""
    await ctx.info("Запрос списка сенаторов...")
    senatory = await client.poisk_senatorov()
    if not senatory:
        return "Сенаторы не найдены.\n\nАктуальные данные доступны на: https://sovfed.ru/senators"
    rows = [
        (
            s.get("nomer", ""),
            s.get("familiya", ""),
            s.get("imya", ""),
            s.get("region", ""),
            s.get("komitet", "")[:40],
        )
        for s in senatory
    ]
    header = f"**Сенаторы Совета Федерации РФ** — найдено: {len(senatory)}\n\n"
    return header + markdown_table(
        ["№", "Фамилия", "Имя", "Регион", "Комитет"],
        rows,
    )


async def info_senatora(identifikator_senatora: str, ctx: Context) -> str:
    """Получить информацию о сенаторе Совета Федерации.

    Аргументы:
        identifikator_senatora: Идентификатор сенатора.

    Возвращает:
        Информация о сенаторе.
    """
    await ctx.info(f"Запрос информации о сенаторе {identifikator_senatora}...")
    data = await client.info_senatora(identifikator_senatora)
    if not data:
        return (
            f"Сенатор '{identifikator_senatora}' не найден.\n\n"
            f"Проверьте идентификатор на сайте Совета Федерации: sovfed.ru/senators"
        )
    fio = f"{data.get('familiya', '')} {data.get('imya', '')} {data.get('otchestvo', '')}".strip()
    lines = [
        f"**{fio}** (№ {data.get('nomer', identifikator_senatora)})",
        f"- Регион: {data.get('region', '')}",
        f"- Должность: {data.get('dolzhnost', '')}",
    ]
    if data.get("komitet"):
        lines.append(f"- Комитет: {data['komitet']}")
    if data.get("frakciya"):
        lines.append(f"- Фракция: {data['frakciya']}")
    if data.get("data_naznacheniya"):
        lines.append(f"- Дата назначения: {data['data_naznacheniya']}")
    lines.append(f"- Источник: {data.get('istochnik', 'sovfed.ru')}")
    return "\n".join(lines)


async def spisok_komitetov(ctx: Context) -> str:
    """Получить список комитетов Совета Федерации."""
    await ctx.info("Запрос списка комитетов...")
    komitety_api = await client.spisok_komitetov()
    if komitety_api:
        rows = [
            (
                k.get("nazvanie", ""),
                k.get("predsedatel", ""),
                str(k.get("kolichestvo_chlenov", "")),
            )
            for k in komitety_api
        ]
        header = "**Комитеты Совета Федерации РФ**\n\n"
        return header + markdown_table(["Комитет", "Председатель", "Членов"], rows)
    komitety = client.get_komitety_list()
    rows = [(k["kod"], k["nazvanie"]) for k in komitety]
    header = "**Комитеты Совета Федерации РФ** (справочник)\n\n"
    return header + markdown_table(["Код", "Комитет"], rows)


async def spisok_komissiy(ctx: Context) -> str:
    """Получить список комиссий Совета Федерации."""
    await ctx.info("Запрос списка комиссий...")
    komissii_api = await client.spisok_komissiy()
    if komissii_api:
        rows = [
            (
                k.get("nazvanie", ""),
                k.get("predsedatel", ""),
                str(k.get("kolichestvo_chlenov", "")),
            )
            for k in komissii_api
        ]
        header = "**Комиссии Совета Федерации РФ**\n\n"
        return header + markdown_table(["Комиссия", "Председатель", "Членов"], rows)
    komissii = client.get_komissii_list()
    rows = [(k["kod"], k["nazvanie"]) for k in komissii]
    header = "**Комиссии Совета Федерации РФ** (справочник)\n\n"
    return header + markdown_table(["Код", "Комиссия"], rows)


async def poisk_zakonoproektov(
    ctx: Context,
    status: str = "",
    god: int = 0,
) -> str:
    """Поиск законопроектов, рассмотренных Советом Федерации.

    Аргументы:
        status: Статус законопроекта (необязательно).
        god: Год (необязательно).

    Возвращает:
        Список законопроектов.
    """
    await ctx.info("Поиск законопроектов...")
    zakonoproekty = await client.poisk_zakonoproektov(
        status=status,
        god=god,
    )
    if not zakonoproekty:
        filters = []
        if status:
            filters.append(f"статус: {status}")
        if god:
            filters.append(f"год: {god}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Законопроекты{filter_text} не найдены.\n\n"
            f"Данные доступны на: https://sovfed.ru/bills"
        )
    rows = [
        (
            z.get("nomer", ""),
            z.get("nazvanie", "")[:50],
            z.get("status", ""),
            z.get("data_rassmotreniya", ""),
        )
        for z in zakonoproekty
    ]
    header = f"**Законопроекты Совета Федерации РФ** — найдено: {len(zakonoproekty)}\n\n"
    return header + markdown_table(
        ["№", "Название", "Статус", "Дата рассмотрения"],
        rows,
    )


async def spisok_zasedaniy(ctx: Context, god: int = 0) -> str:
    """Получить список заседаний Совета Федерации.

    Аргументы:
        god: Год (необязательно).

    Возвращает:
        Список заседаний.
    """
    await ctx.info("Запрос списка заседаний...")
    zasedaniya = await client.spisok_zasedaniy(god=god)
    if not zasedaniya:
        god_text = f" за {god} год" if god else ""
        return f"Заседания{god_text} не найдены.\n\nДанные доступны на: https://sovfed.ru/sessions"
    rows = [
        (
            z.get("nomer", ""),
            z.get("data", ""),
            z.get("status", ""),
            z.get("povestka", "")[:50],
        )
        for z in zasedaniya
    ]
    header = f"**Заседания Совета Федерации РФ** — найдено: {len(zasedaniya)}\n\n"
    return header + markdown_table(
        ["№", "Дата", "Статус", "Повестка"],
        rows,
    )
