"""Инструменты модуля Счётной палаты РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client


async def spisok_napravleniy(ctx: Context) -> str:
    """Получить список направлений контрольной деятельности Счётной палаты."""
    await ctx.info("Запрос списка направлений контроля...")
    napravleniya = client.poluchit_spisok_napravleniy()
    stroki_tablitsy = [(n["kod"], n["nazvanie"]) for n in napravleniya]
    zagolovok = "**Направления контрольной деятельности Счётной палаты РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Направление"], stroki_tablitsy)


async def spisok_tipov_meropriyatiy(ctx: Context) -> str:
    """Получить список типов контрольных мероприятий."""
    await ctx.info("Запрос списка типов мероприятий...")
    tipy = client.poluchit_spisok_tipov_meropriyatiy()
    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in tipy]
    zagolovok = "**Типы контрольных мероприятий**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy)


async def spisok_subiektov_audita(ctx: Context) -> str:
    """Получить список субъектов внешнего государственного аудита."""
    await ctx.info("Запрос списка субъектов аудита...")
    subiekty = client.poluchit_spisok_subiektov_audita()
    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in subiekty]
    zagolovok = "**Субъекты внешнего государственного аудита**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Субъект"], stroki_tablitsy)


async def poisk_kontrolnyh_meropriyatiy(
    ctx: Context,
    napravlenie: str = "",
    sostoyanie: str = "",
    god: int = 0,
) -> str:
    """Поиск контрольных мероприятий Счётной палаты.

    Аргументы:
        napravlenie: Код направления контроля (необязательно).
        sostoyanie: Статус мероприятия (необязательно).
        god: Год (необязательно).

    Возвращает:
        Список контрольных мероприятий.
    """
    await ctx.info("Поиск контрольных мероприятий...")
    meropriyatiya = await client.poisk_kontrolnyh_meropriyatiy(
        napravlenie=napravlenie,
        sostoyanie=sostoyanie,
        god=god,
    )
    if not meropriyatiya:
        return (
            "Контрольные мероприятия не найдены.\n\n"
            "Актуальные данные доступны на: https://ach.gov.ru/controls"
        )
    stroki_tablitsy = [
        (
            m.get("nomer", ""),
            m.get("nazvanie", "")[:50],
            m.get("tip", ""),
            m.get("sostoyanie", ""),
            str(m.get("obiem_sredstv", "")),
        )
        for m in meropriyatiya
    ]
    return tablitsa_v_markdown(
        ["№", "Название", "Тип", "Статус", "Объём средств"],
        stroki_tablitsy,
    )


async def info_kontrolnogo_meropriyatiya(nomer: str, ctx: Context) -> str:
    """Получить информацию о контрольном мероприятии по номеру.

    Аргументы:
        nomer: Номер мероприятия.

    Возвращает:
        Информация о мероприятии.
    """
    await ctx.info(f"Запрос информации о контрольном мероприятии {nomer}...")
    dannye = await client.poluchit_kontrolnoe_meropriyatie(nomer)
    if not dannye:
        return (
            f"Контрольное мероприятие '{nomer}' не найдено.\n\n"
            f"Проверьте номер на сайте Счётной палаты: ach.gov.ru"
        )
    stroki = [
        f"**{dannye.get('nazvanie', '')}** (№ {dannye.get('nomer', nomer)})",
        f"- Тип: {dannye.get('tip', '')}",
        f"- Направление: {dannye.get('napravlenie', '')}",
    ]
    if dannye.get("data_nachala"):
        stroki.append(f"- Дата начала: {dannye['data_nachala']}")
    if dannye.get("data_okonchaniya"):
        stroki.append(f"- Дата окончания: {dannye['data_okonchaniya']}")
    if dannye.get("sostoyanie"):
        stroki.append(f"- Статус: {dannye['sostoyanie']}")
    if dannye.get("obiem_sredstv"):
        stroki.append(
            f"- Объём средств: {formatirovat_chislo_ru(dannye['obiem_sredstv'], 2)} руб."
        )
    stroki.append(f"- Источник: {dannye.get('istochnik', 'ach.gov.ru')}")
    return "\n".join(stroki)


async def info_auditorskogo_zaklyucheniya(nomer: str, ctx: Context) -> str:
    """Получить аудиторское заключение по номеру.

    Аргументы:
        nomer: Номер заключения.

    Возвращает:
        Информация о заключении.
    """
    await ctx.info(f"Запрос аудиторского заключения {nomer}...")
    dannye = await client.poluchit_auditorskoe_zaklyuchenie(nomer)
    if not dannye:
        return (
            f"Аудиторское заключение '{nomer}' не найдено.\n\n"
            f"Проверьте номер на сайте Счётной палаты: ach.gov.ru"
        )
    stroki = [
        f"**{dannye.get('nazvanie', '')}** (№ {dannye.get('nomer', nomer)})",
        f"- Дата публикации: {dannye.get('data_publikacii', '')}",
        f"- Объект аудита: {dannye.get('obekt_audita', '')}",
        f"- Направление: {dannye.get('napravlenie', '')}",
        f"- Выявлено нарушений: {dannye.get('vyavleno_narusheniy', 0)}",
    ]
    if dannye.get("summa_narusheniy"):
        stroki.append(
            f"- Сумма нарушений: {formatirovat_chislo_ru(dannye['summa_narusheniy'], 2)} руб."
        )
    rekomendacii = dannye.get("rekomendacii", [])
    if rekomendacii:
        stroki.append(f"- Рекомендации: {', '.join(str(r)[:80] for r in rekomendacii[:5])}")
    if dannye.get("ispolnenie"):
        stroki.append(f"- Исполнение: {dannye['ispolnenie']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'ach.gov.ru')}")
    return "\n".join(stroki)


async def ispolnenie_byudzheta(ctx: Context, period: str = "") -> str:
    """Получить данные об исполнении федерального бюджета.

    Аргументы:
        period: Период (год, например '2025').

    Возвращает:
        Данные об исполнении бюджета.
    """
    await ctx.info("Запрос данных об исполнении бюджета...")
    dannye = await client.poluchit_byudzhet_ispolnenie(period)
    if not dannye:
        period_tekst = f" за период {period}" if period else ""
        return (
            f"Данные об исполнении федерального бюджета{period_tekst} недоступны.\n\n"
            f"Данные доступны на:\n"
            f"- Счётная палата: ach.gov.ru/controls/budget\n"
            f"- Портал бюджетных данных: budget.gov.ru"
        )
    stroki = [f"**Исполнение федерального бюджета за {dannye.get('period', '')}**"]
    if dannye.get("dohody"):
        stroki.append(f"- Доходы: {formatirovat_chislo_ru(dannye['dohody'], 2)} млрд руб.")
    if dannye.get("raskhody"):
        stroki.append(f"- Расходы: {formatirovat_chislo_ru(dannye['raskhody'], 2)} млрд руб.")
    if dannye.get("defitsit") is not None:
        stroki.append(f"- Дефицит: {formatirovat_chislo_ru(dannye['defitsit'], 2)} млрд руб.")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'budget.gov.ru')}")
    return "\n".join(stroki)


async def poisk_narusheniy(
    ctx: Context,
    organizaciya: str = "",
    tip: str = "",
    god: int = 0,
) -> str:
    """Поиск выявленных нарушений по организации или типу.

    Аргументы:
        organizaciya: Название организации (необязательно).
        tip: Тип нарушения (необязательно).
        god: Год (необязательно).

    Возвращает:
        Список выявленных нарушений.
    """
    await ctx.info("Поиск нарушений...")
    narusheniya = await client.poisk_narusheniy(
        organizaciya=organizaciya,
        tip=tip,
        god=god,
    )
    if not narusheniya:
        filtry = []
        if organizaciya:
            filtry.append(f"организация: {organizaciya}")
        if tip:
            filtry.append(f"тип: {tip}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Нарушения{tekst_filtra} не найдены.\n\n"
            f"Данные доступны на сайте Счётной палаты: ach.gov.ru"
        )
    stroki_tablitsy = [
        (
            n.get("organizaciya", ""),
            n.get("tip_narusheniya", ""),
            n.get("opisanie", "")[:60],
            str(n.get("summa", "")),
        )
        for n in narusheniya
    ]
    zagolovok = f"**Выявленные нарушения** — найдено: {len(narusheniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Организация", "Тип", "Описание", "Сумма (руб.)"],
        stroki_tablitsy,
    )
