"""Инструменты модуля Счётной палаты РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client


async def spisok_napravleniy(ctx: Context) -> str:
    """Получить список направлений контрольной деятельности Счётной палаты."""
    await ctx.info("Запрос списка направлений контроля...")
    napravleniya = client.get_napravleniya_list()
    rows = [(n["code"], n["name"]) for n in napravleniya]
    header = "**Направления контрольной деятельности Счётной палаты РФ**\n\n"
    return header + markdown_table(["Код", "Направление"], rows)


async def spisok_tipov_meropriyatiy(ctx: Context) -> str:
    """Получить список типов контрольных мероприятий."""
    await ctx.info("Запрос списка типов мероприятий...")
    tipy = client.get_tipy_meropriyatiy_list()
    rows = [(t["code"], t["name"]) for t in tipy]
    header = "**Типы контрольных мероприятий**\n\n"
    return header + markdown_table(["Код", "Тип"], rows)


async def spisok_subiektov_audita(ctx: Context) -> str:
    """Получить список субъектов внешнего государственного аудита."""
    await ctx.info("Запрос списка субъектов аудита...")
    subiekty = client.get_subiekty_audita_list()
    rows = [(s["code"], s["name"]) for s in subiekty]
    header = "**Субъекты внешнего государственного аудита**\n\n"
    return header + markdown_table(["Код", "Субъект"], rows)


async def poisk_kontrolnyh_meropriyatiy(
    ctx: Context,
    napravlenie: str = "",
    status: str = "",
    god: int = 0,
) -> str:
    """Поиск контрольных мероприятий Счётной палаты.

    Args:
        napravlenie: Код направления контроля (необязательно).
        status: Статус мероприятия (необязательно).
        god: Год (необязательно).

    Returns:
        Список контрольных мероприятий.
    """
    await ctx.info("Поиск контрольных мероприятий...")
    meropriyatiya = await client.poisk_kontrolnyh_meropriyatiy(
        napravlenie=napravlenie,
        status=status,
        god=god,
    )
    if not meropriyatiya:
        return (
            "Контрольные мероприятия не найдены.\n\n"
            "Актуальные данные доступны на: https://ach.gov.ru/controls"
        )
    rows = [
        (
            m.get("nomer", ""),
            m.get("nazvanie", "")[:50],
            m.get("tip", ""),
            m.get("status", ""),
            str(m.get("obiem_sredstv", "")),
        )
        for m in meropriyatiya
    ]
    return markdown_table(
        ["№", "Название", "Тип", "Статус", "Объём средств"],
        rows,
    )


async def info_kontrolnogo_meropriyatiya(nomer: str, ctx: Context) -> str:
    """Получить информацию о контрольном мероприятии по номеру.

    Args:
        nomer: Номер мероприятия.

    Returns:
        Информация о мероприятии.
    """
    await ctx.info(f"Запрос информации о контрольном мероприятии {nomer}...")
    data = await client.poluchit_kontrolnoe_meropriyatie(nomer)
    if not data:
        return (
            f"Контрольное мероприятие '{nomer}' не найдено.\n\n"
            f"Проверьте номер на сайте Счётной палаты: ach.gov.ru"
        )
    lines = [
        f"**{data.get('nazvanie', '')}** (№ {data.get('nomer', nomer)})",
        f"- Тип: {data.get('tip', '')}",
        f"- Направление: {data.get('napravlenie', '')}",
    ]
    if data.get("data_nachala"):
        lines.append(f"- Дата начала: {data['data_nachala']}")
    if data.get("data_okonchaniya"):
        lines.append(f"- Дата окончания: {data['data_okonchaniya']}")
    if data.get("status"):
        lines.append(f"- Статус: {data['status']}")
    if data.get("obiem_sredstv"):
        lines.append(f"- Объём средств: {format_number_ru(data['obiem_sredstv'], 2)} руб.")
    lines.append(f"- Источник: {data.get('istochnik', 'ach.gov.ru')}")
    return "\n".join(lines)


async def info_auditorskogo_zaklyucheniya(nomer: str, ctx: Context) -> str:
    """Получить аудиторское заключение по номеру.

    Args:
        nomer: Номер заключения.

    Returns:
        Информация о заключении.
    """
    await ctx.info(f"Запрос аудиторского заключения {nomer}...")
    data = await client.poluchit_auditorskoe_zaklyuchenie(nomer)
    if not data:
        return (
            f"Аудиторское заключение '{nomer}' не найдено.\n\n"
            f"Проверьте номер на сайте Счётной палаты: ach.gov.ru"
        )
    lines = [
        f"**{data.get('nazvanie', '')}** (№ {data.get('nomer', nomer)})",
        f"- Дата публикации: {data.get('data_publikacii', '')}",
        f"- Объект аудита: {data.get('obekt_audita', '')}",
        f"- Направление: {data.get('napravlenie', '')}",
        f"- Выявлено нарушений: {data.get('vyavleno_narusheniy', 0)}",
    ]
    if data.get("summa_narusheniy"):
        lines.append(f"- Сумма нарушений: {format_number_ru(data['summa_narusheniy'], 2)} руб.")
    rekomendacii = data.get("rekomendacii", [])
    if rekomendacii:
        lines.append(f"- Рекомендации: {', '.join(str(r)[:80] for r in rekomendacii[:5])}")
    if data.get("ispolnenie"):
        lines.append(f"- Исполнение: {data['ispolnenie']}")
    lines.append(f"- Источник: {data.get('istochnik', 'ach.gov.ru')}")
    return "\n".join(lines)


async def ispolnenie_byudzheta(ctx: Context, period: str = "") -> str:
    """Получить данные об исполнении федерального бюджета.

    Args:
        period: Период (год, например '2025').

    Returns:
        Данные об исполнении бюджета.
    """
    await ctx.info("Запрос данных об исполнении бюджета...")
    data = await client.poluchit_byudzhet_ispolnenie(period)
    if not data:
        period_text = f" за период {period}" if period else ""
        return (
            f"Данные об исполнении федерального бюджета{period_text} недоступны.\n\n"
            f"Данные доступны на:\n"
            f"- Счётная палата: ach.gov.ru/controls/budget\n"
            f"- Портал бюджетных данных: budget.gov.ru"
        )
    lines = [f"**Исполнение федерального бюджета за {data.get('period', '')}**"]
    if data.get("dohody"):
        lines.append(f"- Доходы: {format_number_ru(data['dohody'], 2)} млрд руб.")
    if data.get("raskhody"):
        lines.append(f"- Расходы: {format_number_ru(data['raskhody'], 2)} млрд руб.")
    if data.get("deficit") is not None:
        lines.append(f"- Дефицит: {format_number_ru(data['deficit'], 2)} млрд руб.")
    lines.append(f"- Источник: {data.get('istochnik', 'budget.gov.ru')}")
    return "\n".join(lines)


async def poisk_narusheniy(
    ctx: Context,
    organizaciya: str = "",
    tip: str = "",
    god: int = 0,
) -> str:
    """Поиск выявленных нарушений по организации или типу.

    Args:
        organizaciya: Название организации (необязательно).
        tip: Тип нарушения (необязательно).
        god: Год (необязательно).

    Returns:
        Список выявленных нарушений.
    """
    await ctx.info("Поиск нарушений...")
    narusheniya = await client.poisk_narusheniy(
        organizaciya=organizaciya,
        tip=tip,
        god=god,
    )
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
    rows = [
        (
            n.get("organizaciya", ""),
            n.get("tip_narusheniya", ""),
            n.get("opisanie", "")[:60],
            str(n.get("summa", "")),
        )
        for n in narusheniya
    ]
    header = f"**Выявленные нарушения** — найдено: {len(narusheniya)}\n\n"
    return header + markdown_table(
        ["Организация", "Тип", "Описание", "Сумма (руб.)"],
        rows,
    )
