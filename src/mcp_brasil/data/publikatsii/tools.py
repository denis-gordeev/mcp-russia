"""Tool functions for the Официальные публикации РФ feature.

Tools for accessing legal acts, bills, publications, and amendments.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import markdown_table

from . import client


async def spisok_tipov_aktov(ctx: Context) -> str:
    """Получить список типов нормативных актов.

    Returns:
        Список типов актов.
    """
    await ctx.info("Запрос списка типов актов...")
    tipy = client.get_tipy_aktov_list()

    rows = [(t["code"], t["name"]) for t in tipy]
    header = "**Типы нормативных актов РФ**\n\n"
    return header + markdown_table(["Код", "Тип"], rows)


async def spisok_otrasley(ctx: Context) -> str:
    """Получить список отраслей законодательства.

    Returns:
        Список отраслей.
    """
    await ctx.info("Запрос списка отраслей законодательства...")
    otrsli = client.get_otrasli_list()

    rows = [(o["code"], o["name"]) for o in otrsli]
    header = "**Отрасли законодательства РФ**\n\n"
    return header + markdown_table(["Код", "Отрасль"], rows)


async def spisok_istochnikov(ctx: Context) -> str:
    """Получить список источников официальных публикаций.

    Returns:
        Список источников.
    """
    await ctx.info("Запрос списка источников публикаций...")
    istochniki = client.get_istochniki_list()

    rows = [(i["code"], i["name"]) for i in istochniki]
    header = "**Источники официальных публикаций**\n\n"
    return header + markdown_table(["Код", "Источник"], rows)


async def spisok_statusov(ctx: Context) -> str:
    """Получить список статусов документов.

    Returns:
        Список статусов.
    """
    await ctx.info("Запрос списка статусов документов...")
    statusy = client.get_statusy_list()

    rows = [(s["code"], s["name"]) for s in statusy]
    header = "**Статусы документов**\n\n"
    return header + markdown_table(["Код", "Статус"], rows)


async def info_normativnogo_akta(
    nomer: str,
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить информацию о нормативном акте по номеру.

    Args:
        nomer: Номер акта.
        tip: Тип акта (fz, ukaz, postanovlenie_pr и т.д.).

    Returns:
        Информация о нормативном акте.
    """
    await ctx.info(f"Запрос информации о нормативном акте {nomer}...")
    data = await client.poluchit_normativnyy_akt(nomer, tip)

    if not data:
        return (
            f"Нормативный акт '{nomer}' не найден.\n\n"
            f"Проверьте номер на официальном портале: pravo.gov.ru"
        )

    lines = [
        f"**{data.nazvanie}**",
        f"- Номер: {data.nomer}",
        f"- Тип: {data.tip}",
        f"- Дата принятия: {data.data_prinyatiya}",
        f"- Статус: {data.status}",
        f"- Отрасль: {data.otrysl}",
    ]
    if data.kratkoe_opisanie:
        lines.append(f"- Описание: {data.kratkoe_opisanie}")
    if data.izmeneniya:
        lines.append(f"- Изменений: {len(data.izmeneniya)}")
    if data.tekst_url:
        lines.append(f"- Текст: {data.tekst_url}")
    lines.append(f"- Источник: {data.istochnik}")
    return "\n".join(lines)


async def info_zakonproekta(nomer: str, ctx: Context | None = None) -> str:
    """Получить информацию о законопроекте по номеру.

    Args:
        nomer: Номер законопроекта.

    Returns:
        Информация о законопроекте.
    """
    await ctx.info(f"Запрос информации о законопроекте {nomer}...")
    data = await client.poluchit_zakon_proekt(nomer)

    if not data:
        return (
            f"Законопроект '{nomer}' не найден.\n\n"
            f"Проверьте номер на сайте sozd.duma.gov.ru"
        )

    lines = [
        f"**{data.nazvanie}**",
        f"- Номер: {data.nomer}",
        f"- Стадия: {data.stadnya}",
        f"- Дата внесения: {data.data_vneseniya}",
        f"- Субъект внесения: {data.vnesen_subiekt}",
        f"- Ответственный комитет: {data.otvetstvennyy_komitet}",
    ]
    if data.chteniya:
        lines.append(f"- Чтений: {len(data.chteniya)}")
    if data.tekst_url:
        lines.append(f"- Текст: {data.tekst_url}")
    return "\n".join(lines)


