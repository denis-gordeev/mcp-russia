"""Инструменты модуля Официальные публикации РФ.

Инструменты для доступа к нормативным актам, законопроектам, публикациям и поправкам
с Официального портала правовой информации (pravo.gov.ru).

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client

_PRAVO_ATTRIBUTION = "\n\n_Источник: Официальный портал правовой информации (pravo.gov.ru)_"


async def spisok_tipov_aktov(ctx: Context) -> str:
    """Получить список типов нормативных актов.

    Возвращает:
        Список типов актов.
    """
    await ctx.info("Запрос списка типов актов...")
    tipy = client.poluchit_spisok_tipov_aktov()

    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in tipy]
    zagolovok = "**Типы нормативных актов РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy) + _PRAVO_ATTRIBUTION


async def spisok_otrasley(ctx: Context) -> str:
    """Получить список отраслей законодательства.

    Возвращает:
        Список отраслей.
    """
    await ctx.info("Запрос списка отраслей законодательства...")
    otrsli = client.poluchit_spisok_otrasley()

    stroki_tablitsy = [(o["kod"], o["nazvanie"]) for o in otrsli]
    zagolovok = "**Отрасли законодательства РФ**\n\n"
    return (
        zagolovok + tablitsa_v_markdown(["Код", "Отрасль"], stroki_tablitsy) + _PRAVO_ATTRIBUTION
    )


async def spisok_istochnikov(ctx: Context) -> str:
    """Получить список источников официальных публикаций.

    Возвращает:
        Список источников.
    """
    await ctx.info("Запрос списка источников публикаций...")
    istochniki = client.poluchit_spisok_istochnikov()

    stroki_tablitsy = [(i["kod"], i["nazvanie"]) for i in istochniki]
    zagolovok = "**Источники официальных публикаций**\n\n"
    return (
        zagolovok + tablitsa_v_markdown(["Код", "Источник"], stroki_tablitsy) + _PRAVO_ATTRIBUTION
    )


async def spisok_statusov(ctx: Context) -> str:
    """Получить список статусов документов.

    Возвращает:
        Список статусов.
    """
    await ctx.info("Запрос списка статусов документов...")
    statusy = client.poluchit_spisok_statusov()

    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in statusy]
    zagolovok = "**Статусы документов**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Статус"], stroki_tablitsy) + _PRAVO_ATTRIBUTION


async def info_normativnogo_akta(
    nomer: str,
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить информацию о нормативном акте по номеру.

    Аргументы:
        nomer: Номер акта.
        tip: Тип акта (fz, ukaz, postanovlenie_pr и т.д.).

    Возвращает:
        Информация о нормативном акте.
    """
    if ctx:
        await ctx.info(f"Запрос информации о нормативном акте {nomer}...")
    dannye = await client.poluchit_normativnyy_akt(nomer, tip)

    if not dannye:
        return (
            f"Нормативный акт '{nomer}' не найден.\n\n"
            f"Проверьте номер на портале: https://pravo.gov.ru/opendata/7700748144-prfgi"
        )

    stroki = [
        f"**{dannye.nazvanie}**",
        f"- Номер: {dannye.nomer}",
        f"- Тип: {dannye.tip}",
        f"- Дата принятия: {dannye.data_prinyatiya}",
        f"- Статус: {dannye.sostoyanie}",
        f"- Отрасль: {dannye.otrysl}",
    ]
    if dannye.kratkoe_opisanie:
        stroki.append(f"- Описание: {dannye.kratkoe_opisanie}")
    if dannye.izmeneniya:
        stroki.append(f"- Изменений: {len(dannye.izmeneniya)}")
    if dannye.tekst_ssylka:
        stroki.append(f"- Текст: {dannye.tekst_ssylka}")
    stroki.append(f"- Источник: {dannye.istochnik}")
    stroki.append(_PRAVO_ATTRIBUTION.strip())
    return "\n".join(stroki)


async def info_zakonproekta(nomer: str, ctx: Context | None = None) -> str:
    """Получить информацию о законопроекте по номеру.

    Аргументы:
        nomer: Номер законопроекта.

    Возвращает:
        Информация о законопроекте.
    """
    if ctx:
        await ctx.info(f"Запрос информации о законопроекте {nomer}...")
    dannye = await client.poluchit_zakon_proekt(nomer)

    if not dannye:
        return f"Законопроект '{nomer}' не найден.\n\nПроверьте на https://sozd.duma.gov.ru или https://pravo.gov.ru"

    stroki = [
        f"**{dannye.nazvanie}**",
        f"- Номер: {dannye.nomer}",
        f"- Стадия: {dannye.stadnya}",
        f"- Дата внесения: {dannye.data_vneseniya}",
        f"- Субъект внесения: {dannye.vnesen_subiekt}",
        f"- Ответственный комитет: {dannye.otvetstvennyy_komitet}",
    ]
    if dannye.chteniya:
        stroki.append(f"- Чтений: {len(dannye.chteniya)}")
    if dannye.tekst_ssylka:
        stroki.append(f"- Текст: {dannye.tekst_ssylka}")
    stroki.append(_PRAVO_ATTRIBUTION.strip())
    return "\n".join(stroki)


