"""Инструменты модуля Минобрнауки."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import (
    FEDERALNYE_OKRUGA,
    FORMY_OBUCHENIYA,
    OTRASLI_NAUKI,
    STATUSY_AKKREDITATSII,
    TIPY_GRANTOV,
    TIPY_VUZOV,
    UROVNI_OBRAZOVANIYA,
)


async def spisok_tipov_vuzov(ctx: Context) -> str:
    """Список типов высших учебных заведений.

    Возвращает:
        Список типов вузов (университет, академия, институт и т.д.).
    """
    rows = [(t["kod"], t["nazvanie"]) for t in TIPY_VUZOV]
    return markdown_table(["Код", "Тип вуза"], rows)


async def spisok_form_obucheniya(ctx: Context) -> str:
    """Список форм обучения.

    Возвращает:
        Список форм (очная, заочная, очно-заочная, дистанционная).
    """
    rows = [(f["kod"], f["nazvanie"]) for f in FORMY_OBUCHENIYA]
    return markdown_table(["Код", "Форма обучения"], rows)


async def spisok_urovney_obrazovaniya(ctx: Context) -> str:
    """Список уровней образования.

    Возвращает:
        Список уровней (бакалавриат, специалитет, магистратура и т.д.).
    """
    rows = [(u["kod"], u["nazvanie"]) for u in UROVNI_OBRAZOVANIYA]
    return markdown_table(["Код", "Уровень образования"], rows)


async def spisok_otrasley_nauki(ctx: Context) -> str:
    """Список отраслей науки.

    Возвращает:
        Список отраслей (естественные, технические, гуманитарные и т.д.).
    """
    rows = [(o["kod"], o["nazvanie"]) for o in OTRASLI_NAUKI]
    return markdown_table(["Код", "Отрасль науки"], rows)


async def spisok_tipov_grantov(ctx: Context) -> str:
    """Список типов научных грантов.

    Возвращает:
        Список грантовых фондов и программ.
    """
    rows = [(g["kod"], g["nazvanie"]) for g in TIPY_GRANTOV]
    return markdown_table(["Код", "Тип гранта"], rows)


async def spisok_statusov_akkreditatsii(ctx: Context) -> str:
    """Список статусов аккредитации вузов.

    Возвращает:
        Список статусов (действует, приостановлена, отменена).
    """
    rows = [(s["kod"], s["nazvanie"]) for s in STATUSY_AKKREDITATSII]
    return markdown_table(["Код", "Статус аккредитации"], rows)


async def spisok_federalnyh_okrugov(ctx: Context) -> str:
    """Список федеральных округов РФ.

    Возвращает:
        Список федеральных округов.
    """
    rows = [(f["kod"], f["nazvanie"]) for f in FEDERALNYE_OKRUGA]
    return markdown_table(["Код", "Федеральный округ"], rows)


async def info_vuza(ctx: Context, nazvanie: str = "", inn: str = "") -> str:
    """Информация о высшем учебном заведении (аккредитация Рособрнадзора).

    Аргументы:
        nazvanie: Название вуза (напр. «МГУ», «МФТИ»).
        inn: ИНН вуза.

    Возвращает:
        Сведения о вузе (тип, город, регион, аккредитация).
    """
    await ctx.info(f"Запрос информации о вузе «{nazvanie or inn}»...")
    if inn:
        data = await client.info_akkreditacii(inn)
    else:
        results = await client.poisk_akreditovannyh_vuzov(nazvanie=nazvanie)
        data = results[0] if results else None

    if not data:
        return f"Информация о вузе «{nazvanie or inn}» не найдена в реестре Рособрнадзора."
    lines = [
        f"**{data.get('nazvanie', nazvanie or inn)}**",
        f"- ИНН: {data.get('inn', '')}",
        f"- Тип: {data.get('tip', '')}",
        f"- Город: {data.get('gorod', '')}",
        f"- Регион: {data.get('region', '')}",
        f"- Аккредитация: {data.get('status_akkreditatsii', '')}",
        f"- Дата аккредитации: {data.get('data_akkreditatsii', '')}",
        f"- Срок действия: {data.get('srok_deystviya', '')}",
        f"- № свидетельства: {data.get('nomer_svidetelstva', '')}",
        f"- Адрес: {data.get('adres', '')}",
        f"- Сайт: {data.get('sayt', '')}",
        f"- Источник: {data.get('istochnik', 'Рособрнадзор')}",
    ]
    return "\n".join(lines)


async def programmy_vuza(ctx: Context, vuz: str, uroven: str = "") -> str:
    """Образовательные программы вуза.

    Аргументы:
        vuz: Название вуза.
        uroven: Уровень образования (необязательно).

    Возвращает:
        Список программ с кодами направлений.
    """
    await ctx.info(f"Запрос программ вуза «{vuz}»...")
    results = await client.poisk_akreditovannyh_vuzov(nazvanie=vuz)
    if not results:
        return f"Вуз «{vuz}» не найден в реестре Рособрнадзора."

    data = results[0]
    lines = [
        f"**{data.get('nazvanie', vuz)}**",
        f"- Аккредитация: {data.get('status_akkreditatsii', '')}",
        f"- № свидетельства: {data.get('nomer_svidetelstva', '')}",
        "",
        "Подробная информация об образовательных программах доступна на:",
        f"- {data.get('sayt', 'сайте вуза')}",
        "- Рособрнадзор: https://obrnadzor.gov.ru/ru/registry_accreditation",
    ]
    return "\n".join(lines)


async def granty_i_isledovaniya(ctx: Context, organizatsiya: str = "") -> str:
    """Научные гранты и исследования.

    Аргументы:
        organizatsiya: Организация-заявитель (необязательно).

    Возвращает:
        Список грантовых фондов и программ.
    """
    await ctx.info("Запрос информации о грантах...")
    granty = await client.poluchit_granty(organizatsiya)
    if not granty:
        return "Гранты не найдены."
    rows = []
    for g in granty:
        summ = (
            format_number_ru(g.get("summa_finansirovaniya", 0), 0)
            if g.get("summa_finansirovaniya")
            else "—"
        )
        rows.append(
            (
                g.get("tip_granta", ""),
                g.get("nazvanie", ""),
                g.get("rukovoditel", ""),
                summ,
                g.get("status", ""),
            )
        )
    return markdown_table(
        ["Тип гранта", "Название", "Руководитель", "Сумма (₽)", "Статус"],
        rows,
    )


async def reyting_vuzov(ctx: Context, tip_reytinga: str = "", god: int = 2024) -> str:
    """Рейтинг высших учебных заведений.

    Аргументы:
        tip_reytinga: Тип рейтинга (необязательно).
        god: Год рейтинга.

    Возвращает:
        Таблица рейтинга вузов с баллами по категориям.
    """
    await ctx.info(f"Запрос рейтинга вузов за {god} г....")
    reyting = await client.poluchit_reyting(tip_reytinga, god)
    if not reyting:
        return (
            f"Рейтинг вузов за {god} г. не получен.\n\n"
            f"Актуальные рейтинги доступны на:\n"
            f"- https://vuz.minobrnauki.gov.ru\n"
            f"- https://obrnadzor.gov.ru"
        )
    rows = []
    for r in reyting:
        rows.append(
            (
                str(r.get("mesto_v_reytinge", "")),
                r.get("nazvanie", ""),
                format_number_ru(r.get("ball", 0), 1) if r.get("ball") else "—",
                r.get("tip_reytinga", ""),
            )
        )
    return markdown_table(
        ["Место", "Вуз", "Балл", "Тип рейтинга"],
        rows,
    )


async def aspirantura(ctx: Context, organizatsiya: str = "") -> str:
    """Данные об аспирантах и докторантах.

    Аргументы:
        organizatsiya: Организация (необязательно).

    Возвращает:
        Сведения об аспирантах, направлениях и научных руководителях.
    """
    return (
        "**Данные об аспирантуре**\n\n"
        "Информация об аспирантах и докторантах доступна через:\n"
        "- ЕГИСУ науки: https://esu.minobrnauki.gov.ru\n"
        "- Рособрнадзор: https://obrnadzor.gov.ru\n"
        "- Мониторинг образования: https://vuz.minobrnauki.gov.ru\n\n"
        "Для получения данных по конкретной организации "
        "укажите ИНН через инструмент info_vuza."
    )


async def poisk_licenziy(ctx: Context, nazvanie: str = "", inn: str = "") -> str:
    """Поиск лицензий на образовательную деятельность.

    Аргументы:
        nazvanie: Название вуза (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список лицензий с номерами и статусами.
    """
    await ctx.info("Запрос лицензий из реестра Рособрнадзора...")
    results = await client.poisk_licenziy(nazvanie=nazvanie, inn=inn)
    if not results:
        return "Лицензии не найдены."
    rows = []
    for r in results:
        rows.append(
            (
                r.get("nomer_licenzii", ""),
                r.get("nazvanie", ""),
                r.get("status_licenzii", ""),
                r.get("srok_deystviya", ""),
            )
        )
    return markdown_table(
        ["№ лицензии", "Организация", "Статус", "Срок действия"],
        rows,
    )
