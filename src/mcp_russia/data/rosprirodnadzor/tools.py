"""Инструменты модуля Росприроднадзора.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_vidov_nadzora(ctx: Context) -> str:
    """Получить список видов государственного надзора Росприроднадзора."""
    await ctx.info("Запрос списка видов надзора...")
    vidy = client.poluchit_spisok_vidov_nadzora()
    stroki_tablitsy = [(v["kod"], v["nazvanie"]) for v in vidy]
    zagolovok = "**Виды государственного надзора Росприроднадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид надзора"], stroki_tablitsy)


async def spisok_kategoriy_obnv(ctx: Context) -> str:
    """Получить список категорий объектов негативного воздействия."""
    await ctx.info("Запрос списка категорий ОНВ...")
    kategorii = client.poluchit_spisok_kategoriy_obnv()
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in kategorii]
    zagolovok = "**Категории объектов негативного воздействия (ОНВ)**\n\n"
    return zagolovok + tablitsa_v_markdown(["Категория", "Описание"], stroki_tablitsy)


async def spisok_vidov_litsenziy_nedra(ctx: Context) -> str:
    """Получить список видов лицензий на пользование недрами."""
    await ctx.info("Запрос списка видов лицензий...")
    vidy = client.poluchit_spisok_vidov_litsenziy_nedra()
    stroki_tablitsy = [(v["kod"], v["nazvanie"]) for v in vidy]
    zagolovok = "**Виды лицензий на пользование недрами**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид лицензии"], stroki_tablitsy)


async def poisk_proverok(
    ctx: Context,
    organizaciya: str = "",
    vid_nadzora: str = "",
    god: int = 0,
) -> str:
    """Поиск экологических проверок Росприроднадзора.

    Аргументы:
        organizaciya: Название организации (необязательно).
        vid_nadzora: Вид надзора (необязательно).
        god: Год (необязательно).

    Возвращает:
        Список проверок.
    """
    await ctx.info("Поиск экологических проверок...")
    proverki = await client.poisk_proverok(
        organizaciya=organizaciya,
        vid_nadzora=vid_nadzora,
        god=god,
    )
    if not proverki:
        return (
            "Экологические проверки не найдены.\n\n"
            "Актуальные данные доступны на: https://rpn.gov.ru/activities"
        )
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("organizaciya", "")[:50],
            p.get("vid_nadzora", ""),
            p.get("sostoyanie", ""),
            str(p.get("vyavleno_narusheniy", "")),
        )
        for p in proverki
    ]
    return tablitsa_v_markdown(
        ["№", "Организация", "Вид надзора", "Статус", "Нарушений"],
        stroki_tablitsy,
    )


async def info_proverki(nomer: str, ctx: Context) -> str:
    """Получить информацию о проверке по номеру.

    Аргументы:
        nomer: Номер проверки.

    Возвращает:
        Информация о проверке.
    """
    await ctx.info(f"Запрос информации о проверке {nomer}...")
    dannye = await client.info_proverki(nomer)
    if not dannye:
        return (
            f"Проверка '{nomer}' не найдена.\n\n"
            f"Проверьте номер на сайте Росприроднадзора: rpn.gov.ru"
        )
    stroki = [
        f"**Проверка № {dannye.get('nomer', nomer)}**",
        f"- Организация: {dannye.get('organizaciya', '')}",
        f"- Вид надзора: {dannye.get('vid_nadzora', '')}",
    ]
    if dannye.get("data_nachala"):
        stroki.append(f"- Дата начала: {dannye['data_nachala']}")
    if dannye.get("data_okonchaniya"):
        stroki.append(f"- Дата окончания: {dannye['data_okonchaniya']}")
    if dannye.get("sostoyanie"):
        stroki.append(f"- Статус: {dannye['sostoyanie']}")
    if dannye.get("vyavleno_narusheniy"):
        stroki.append(f"- Выявлено нарушений: {dannye['vyavleno_narusheniy']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'rpn.gov.ru')}")
    return "\n".join(stroki)


async def poisk_obektov_negativnogo(
    ctx: Context,
    organizaciya: str = "",
    kategoriya: str = "",
) -> str:
    """Поиск объектов негативного воздействия на окружающую среду.

    Аргументы:
        organizaciya: Название организации (необязательно).
        kategoriya: Категория ОНВ I–IV (необязательно).

    Возвращает:
        Список объектов ОНВ.
    """
    await ctx.info("Поиск объектов негативного воздействия...")
    obekty = await client.poisk_obektov_negativnogo(
        organizaciya=organizaciya,
        kategoriya=kategoriya,
    )
    if not obekty:
        filtry = []
        if organizaciya:
            filtry.append(f"организация: {organizaciya}")
        if kategoriya:
            filtry.append(f"категория: {kategoriya}")
        filter_text = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Объекты негативного воздействия{filter_text} не найдены.\n\n"
            f"Реестр ОНВ доступен на: https://rpn.gov.ru/onv"
        )
    stroki_tablitsy = [
        (
            o.get("nomer", ""),
            o.get("nazvanie", "")[:50],
            o.get("kategoriya", ""),
            o.get("subiekt", ""),
        )
        for o in obekty
    ]
    zagolovok = f"**Объекты негативного воздействия** — найдено: {len(obekty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Название", "Категория", "Регион"],
        stroki_tablitsy,
    )


async def poisk_litsenziy_nedra(
    ctx: Context,
    territoriya: str = "",
    vid_litsenzii: str = "",
) -> str:
    """Поиск лицензий на пользование недрами.

    Аргументы:
        territoriya: Территория / субъект РФ (необязательно).
        vid_litsenzii: Вид лицензии (необязательно).

    Возвращает:
        Список лицензий.
    """
    await ctx.info("Поиск лицензий на недропользование...")
    litsenzii = await client.poisk_litsenziy_nedra(
        territoriya=territoriya,
        vid_litsenzii=vid_litsenzii,
    )
    if not litsenzii:
        filtry = []
        if territoriya:
            filtry.append(f"территория: {territoriya}")
        if vid_litsenzii:
            filtry.append(f"вид лицензии: {vid_litsenzii}")
        filter_text = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Лицензии на недропользование{filter_text} не найдены.\n\n"
            f"Реестр лицензий доступен на: https://rpn.gov.ru/licenses"
        )
    stroki_tablitsy = [
        (
            lic.get("nomer", ""),
            lic.get("vid_litsenzii", ""),
            lic.get("territoriya", ""),
            lic.get("derzhatel", "")[:40],
            lic.get("srok_deystviya", ""),
        )
        for lic in litsenzii
    ]
    zagolovok = f"**Лицензии на пользование недрами** — найдено: {len(litsenzii)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Вид лицензии", "Территория", "Держатель", "Срок действия"],
        stroki_tablitsy,
    )


async def ekologicheskie_platezhi(
    ctx: Context,
    god: int = 0,
    tip_platezha: str = "",
) -> str:
    """Получить данные об экологических платежах.

    Аргументы:
        god: Год (необязательно).
        tip_platezha: Тип платежа (необязательно).

    Возвращает:
        Список экологических платежей.
    """
    await ctx.info("Запрос экологических платежей...")
    platezhi = await client.poluchit_ekologicheskie_platezhi(
        god=god,
        tip_platezha=tip_platezha,
    )
    if not platezhi:
        god_text = f" за {god} год" if god else ""
        return (
            f"Экологические платежи{god_text} не найдены.\n\n"
            f"Данные доступны на Госуслугах: gosuslugi.ru"
        )
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("platelshchik", "")[:40],
            p.get("tip_platezha", ""),
            str(p.get("summa", "")),
            str(p.get("god", "")),
        )
        for p in platezhi
    ]
    zagolovok = f"**Экологические платежи** — найдено: {len(platezhi)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Плательщик", "Тип платежа", "Сумма (руб.)", "Год"],
        stroki_tablitsy,
    )
