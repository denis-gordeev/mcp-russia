"""Инструменты модуля Картотеки арбитражных дел.

Инструменты для поиска судебных дел, судебных актов, судей и сторон.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_rubli, tablitsa_v_markdown

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

    Аргументы:
        nomer: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        kategoriya: Категория дела.

    Возвращает:
        Результаты поиска дел.
    """
    if ctx:
        await ctx.info(f"Поиск дел: {nomer or istorcz or otvetchik or 'все'}...")

    dela = await client.poisk_del(
        nomer=nomer,
        istorcz=istorcz,
        otvetchik=otvetchik,
        inn=inn,
        kategoriya=kategoriya,
    )

    header = "**Картотека арбитражных дел**\n\n"

    filtry = []
    if nomer:
        filtry.append(f"Номер: {nomer}")
    if istorcz:
        filtry.append(f"Истец: {istorcz}")
    if otvetchik:
        filtry.append(f"Ответчик: {otvetchik}")
    if inn:
        filtry.append(f"ИНН: {inn}")
    if kategoriya:
        filtry.append(f"Категория: {kategoriya}")

    if filtry:
        header += "Фильтры: " + ", ".join(filtry) + "\n\n"

    if not dela:
        header += (
            "Дела не найдены.\n\n"
            "Источник: Картотека арбитражных дел (kad.arbitr.ru)\n"
            "Попробуйте уточнить параметры поиска."
        )
        return header

    stroki_tablitsy = []
    for d in dela[:20]:
        summa = formatirovat_rubli(d.summa_iska) if d.summa_iska > 0 else "—"
        stroki_tablitsy.append(
            (
                d.nomer,
                d.kategoriya or "—",
                d.sostoyanie or "—",
                d.nazvanie_suda or "—",
                summa,
            )
        )

    header += f"Найдено дел: {len(dela)}\n\n"
    header += tablitsa_v_markdown(
        ["Номер дела", "Категория", "Статус", "Суд", "Сумма иска"],
        stroki_tablitsy,
    )
    header += "\n\nИсточник: Картотека арбитражных дел (kad.arbitr.ru)"
    return header


async def info_dela(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить подробную информацию о судебном деле.

    Аргументы:
        nomer_dela: Номер дела (например, 'А40-12345/2024').

    Возвращает:
        Подробная информация о деле.
    """
    await ctx.info(f"Запрос информации о деле {nomer_dela}...")
    delo = await client.info_dela(nomer_dela)

    if not delo:
        return (
            f"Дело с номером {nomer_dela} не найдено в КАД.\n\nИспользуйте poisk_del() для поиска."
        )

    stroki = [
        f"**Дело {delo.nomer}**",
        f"- Категория: {delo.kategoriya}",
        f"- Статус: {delo.sostoyanie}",
        f"- Судья: {delo.sudya}",
        f"- Суд: {delo.nazvanie_suda}",
        f"- Дата возбуждения: {delo.data_vozbuzhdeniya}",
        f"- Последний акт: {delo.data_poslednego_akta}",
        f"- Истцы: {', '.join(delo.istorcy)}",
        f"- Ответчики: {', '.join(delo.otvetchiki)}",
    ]
    if delo.summa_iska > 0:
        stroki.append(f"- Сумма иска: {formatirovat_rubli(delo.summa_iska)}")
    return "\n".join(stroki)


async def akty_po_delu(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить судебные акты по делу.

    Аргументы:
        nomer_dela: Номер дела.

    Возвращает:
        Судебные акты по делу.
    """
    await ctx.info(f"Запрос актов по делу {nomer_dela}...")
    akty = await client.akty_po_delu(nomer_dela)

    if not akty:
        return (
            f"Судебные акты по делу {nomer_dela} не найдены.\n\n"
            f"Проверьте номер дела или используйте info_dela()."
        )

    stroki_tablitsy = [(a.tip_akta, a.data_akta, a.sud, a.rezolyutsiya[:50]) for a in akty]
    header = f"**Судебные акты по делу {nomer_dela}**\n\n"
    return header + tablitsa_v_markdown(["Тип акта", "Дата", "Суд", "Резолюция"], stroki_tablitsy)


async def storony_dela(
    nomer_dela: str,
    ctx: Context,
) -> str:
    """Получить стороны судебного дела.

    Аргументы:
        nomer_dela: Номер дела.

    Возвращает:
        Стороны дела (истцы и ответчики).
    """
    await ctx.info(f"Запрос сторон по делу {nomer_dela}...")
    storony = await client.storony_dela(nomer_dela)

    if not storony:
        return f"Стороны по делу {nomer_dela} не найдены.\n\nПроверьте номер дела."

    stroki = [f"**Стороны дела {nomer_dela}**\n"]
    for s in storony:
        stroki.append(f"- **{s.tip}**: {s.nazvanie}")
        if s.inn:
            stroki.append(f"  ИНН: {s.inn}")
        if s.subiekt:
            stroki.append(f"  Регион: {s.subiekt}")
    return "\n".join(stroki)


async def spravochnik_kategoriy(ctx: Context) -> str:
    """Получить справочник категорий дел.

    Возвращает:
        Категории дел.
    """
    await ctx.info("Запрос справочника категорий дел...")
    kategorii = client.poluchit_kategorii_del()

    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in kategorii]
    header = "**Категории арбитражных дел**\n\n"
    return header + tablitsa_v_markdown(["Код", "Категория"], stroki_tablitsy)


async def spravochnik_instantsiy(ctx: Context) -> str:
    """Получить справочник инстанций арбитражных судов.

    Возвращает:
        Инстанции судов.
    """
    await ctx.info("Запрос справочника инстанций судов...")
    instantsii = client.poluchit_instantsii()

    stroki_tablitsy = [(i["kod"], i["nazvanie"]) for i in instantsii]
    header = "**Инстанции арбитражных судов**\n\n"
    return header + tablitsa_v_markdown(["Код", "Инстанция"], stroki_tablitsy)


async def spravochnik_statusov(ctx: Context) -> str:
    """Получить справочник статусов дел.

    Возвращает:
        Статусы дел.
    """
    await ctx.info("Запрос справочника статусов дел...")
    statusy = client.poluchit_statusy_del()

    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in statusy]
    header = "**Статусы судебных дел**\n\n"
    return header + tablitsa_v_markdown(["Код", "Статус"], stroki_tablitsy)


async def spravochnik_aktov(ctx: Context) -> str:
    """Получить справочник типов судебных актов.

    Возвращает:
        Типы актов.
    """
    await ctx.info("Запрос справочника типов актов...")
    tipy = client.poluchit_tipy_aktov()

    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in tipy]
    header = "**Типы судебных актов**\n\n"
    return header + tablitsa_v_markdown(["Код", "Тип акта"], stroki_tablitsy)
