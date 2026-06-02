"""Tool functions for the Kad Arbitrazh (Картотека арбитражных дел) feature.

Tools for searching court cases, judicial acts, judges, and parties.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_rub, markdown_table

from . import client


async def poisk_del(
    nomer: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    kategoriya: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск дел в Картотеке арбитражных дел.

    Args:
        nomer: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        kategoriya: Категория дела.

    Returns:
        Результаты поиска дел.
    """
    if ctx:
        await ctx.info(f"Поиск дел: {nomer or istorcz or otvetchik or 'все'}...")

    dela = await client.poisk_del(
        number=nomer,
        istorcz=istorcz,
        otvetchik=otvetchik,
        inn=inn,
        category=kategoriya,
    )

    header = "**Картотека арбитражных дел**\n\n"

    filters = []
    if nomer:
        filters.append(f"Номер: {nomer}")
    if istorcz:
        filters.append(f"Истец: {istorcz}")
    if otvetchik:
        filters.append(f"Ответчик: {otvetchik}")
    if inn:
        filters.append(f"ИНН: {inn}")
    if kategoriya:
        filters.append(f"Категория: {kategoriya}")

    if filters:
        header += "Фильтры: " + ", ".join(filters) + "\n\n"

    if not dela:
        header += (
            "Дела не найдены.\n\n"
            "Источник: Картотека арбитражных дел (kad.arbitr.ru)\n"
            "Попробуйте уточнить параметры поиска."
        )
        return header

    rows = []
    for d in dela[:20]:
        summa = format_rub(d.summa_iska) if d.summa_iska > 0 else "—"
        rows.append(
            (
                d.number,
                d.category or "—",
                d.status or "—",
                d.sud_name or "—",
                summa,
            )
        )

    header += f"Найдено дел: {len(dela)}\n\n"
    header += markdown_table(
        ["Номер дела", "Категория", "Статус", "Суд", "Сумма иска"],
        rows,
    )
    header += "\n\nИсточник: Картотека арбитражных дел (kad.arbitr.ru)"
    return header


async def info_dela(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить подробную информацию о судебном деле.

    Args:
        nomer_dela: Номер дела (например, 'А40-12345/2024').

    Returns:
        Подробная информация о деле.
    """
    await ctx.info(f"Запрос информации о деле {nomer_dela}...")
    delo = await client.info_dela(nomer_dela)

    if not delo:
        return (
            f"Дело с номером {nomer_dela} не найдено в КАД.\n\nИспользуйте poisk_del() для поиска."
        )

    lines = [
        f"**Дело {delo.number}**",
        f"- Категория: {delo.category}",
        f"- Статус: {delo.status}",
        f"- Судья: {delo.sudya}",
        f"- Суд: {delo.sud_name}",
        f"- Дата возбуждения: {delo.data_vozbuzhdeniya}",
        f"- Последний акт: {delo.posledniy_akt_date}",
        f"- Истцы: {', '.join(delo.istorcy)}",
        f"- Ответчики: {', '.join(delo.otvetchiki)}",
    ]
    if delo.summa_iska > 0:
        lines.append(f"- Сумма иска: {format_rub(delo.summa_iska)}")
    return "\n".join(lines)


async def akty_po_delu(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить судебные акты по делу.

    Args:
        nomer_dela: Номер дела.

    Returns:
        Судебные акты по делу.
    """
    await ctx.info(f"Запрос актов по делу {nomer_dela}...")
    akty = await client.akty_po_delu(nomer_dela)

    if not akty:
        return (
            f"Судебные акты по делу {nomer_dela} не найдены.\n\n"
            f"Проверьте номер дела или используйте info_dela()."
        )

    rows = [(a.tip_akta, a.data_akta, a.sud, a.rezolyutsiya[:50]) for a in akty]
    header = f"**Судебные акты по делу {nomer_dela}**\n\n"
    return header + markdown_table(["Тип акта", "Дата", "Суд", "Резолюция"], rows)


async def storony_dela(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить стороны судебного дела.

    Args:
        nomer_dela: Номер дела.

    Returns:
        Стороны дела (истцы и ответчики).
    """
    await ctx.info(f"Запрос сторон по делу {nomer_dela}...")
    storony = await client.storony_dela(nomer_dela)

    if not storony:
        return f"Стороны по делу {nomer_dela} не найдены.\n\nПроверьте номер дела."

    lines = [f"**Стороны дела {nomer_dela}**\n"]
    for s in storony:
        lines.append(f"- **{s.tip}**: {s.name}")
        if s.inn:
            lines.append(f"  ИНН: {s.inn}")
        if s.region:
            lines.append(f"  Регион: {s.region}")
    return "\n".join(lines)


async def spravochnik_kategoriy(ctx: Context) -> str:
    """Получить справочник категорий дел.

    Returns:
        Категории дел.
    """
    await ctx.info("Запрос справочника категорий дел...")
    kategorii = client.get_kategorii_del()

    rows = [(k["code"], k["name"]) for k in kategorii]
    header = "**Категории арбитражных дел**\n\n"
    return header + markdown_table(["Код", "Категория"], rows)


async def spravochnik_instantsiy(ctx: Context) -> str:
    """Получить справочник инстанций арбитражных судов.

    Returns:
        Инстанции судов.
    """
    await ctx.info("Запрос справочника инстанций судов...")
    instantsii = client.get_instantsii()

    rows = [(i["code"], i["name"]) for i in instantsii]
    header = "**Инстанции арбитражных судов**\n\n"
    return header + markdown_table(["Код", "Инстанция"], rows)


async def spravochnik_statusov(ctx: Context) -> str:
    """Получить справочник статусов дел.

    Returns:
        Статусы дел.
    """
    await ctx.info("Запрос справочника статусов дел...")
    statusy = client.get_statusy_del()

    rows = [(s["code"], s["name"]) for s in statusy]
    header = "**Статусы судебных дел**\n\n"
    return header + markdown_table(["Код", "Статус"], rows)


async def spravochnik_aktov(ctx: Context) -> str:
    """Получить справочник типов судебных актов.

    Returns:
        Типы актов.
    """
    await ctx.info("Запрос справочника типов актов...")
    tipy = client.get_tipy_aktov()

    rows = [(t["code"], t["name"]) for t in tipy]
    header = "**Типы судебных актов**\n\n"
    return header + markdown_table(["Код", "Тип акта"], rows)
