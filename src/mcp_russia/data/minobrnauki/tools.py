"""Tools for the Минобрнауки feature.

All tool docstrings are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import (
    FederalnyeOkruga,
    FormyObucheniya,
    OtrasliNauki,
    StatusyAkkreditatsii,
    TipyGrantov,
    TipyVUZov,
    UrovniObrazovaniya,
)


async def spisok_tipov_vuzov(ctx: Context) -> str:
    """Список типов высших учебных заведений. (legacy — placeholder)

    Returns:
        Список типов вузов (университет, академия, институт и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TipyVUZov]
    return markdown_table(["Код", "Тип вуза"], rows)


async def spisok_form_obucheniya(ctx: Context) -> str:
    """Список форм обучения. (legacy — placeholder)

    Returns:
        Список форм (очная, заочная, очно-заочная, дистанционная).
    """
    rows = [(f["code"], f["name"]) for f in FormyObucheniya]
    return markdown_table(["Код", "Форма обучения"], rows)


async def spisok_urovney_obrazovaniya(ctx: Context) -> str:
    """Список уровней образования. (legacy — placeholder)

    Returns:
        Список уровней (бакалавриат, специалитет, магистратура и т.д.).
    """
    rows = [(u["code"], u["name"]) for u in UrovniObrazovaniya]
    return markdown_table(["Код", "Уровень образования"], rows)


async def spisok_otrasley_nauki(ctx: Context) -> str:
    """Список отраслей науки. (legacy — placeholder)

    Returns:
        Список отраслей (естественные, технические, гуманитарные и т.д.).
    """
    rows = [(o["code"], o["name"]) for o in OtrasliNauki]
    return markdown_table(["Код", "Отрасль науки"], rows)


async def spisok_tipov_grantov(ctx: Context) -> str:
    """Список типов научных грантов. (legacy — placeholder)

    Returns:
        Список грантовых фондов и программ.
    """
    rows = [(g["code"], g["name"]) for g in TipyGrantov]
    return markdown_table(["Код", "Тип гранта"], rows)


async def spisok_statusov_akkreditatsii(ctx: Context) -> str:
    """Список статусов аккредитации вузов. (legacy — placeholder)

    Returns:
        Список статусов (действует, приостановлена, отменена).
    """
    rows = [(s["code"], s["name"]) for s in StatusyAkkreditatsii]
    return markdown_table(["Код", "Статус аккредитации"], rows)


async def spisok_federalnyh_okrugov(ctx: Context) -> str:
    """Список федеральных округов РФ. (legacy — placeholder)

    Returns:
        Список федеральных округов.
    """
    rows = [(f["code"], f["name"]) for f in FederalnyeOkruga]
    return markdown_table(["Код", "Федеральный округ"], rows)


async def info_vuza(ctx: Context, nazvanie: str) -> str:
    """Информация о высшем учебном заведении. (legacy — placeholder)

    Args:
        nazvanie: Название вуза (напр. «МГУ», «МФТИ»).

    Returns:
        Сведения о вузе (тип, город, ректор, студенты, аккредитация).
    """
    c = client.MinobrnaukiClient()
    data = c.poluchit_vuz(nazvanie)
    if not data:
        return f"Информация о вузе «{nazvanie}» не найдена (API integration pending)."
    lines = [
        f"**{data.get('nazvanie', nazvanie)}**",
        f"- Тип: {data.get('tip', '')}",
        f"- Город: {data.get('gorod', '')}",
        f"- Регион: {data.get('region', '')}",
        f"- Ректор: {data.get('rektor', '')}",
        f"- Год основания: {data.get('god_osnovaniya', '')}",
        f"- Студенты: {format_number_ru(data.get('kolichestvo_studentov', 0), 0)}",
        f"- Преподаватели: {format_number_ru(data.get('kolichestvo_prepodavateley', 0), 0)}",
        f"- Аккредитация: {data.get('status_akkreditatsii', '')}",
        f"- Сайт: {data.get('sajt', '')}",
    ]
    return "\n".join(lines)


async def programmy_vuza(ctx: Context, vuz: str, uroven: str = "") -> str:
    """Образовательные программы вуза. (legacy — placeholder)

    Args:
        vuz: Название вуза.
        uroven: Уровень образования (необязательно).

    Returns:
        Список программ с кодами направлений и проходными баллами.
    """
    c = client.MinobrnaukiClient()
    programmy = c.poluchit_programmy(vuz, uroven)
    if not programmy:
        return f"Программы вуза «{vuz}» не найдены (API integration pending)."
    rows = []
    for p in programmy:
        rows.append(
            (
                p.get("kod_napravleniya", ""),
                p.get("nazvanie", ""),
                p.get("uroven", ""),
                p.get("forma_obucheniya", ""),
                str(p.get("byudzhetnye_mesta", "")),
            )
        )
    return markdown_table(
        ["Код", "Программа", "Уровень", "Форма", "Бюдж. места"],
        rows,
    )


async def granty_i_isledovaniya(ctx: Context, organizatsiya: str = "") -> str:
    """Научные гранты и исследования. (legacy — placeholder)

    Args:
        organizatsiya: Организация-заявитель (необязательно).

    Returns:
        Список грантов с суммами финансирования и сроками.
    """
    c = client.MinobrnaukiClient()
    granty = c.poluchit_granty(organizatsiya)
    if not granty:
        return "Гранты не найдены (API integration pending)."
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
    """Рейтинг высших учебных заведений. (legacy — placeholder)

    Args:
        tip_reytinga: Тип рейтинга (необязательно).
        god: Год рейтинга.

    Returns:
        Таблица рейтинга вузов с баллами по категориям.
    """
    c = client.MinobrnaukiClient()
    reyting = c.poluchit_reyting(tip_reytinga, god)
    if not reyting:
        return f"Рейтинг вузов за {god} г. не найден (API integration pending)."
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
    """Данные об аспирантах и докторантах. (legacy — placeholder)

    Args:
        organizatsiya: Организация (необязательно).

    Returns:
        Сведения об аспирантах, направлениях и научных руководителях.
    """
    c = client.MinobrnaukiClient()
    aspiranty = c.poluchit_aspirantov(organizatsiya)
    if not aspiranty:
        return "Данные об аспирантах не найдены (API integration pending)."
    rows = []
    for a in aspiranty:
        rows.append(
            (
                a.get("fio", ""),
                a.get("napravlenie", ""),
                a.get("forma_obucheniya", ""),
                a.get("nauchny_rukovoditel", ""),
                a.get("status", ""),
            )
        )
    return markdown_table(
        ["ФИО", "Направление", "Форма", "Руководитель", "Статус"],
        rows,
    )
