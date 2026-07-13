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

_ISTOCHNIK_PRAVO = "\n\n_Источник: Официальный портал правовой информации (pravo.gov.ru)_"


async def spisok_tipov_aktov(kontekst: Context) -> str:
    """Получить список типов нормативных актов.

    Возвращает:
        Список типов актов.
    """
    await kontekst.info("Запрос списка типов актов...")
    tipy = client.poluchit_spisok_tipov_aktov()

    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in tipy]
    zagolovok = "**Типы нормативных актов РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy) + _ISTOCHNIK_PRAVO


async def spisok_otrasley(kontekst: Context) -> str:
    """Получить список отраслей законодательства.

    Возвращает:
        Список отраслей.
    """
    await kontekst.info("Запрос списка отраслей законодательства...")
    otrsli = client.poluchit_spisok_otrasley()

    stroki_tablitsy = [(o["kod"], o["nazvanie"]) for o in otrsli]
    zagolovok = "**Отрасли законодательства РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Отрасль"], stroki_tablitsy) + _ISTOCHNIK_PRAVO


async def spisok_istochnikov(kontekst: Context) -> str:
    """Получить список источников официальных публикаций.

    Возвращает:
        Список источников.
    """
    await kontekst.info("Запрос списка источников публикаций...")
    istochniki = client.poluchit_spisok_istochnikov()

    stroki_tablitsy = [(i["kod"], i["nazvanie"]) for i in istochniki]
    zagolovok = "**Источники официальных публикаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Источник"], stroki_tablitsy) + _ISTOCHNIK_PRAVO


async def spisok_statusov(kontekst: Context) -> str:
    """Получить список статусов документов.

    Возвращает:
        Список статусов.
    """
    await kontekst.info("Запрос списка статусов документов...")
    statusy = client.poluchit_spisok_statusov()

    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in statusy]
    zagolovok = "**Статусы документов**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Статус"], stroki_tablitsy) + _ISTOCHNIK_PRAVO


async def info_normativnogo_akta(
    nomer: str,
    tip: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить информацию о нормативном акте по номеру.

    Аргументы:
        nomer: Номер акта.
        tip: Тип акта (fz, ukaz, postanovlenie_pr и т.д.).

    Возвращает:
        Информация о нормативном акте.
    """
    if kontekst:
        await kontekst.info(f"Запрос информации о нормативном акте {nomer}...")
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
        f"- Отрасль: {dannye.otrasl}",
    ]
    if dannye.kratkoe_opisanie:
        stroki.append(f"- Описание: {dannye.kratkoe_opisanie}")
    if dannye.izmeneniya:
        stroki.append(f"- Изменений: {len(dannye.izmeneniya)}")
    if dannye.tekst_ssylka:
        stroki.append(f"- Текст: {dannye.tekst_ssylka}")
    stroki.append(f"- Источник: {dannye.istochnik}")
    stroki.append(_ISTOCHNIK_PRAVO.strip())
    return "\n".join(stroki)


async def info_zakonproekta(nomer: str, kontekst: Context | None = None) -> str:
    """Получить информацию о законопроекте по номеру.

    Аргументы:
        nomer: Номер законопроекта.

    Возвращает:
        Информация о законопроекте.
    """
    if kontekst:
        await kontekst.info(f"Запрос информации о законопроекте {nomer}...")
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
    stroki.append(_ISTOCHNIK_PRAVO.strip())
    return "\n".join(stroki)


async def poisk_aktov(
    tekst: str,
    tip: str = "",
    kontekst: Context | None = None,
) -> str:
    """Поиск нормативных актов по тексту.

    Аргументы:
        tekst: Текст для поиска.
        tip: Тип документа (необязательно).

    Возвращает:
        Результаты поиска.
    """
    if kontekst:
        await kontekst.info(f"Поиск актов: '{tekst}'...")
    rezultaty = await client.poluchit_poisku(tekst, tip)

    if not rezultaty:
        tip_tekst = f" (тип: {tip})" if tip else ""
        return (
            f"Нормативные акты по запросу '{tekst}'{tip_tekst} не найдены.\n\n"
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

    stroki.append(_ISTOCHNIK_PRAVO.strip())
    return "\n".join(stroki)


async def publikatsii_po_datam(
    tip: str = "",
    otrasl: str = "",
    data_s: str = "",
    data_po: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить публикации за период.

    Аргументы:
        tip: Тип документа (необязательно).
        otrasl: Отрасль законодательства (необязательно).
        data_s: Дата начала периода.
        data_po: Дата окончания периода.

    Возвращает:
        Список публикаций.
    """
    if kontekst:
        await kontekst.info("Запрос публикаций за период...")
    dannye = await client.poluchit_publikatsii(
        tip=tip, otrasl=otrasl, data_s=data_s, data_po=data_po
    )

    if not dannye:
        filtry = []
        if tip:
            filtry.append(f"тип: {tip}")
        if otrasl:
            filtry.append(f"отрасль: {otrasl}")
        if data_s:
            filtry.append(f"с {data_s}")
        if data_po:
            filtry.append(f"по {data_po}")
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

    stroki.append(_ISTOCHNIK_PRAVO.strip())
    return "\n".join(stroki)


async def izmeneniya_akta(akt_nomer: str, kontekst: Context | None = None) -> str:
    """Получить изменения нормативного акта.

    Аргументы:
        akt_nomer: Номер акта.

    Возвращает:
        Список изменений.
    """
    if kontekst:
        await kontekst.info(f"Запрос изменений акта {akt_nomer}...")
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

    stroki.append(_ISTOCHNIK_PRAVO.strip())
    return "\n".join(stroki)
