"""Инструменты модуля Минздрава РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def poisk_med_organizatsiy(
    ctx: Context,
    subiekt: str = "",
    tip: str = "",
    gorod: str = "",
) -> str:
    """Поиск медицинских организаций в ФРМО.

    Аргументы:
        subiekt: Субъект РФ (необязательно).
        tip: Тип организации — больница, поликлиника и т.д. (необязательно).
        gorod: Город (необязательно).

    Возвращает:
        Список медицинских организаций.
    """
    await ctx.info(f"Поиск медицинских организаций: {subiekt or 'все'}...")
    orgs = await client.poisk_med_organizatsiy(
        subiekt=subiekt,
        tip=tip,
        gorod=gorod,
    )
    if not orgs:
        return (
            "Медицинские организации не найдены.\n\n"
            "Данные доступны через:\n"
            "- ФРМО: https://frrr.rosminzdrav.ru\n"
            "- Росздравнадзор: https://roszdravnadzor.gov.ru"
        )
    rows = [
        (
            o.get("nazvanie", ""),
            o.get("tip", ""),
            o.get("subiekt", ""),
            o.get("gorod", ""),
        )
        for o in orgs
    ]
    return tablitsa_v_markdown(
        ["Название", "Тип", "Регион", "Город"],
        rows,
    )


async def info_med_organizatsii(
    ctx: Context,
    identifikator_mo: str,
) -> str:
    """Получить информацию о конкретной медицинской организации.

    Аргументы:
        identifikator_mo: Идентификатор медицинской организации (ОГРН или ИНН).

    Возвращает:
        Подробная информация о медицинской организации.
    """
    await ctx.info(f"Запрос информации о МО {identifikator_mo}...")
    mo = await client.info_med_organizatsii(identifikator_mo)

    if not mo:
        return (
            f"Медицинская организация с ID {identifikator_mo} не найдена.\n\n"
            f"Используйте poisk_med_organizatsiy() для поиска."
        )

    lines = [
        f"**{mo.get('nazvanie', '')}**",
        f"- Тип: {mo.get('tip', '')}",
        f"- Адрес: {mo.get('adres', '')}",
        f"- Регион: {mo.get('subiekt', '')}",
        f"- Город: {mo.get('gorod', '')}",
        f"- Телефон: {mo.get('telefon', '')}",
        f"- Лицензия: {mo.get('litsenzia', '')}",
        f"- Коек: {mo.get('krovatey', 0)}",
        f"- Врачей: {mo.get('vrachey', 0)}",
        f"- Источник: {mo.get('istochnik', 'ФРМО')}",
    ]
    return "\n".join(lines)


async def poisk_litsenziy(
    ctx: Context,
    inn: str = "",
    vid: str = "",
) -> str:
    """Поиск лицензий Росздравнадзора на медицинскую деятельность.

    Аргументы:
        inn: ИНН организации (необязательно).
        vid: Вид лицензируемой деятельности (необязательно).

    Возвращает:
        Список лицензий.
    """
    await ctx.info("Поиск лицензий Росздравнадзора...")
    litsenzii = await client.poisk_litsenziy(inn=inn, vid=vid)
    if not litsenzii:
        return (
            "Лицензии не найдены.\n\n"
            "Реестр лицензий Росздравнадзора: https://roszdravnadzor.gov.ru"
        )
    rows = [
        (
            lit.get("nomer", ""),
            lit.get("organizaciya", ""),
            lit.get("vid_deyatelnosti", ""),
            lit.get("status", ""),
            lit.get("data_okonchaniya", ""),
        )
        for lit in litsenzii
    ]
    return tablitsa_v_markdown(
        ["№ лицензии", "Организация", "Вид деятельности", "Статус", "Действует до"],
        rows,
    )


async def pokazateli_zdorovya(
    ctx: Context,
    subiekt: str = "",
    god: int = 0,
) -> str:
    """Получить показатели здоровья населения из открытых данных Минздрава.

    Аргументы:
        subiekt: Субъект РФ (пусто = вся Россия).
        god: Год данных.

    Возвращает:
        Показатели здоровья населения.
    """
    await ctx.info(f"Запрос показателей здоровья: {subiekt or 'РФ'}, {god or 'последние'}...")
    data = await client.pokazateli_zdorovya(subiekt=subiekt, god=god)
    if not data:
        return (
            f"**Показатели здоровья населения**\n\n"
            f"Регион: {subiekt or 'Вся Россия'}\n\n"
            f"Данные доступны через открытые источники Минздрава:\n"
            f"https://data.minzdrav.gov.ru"
        )
    rows = [
        (
            p.get("nazvanie", ""),
            str(p.get("znachenie", "")),
            p.get("ed_izm", ""),
            str(p.get("god", "")),
            p.get("subiekt", ""),
        )
        for p in data
    ]
    return tablitsa_v_markdown(
        ["Показатель", "Значение", "Ед. изм.", "Год", "Регион"],
        rows,
    )


async def statistika_zabolevaniy(
    ctx: Context,
    kod_mkb: str = "",
    subiekt: str = "",
    god: int = 0,
) -> str:
    """Получить статистику заболеваний по МКБ-10.

    Аргументы:
        kod_mkb: Код МКБ-10 (например, 'I00-I99' для болезней кровообращения).
        subiekt: Субъект РФ.
        god: Год данных.

    Возвращает:
        Статистика заболеваний.
    """
    await ctx.info(f"Запрос статистики заболеваний: {kod_mkb or 'все'}, {god or 'последние'}...")
    data = await client.statistika_zabolevaniy(kod_mkb=kod_mkb, subiekt=subiekt, god=god)
    if not data:
        header = "**Статистика заболеваний**\n\n"
        if kod_mkb:
            header += f"Код МКБ-10: {kod_mkb}\n"
        if subiekt:
            header += f"Регион: {subiekt}\n"
        header += (
            "\nДанные о заболеваемости доступны через:\n"
            "- Открытые данные Минздрава: https://data.minzdrav.gov.ru\n"
        )
        return header
    rows = [
        (
            z.get("kod_mkb", ""),
            z.get("nazvanie", ""),
            str(z.get("chelovek_zabolelo", "")),
            str(z.get("letalnykh_sluchaev", "")),
            str(z.get("god", "")),
        )
        for z in data
    ]
    return tablitsa_v_markdown(
        ["МКБ-10", "Заболевание", "Заболевших", "Летальных", "Год"],
        rows,
    )


async def spravochnik_mo(ctx: Context) -> str:
    """Получить справочник типов медицинских организаций.

    Возвращает:
        Справочник типов МО.
    """
    await ctx.info("Запрос справочника типов медицинских организаций...")
    tipy = client.poluchit_tipy_mo()
    rows = [(t["kod"], t["nazvanie"]) for t in tipy]
    header = "**Типы медицинских организаций**\n\n"
    return header + tablitsa_v_markdown(["Код", "Тип организации"], rows)


async def spravochnik_spetsialnostey(ctx: Context) -> str:
    """Получить справочник врачебных специальностей.

    Возвращает:
        Справочник специальностей.
    """
    await ctx.info("Запрос справочника врачебных специальностей...")
    spetsialnosti = client.poluchit_spetsialnosti()
    rows = [(s["kod"], s["nazvanie"]) for s in spetsialnosti]
    header = "**Врачебные специальности**\n\n"
    return header + tablitsa_v_markdown(["Код", "Специальность"], rows)


async def spravochnik_mkb10(ctx: Context) -> str:
    """Получить основные классы МКБ-10.

    Возвращает:
        Классы МКБ-10.
    """
    await ctx.info("Запрос справочника МКБ-10...")
    mkb_classes = client.poluchit_klassy_mkb10()
    rows = [(m["kod"], m["nazvanie"]) for m in mkb_classes]
    header = "**Классы МКБ-10**\n\n"
    return header + tablitsa_v_markdown(["Код", "Класс заболеваний"], rows)