async def poisk_aktov(
    tekst: str,
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск нормативных актов по тексту.

    Аргументы:
        tekst: Текст для поиска.
        tip: Тип документа (необязательно).

    Возвращает:
        Результаты поиска.
    """
    if ctx:
        await ctx.info(f"Поиск актов: '{tekst}'...")
    rezultaty = await client.poluchit_poisku(tekst, tip)

    if not rezultaty:
        tip_text = f" (тип: {tip})" if tip else ""
        return (
            f"Нормативные акты по запросу '{tekst}'{tip_text} не найдены.\n\n"
            f"Попробуйте изменить запрос или используйте https://pravo.gov.ru/opendata/7700748144-prfgi"
        )

    stroki = [f"**Результаты поиска: '{tekst}'** — найдено: {len(rezultaty)}\n"]
    for i, a in enumerate(rezultaty[:10], 1):
        stroki.append(f"{i}. **{a.nazvanie}** ({a.tip})")
        stroki.append(f"   № {a.nomer}, статус: {a.sostoyanie}")
        if a.kratkoe_opisanie:
            stroki.append(f"   {a.kratkoe_opisanie}")
        stroki.append("")

    if len(rezultaty) > 10:
        stroki.append(f"\n... и ещё {len(rezultaty) - 10} результатов")

    stroki.append(_PRAVO_ATTRIBUTION.strip())
    return "\n".join(stroki)


async def publikatsii_po_datam(
    tip: str = "",
    otrysl: str = "",
    data_from: str = "",
    data_to: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить публикации за период.

    Аргументы:
        tip: Тип документа (необязательно).
        otrysl: Отрасль законодательства (необязательно).
        data_from: Дата начала периода.
        data_to: Дата окончания периода.

    Возвращает:
        Список публикаций.
    """
    if ctx:
        await ctx.info("Запрос публикаций за период...")
    dannye = await client.poluchit_publikatsii(
        tip=tip, otrysl=otrysl, data_from=data_from, data_to=data_to
    )

    if not dannye:
        filtry = []
        if tip:
            filtry.append(f"тип: {tip}")
        if otrysl:
            filtry.append(f"отрасль: {otrysl}")
        if data_from:
            filtry.append(f"с {data_from}")
        if data_to:
            filtry.append(f"по {data_to}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Публикации{tekst_filtra} не найдены.\n\n"
            f"Публикации доступны на https://pravo.gov.ru/opendata/7700748144-prfgi"
        )

    stroki = [f"**Официальные публикации** — найдено: {len(dannye)}\n"]
    for p in dannye[:10]:
        stroki.append(f"- **{p.nazvanie}** ({p.tip_dokumenta})")
        stroki.append(f"  Дата: {p.data_publikatsii}, источник: {p.istochnik}")
        if p.annotaciya:
            stroki.append(f"  {p.annotaciya}")
        stroki.append("")

    if len(dannye) > 10:
        stroki.append(f"\n... и ещё {len(dannye) - 10} публикаций")

    stroki.append(_PRAVO_ATTRIBUTION.strip())
    return "\n".join(stroki)


async def izmeneniya_akta(akt_nomer: str, ctx: Context | None = None) -> str:
    """Получить изменения нормативного акта.

    Аргументы:
        akt_nomer: Номер акта.

    Возвращает:
        Список изменений.
    """
    if ctx:
        await ctx.info(f"Запрос изменений акта {akt_nomer}...")
    dannye = await client.poluchit_izmeneniya_akta(akt_nomer)

    if not dannye:
        return (
            f"Изменений акта '{akt_nomer}' не найдено.\n\n"
            f"Проверьте номер акта на https://pravo.gov.ru/opendata/7700748144-prfgi"
        )

    stroki = [f"**Изменения акта {akt_nomer}** — изменений: {len(dannye)}\n"]
    for izm in dannye:
        stroki.append(f"- {izm.izmenenie_nomer} ({izm.izmenenie_data})")
        stroki.append(f"  {izm.izmenenie_opisanie}")
        if izm.data_vstupleniya_v_silu:
            stroki.append(f"  Вступил в силу: {izm.data_vstupleniya_v_silu}")
        stroki.append("")

    stroki.append(_PRAVO_ATTRIBUTION.strip())
    return "\n".join(stroki)