async def poisk_aktov(
    tekst: str,
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск нормативных актов по тексту.

    Args:
        tekst: Текст для поиска.
        tip: Тип документа (необязательно).

    Returns:
        Результаты поиска.
    """
    await ctx.info(f"Поиск актов: '{tekst}'...")
    results = await client.poluchit_poisku(tekst, tip)

    if not results:
        tip_text = f" (тип: {tip})" if tip else ""
        return (
            f"Нормативные акты по запросу '{tekst}'{tip_text} не найдены.\n\n"
            f"Попробуйте изменить запрос или используйте pravo.gov.ru"
        )

    lines = [f"**Результаты поиска: '{tekst}'** — найдено: {len(results)}\n"]
    for i, a in enumerate(results[:10], 1):
        lines.append(f"{i}. **{a.nazvanie}** ({a.tip})")
        lines.append(f"   № {a.nomer}, статус: {a.status}")
        if a.kratkoe_opisanie:
            lines.append(f"   {a.kratkoe_opisanie}")
        lines.append("")

    if len(results) > 10:
        lines.append(f"\n... и ещё {len(results) - 10} результатов")

    return "\n".join(lines)


async def publikatsii_po_datam(
    tip: str = "",
    otrysl: str = "",
    data_from: str = "",
    data_to: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить публикации за период.

    Args:
        tip: Тип документа (необязательно).
        otrysl: Отрасль законодательства (необязательно).
        data_from: Дата начала периода.
        data_to: Дата окончания периода.

    Returns:
        Список публикаций.
    """
    await ctx.info("Запрос публикаций за период...")
    data = await client.poluchit_publikatsii(
        tip=tip, otrysl=otrysl, data_from=data_from, data_to=data_to
    )

    if not data:
        filters = []
        if tip:
            filters.append(f"тип: {tip}")
        if otrysl:
            filters.append(f"отрасль: {otrysl}")
        if data_from:
            filters.append(f"с {data_from}")
        if data_to:
            filters.append(f"по {data_to}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Публикации{filter_text} не найдены.\n\n"
            f"Публикации доступны на портале pravo.gov.ru"
        )

    lines = [f"**Официальные публикации** — найдено: {len(data)}\n"]
    for p in data[:10]:
        lines.append(f"- **{p.nazvanie}** ({p.tip_dokumenta})")
        lines.append(f"  Дата: {p.data_publikatsii}, источник: {p.istochnik}")
        if p.annotaciya:
            lines.append(f"  {p.annotaciya}")
        lines.append("")

    if len(data) > 10:
        lines.append(f"\n... и ещё {len(data) - 10} публикаций")

    return "\n".join(lines)


async def izmeneniya_akta(akt_nomer: str, ctx: Context | None = None) -> str:
    """Получить изменения нормативного акта.

    Args:
        akt_nomer: Номер акта.

    Returns:
        Список изменений.
    """
    await ctx.info(f"Запрос изменений акта {akt_nomer}...")
    data = await client.poluchit_izmeneniya_akta(akt_nomer)

    if not data:
        return (
            f"Изменений акта '{akt_nomer}' не найдено.\n\n"
            f"Проверьте номер акта на портале pravo.gov.ru"
        )

    lines = [f"**Изменения акта {akt_nomer}** — изменений: {len(data)}\n"]
    for izm in data:
        lines.append(f"- {izm.izmenenie_nomer} ({izm.izmenenie_data})")
        lines.append(f"  {izm.izmenenie_opisanie}")
        if izm.data_vstupleniya_v_silu:
            lines.append(f"  Вступил в силу: {izm.data_vstupleniya_v_silu}")
        lines.append("")

    return "\n".join(lines)
