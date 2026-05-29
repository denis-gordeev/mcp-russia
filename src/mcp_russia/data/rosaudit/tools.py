"""Tool functions for the Счётная палата РФ feature.

Tools for accessing audit reports, budget execution data, and control measures.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client


async def spisok_napravleniy(ctx: Context) -> str:
    """Получить список направлений контрольной деятельности Счётной палаты.

    Returns:
        Список направлений контроля.
    """
    await ctx.info("Запрос списка направлений контроля...")
    napravleniya = client.get_napravleniya_list()

    rows = [(n["code"], n["name"]) for n in napravleniya]
    header = "**Направления контрольной деятельности Счётной палаты РФ**\n\n"
    return header + markdown_table(["Код", "Направление"], rows)


async def spisok_tipov_meropriyatiy(ctx: Context) -> str:
    """Получить список типов контрольных мероприятий.

    Returns:
        Список типов мероприятий.
    """
    await ctx.info("Запрос списка типов мероприятий...")
    tipy = client.get_tipy_meropriyatiy_list()

    rows = [(t["code"], t["name"]) for t in tipy]
    header = "**Типы контрольных мероприятий**\n\n"
    return header + markdown_table(["Код", "Тип"], rows)


async def spisok_subiektov_audita(ctx: Context) -> str:
    """Получить список субъектов внешнего государственного аудита.

    Returns:
        Список субъектов аудита.
    """
    await ctx.info("Запрос списка субъектов аудита...")
    subiekty = client.get_subiekty_audita_list()

    rows = [(s["code"], s["name"]) for s in subiekty]
    header = "**Субъекты внешнего государственного аудита**\n\n"
    return header + markdown_table(["Код", "Субъект"], rows)


async def info_kontrolnogo_meropriyatiya(nomer: str, ctx: Context) -> str:
    """Получить информацию о контрольном мероприятии по номеру.

    Args:
        nomer: Номер контрольного мероприятия.

    Returns:
        Информация о контрольном мероприятии.
    """
    await ctx.info(f"Запрос информации о контрольном мероприятии {nomer}...")
    data = await client.poluchit_kontrolnoe_meropriyatie(nomer)

    if not data:
        return (
            f"Контрольное мероприятие '{nomer}' не найдено.\n\n"
            f"Проверьте номер на официальном сайте Счётной палаты: ach.gov.ru"
        )

    lines = [
        f"**{data.nazvanie}** (№ {data.nomer})",
        f"- Тип: {data.tip}",
        f"- Направление: {data.napravlenie}",
    ]
    if data.data_nachala:
        lines.append(f"- Дата начала: {data.data_nachala}")
    if data.data_okonchaniya:
        lines.append(f"- Дата окончания: {data.data_okonchaniya}")
    if data.status:
        lines.append(f"- Статус: {data.status}")
    if data.obiem_sredstv:
        lines.append(f"- Объём средств: {format_number_ru(data.obiem_sredstv, 2)} {data.valyuta}")
    lines.append("- Источник: Счётная палата РФ (ach.gov.ru)")
    return "\n".join(lines)


async def info_auditorskogo_zaklyucheniya(nomer: str, ctx: Context) -> str:
    """Получить аудиторское заключение по номеру.

    Args:
        nomer: Номер аудиторского заключения.

    Returns:
        Аудиторское заключение.
    """
    await ctx.info(f"Запрос аудиторского заключения {nomer}...")
    data = await client.poluchit_auditorskoe_zaklyuchenie(nomer)

    if not data:
        return (
            f"Аудиторское заключение '{nomer}' не найдено.\n\n"
            f"Проверьте номер на официальном сайте Счётной палаты: ach.gov.ru"
        )

    lines = [
        f"**{data.nazvanie}** (№ {data.nomer})",
        f"- Дата публикации: {data.data_publikacii}",
        f"- Объект аудита: {data.obekt_audita}",
        f"- Направление: {data.napravlenie}",
        f"- Выявлено нарушений: {data.vyavleno_narusheniy}",
    ]
    if data.summa_narusheniy:
        lines.append(f"- Сумма нарушений: {format_number_ru(data.summa_narusheniy, 2)} руб.")
    if data.rekomendacii:
        lines.append(f"- Рекомендации: {', '.join(data.rekomendacii[:5])}")
    if data.ispolnenie:
        lines.append(f"- Исполнение: {data.ispolnenie}")
    lines.append("- Источник: Счётная палата РФ (ach.gov.ru)")
    return "\n".join(lines)


async def ispolnenie_byudzheta(period: str = "", ctx: Context | None = None) -> str:
    """Получить данные об исполнении федерального бюджета.

    Args:
        period: Период (например, '2024', '2024-Q1'). По умолчанию — последний доступный.

    Returns:
        Данные об исполнении бюджета.
    """
    data = await client.poluchit_byudzhet_ispolnenie(period)

    if not data:
        period_text = f" за период {period}" if period else ""
        return (
            f"Данные об исполнении федерального бюджета{period_text} недоступны.\n\n"
            f"Данные доступны на сайте Счётной палаты: ach.gov.ru/controls/budget"
        )

    lines = [
        f"**Исполнение федерального бюджета за {data.period}**",
    ]
    if data.dohody:
        lines.append(f"- Доходы: {format_number_ru(data.dohody, 2)} млрд руб.")
    if data.raskhody:
        lines.append(f"- Расходы: {format_number_ru(data.raskhody, 2)} млрд руб.")
    if data.deficit is not None:
        lines.append(f"- Дефицит: {format_number_ru(data.deficit, 2)} млрд руб.")
    lines.append("- Источник: Счётная палата РФ (ach.gov.ru)")
    return "\n".join(lines)


async def poisk_narusheniy(
    organizaciya: str = "",
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск выявленных нарушений по организации или типу.

    Args:
        organizaciya: Название организации (необязательно).
        tip: Тип нарушения (необязательно).

    Returns:
        Список выявленных нарушений.
    """
    narusheniya = await client.poluchit_narusheniya(organizaciya=organizaciya, tip=tip)

    if not narusheniya:
        filters = []
        if organizaciya:
            filters.append(f"организация: {organizaciya}")
        if tip:
            filters.append(f"тип: {tip}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Нарушения{filter_text} не найдены.\n\n"
            f"Данные доступны на сайте Счётной палаты: ach.gov.ru"
        )

    lines = [
        f"**Выявленные нарушения** — найдено: {len(narusheniya)}",
    ]
    for i, n in enumerate(narusheniya[:10], 1):
        line = f"{i}. {n.opisanie}"
        if n.summa:
            line += f" (сумма: {format_number_ru(n.summa, 2)} руб.)"
        if n.organizaciya:
            line += f" — {n.organizaciya}"
        lines.append(line)

    if len(narusheniya) > 10:
        lines.append(f"\n... и ещё {len(narusheniya) - 10} нарушений")

    lines.append("- Источник: Счётная палата РФ (ach.gov.ru)")
    return "\n".join(lines)
