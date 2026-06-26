"""Инструменты модуля Федерального казначейства.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client


async def spisok_vidov_byudzhetov(ctx: Context) -> str:
    """Получить список видов бюджетов бюджетной системы РФ."""
    await ctx.info("Запрос списка видов бюджетов...")
    vidy = client.poluchit_spisok_vidov_byudzhetov()
    rows = [(v["kod"], v["nazvanie"]) for v in vidy]
    header = "**Виды бюджетов бюджетной системы РФ**\n\n"
    return header + tablitsa_v_markdown(["Код", "Вид бюджета"], rows)


async def spisok_kategoriy_raskhodov(ctx: Context) -> str:
    """Получить список категорий расходов бюджета."""
    await ctx.info("Запрос списка категорий расходов...")
    kategorii = client.poluchit_spisok_kategoriy_raskhodov()
    rows = [(k["kod"], k["nazvanie"]) for k in kategorii]
    header = "**Категории расходов бюджета**\n\n"
    return header + tablitsa_v_markdown(["Код", "Категория"], rows)


async def ispolnenie_byudzheta(
    ctx: Context,
    god: int = 0,
    tip: str = "",
) -> str:
    """Получить данные об исполнении бюджета.

    Аргументы:
        god: Год (необязательно).
        tip: Тип бюджета (необязательно).

    Возвращает:
        Данные об исполнении бюджета.
    """
    await ctx.info("Запрос данных об исполнении бюджета...")
    data = await client.poluchit_ispolnenie_byudzheta(god=god, tip=tip)
    if not data:
        tip_text = f" ({tip})" if tip else ""
        god_text = f" за {god} год" if god else ""
        return (
            f"Данные об исполнении бюджета{tip_text}{god_text} недоступны.\n\n"
            f"Данные доступны на:\n"
            f"- Федеральное казначейство: roskazna.gov.ru\n"
            f"- Портал бюджетных данных: budget.gov.ru"
        )
    lines = [f"**Исполнение бюджета за {data.get('period', '')}**"]
    if data.get("tip"):
        lines.append(f"- Тип бюджета: {data['tip']}")
    if data.get("dohody"):
        lines.append(f"- Доходы: {formatirovat_chislo_ru(data['dohody'], 2)} млрд руб.")
    if data.get("raskhody"):
        lines.append(f"- Расходы: {formatirovat_chislo_ru(data['raskhody'], 2)} млрд руб.")
    if data.get("defitsit") is not None:
        lines.append(f"- Дефицит: {formatirovat_chislo_ru(data['defitsit'], 2)} млрд руб.")
    if data.get("sostoyanie"):
        lines.append(f"- Статус: {data['sostoyanie']}")
    lines.append(f"- Источник: {data.get('istochnik', 'budget.gov.ru')}")
    return "\n".join(lines)


async def poisk_uchastnikov_bp(
    ctx: Context,
    inn: str = "",
    nazvanie: str = "",
) -> str:
    """Поиск участников бюджетного процесса.

    Аргументы:
        inn: ИНН организации (необязательно).
        nazvanie: Название организации (необязательно).

    Возвращает:
        Список участников бюджетного процесса.
    """
    await ctx.info("Поиск участников бюджетного процесса...")
    uchastniki = await client.poisk_uchastnikov_bp(inn=inn, nazvanie=nazvanie)
    if not uchastniki:
        filters = []
        if inn:
            filters.append(f"ИНН: {inn}")
        if nazvanie:
            filters.append(f"название: {nazvanie}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Участники бюджетного процесса{filter_text} не найдены.\n\n"
            f"Реестр участников доступен на: roskazna.gov.ru"
        )
    rows = [
        (
            u.get("inn", ""),
            u.get("nazvanie", "")[:50],
            u.get("tip_uchastnika", ""),
            u.get("byudzhet", ""),
        )
        for u in uchastniki
    ]
    header = f"**Участники бюджетного процесса** — найдено: {len(uchastniki)}\n\n"
    return header + tablitsa_v_markdown(
        ["ИНН", "Название", "Тип", "Бюджет"],
        rows,
    )


async def poisk_uchrezhdeniy(
    ctx: Context,
    inn: str = "",
    nazvanie: str = "",
    tip: str = "",
) -> str:
    """Поиск учреждений в сводном реестре.

    Аргументы:
        inn: ИНН учреждения (необязательно).
        nazvanie: Название учреждения (необязательно).
        tip: Тип учреждения (необязательно).

    Возвращает:
        Список учреждений.
    """
    await ctx.info("Поиск учреждений...")
    uchrezhdeniya = await client.poisk_uchrezhdeniy(inn=inn, nazvanie=nazvanie, tip=tip)
    if not uchrezhdeniya:
        filters = []
        if inn:
            filters.append(f"ИНН: {inn}")
        if nazvanie:
            filters.append(f"название: {nazvanie}")
        if tip:
            filters.append(f"тип: {tip}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Учреждения{filter_text} не найдены.\n\n"
            f"Сводный реестр учреждений доступен на: roskazna.gov.ru"
        )
    rows = [
        (
            u.get("inn", ""),
            u.get("nazvanie", "")[:50],
            u.get("tip", ""),
            u.get("osnovnoj_vid_deyatelnosti", "")[:40],
        )
        for u in uchrezhdeniya
    ]
    header = f"**Учреждения** — найдено: {len(uchrezhdeniya)}\n\n"
    return header + tablitsa_v_markdown(
        ["ИНН", "Название", "Тип", "Основной вид деятельности"],
        rows,
    )


async def mezhbyudzhetnye_transferty(
    ctx: Context,
    god: int = 0,
    subiekt: str = "",
) -> str:
    """Получить данные о межбюджетных трансфертах.

    Аргументы:
        god: Год (необязательно).
        subiekt: Код региона (необязательно).

    Возвращает:
        Данные о межбюджетных трансфертах.
    """
    await ctx.info("Запрос данных о межбюджетных трансфертах...")
    transferty = await client.poluchit_mezhbyudzhetnye(god=god, subiekt=subiekt)
    if not transferty:
        god_text = f" за {god} год" if god else ""
        region_text = f", регион: {subiekt}" if subiekt else ""
        return (
            f"Межбюджетные трансферты{god_text}{region_text} не найдены.\n\n"
            f"Данные доступны на: budget.gov.ru"
        )
    rows = [
        (
            t.get("vid", ""),
            t.get("otpravitel", "")[:30],
            t.get("poluchatel", "")[:30],
            str(t.get("summa", "")),
            t.get("god", ""),
        )
        for t in transferty
    ]
    header = f"**Межбюджетные трансферты** — найдено: {len(transferty)}\n\n"
    return header + tablitsa_v_markdown(
        ["Вид", "Отправитель", "Получатель", "Сумма (руб.)", "Год"],
        rows,
    )
