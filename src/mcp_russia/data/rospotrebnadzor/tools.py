"""Tools for the Роспотребнадзор feature."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import (
    KATEGORII_OBIEKTOV,
    NAPRAVLENIYA_DEYATELNOSTI,
    REGIONALNYE_UPRAVLENIYA,
    SANPIN_OSNOVNYE,
    TIPY_PROVEROK,
)


async def spisok_napravleniy(ctx: Context) -> str:
    """Список направлений деятельности Роспотребнадзора.

    Returns:
        Список направлений с кодами и названиями.
    """
    rows = [(n["code"], n["name"]) for n in NAPRAVLENIYA_DEYATELNOSTI]
    return markdown_table(["Код", "Направление"], rows)


async def spisok_tipov_proverok(ctx: Context) -> str:
    """Список типов проверок Роспотребнадзора.

    Returns:
        Список типов проверок (плановая, внеплановая и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TIPY_PROVEROK]
    return markdown_table(["Код", "Тип проверки"], rows)


async def spisok_kategoriy_obiektov(ctx: Context) -> str:
    """Список категорий объектов надзора.

    Returns:
        Список категорий объектов (пищевые предприятия, медицина и т.д.).
    """
    rows = [(k["code"], k["name"]) for k in KATEGORII_OBIEKTOV]
    return markdown_table(["Код", "Категория объекта"], rows)


async def spisok_regionalnyh_upravleniy(ctx: Context) -> str:
    """Список региональных управлений Роспотребнадзора.

    Returns:
        Список управлений по федеральным округам.
    """
    rows = [(r["code"], r["name"]) for r in REGIONALNYE_UPRAVLENIYA]
    return markdown_table(["Код", "Управление"], rows)


async def info_proverki(ctx: Context, nomer_proverki: str) -> str:
    """Подробная информация о проверке.

    Args:
        nomer_proverki: Номер проверки.

    Returns:
        Информация о проверке (тип, объект, даты, статус, результат).
    """
    data = await client.get_proverka(nomer_proverki)
    if not data:
        return f"Проверка № {nomer_proverki} не найдена."
    lines = [
        f"**Проверка** № {data.get('nomer', nomer_proverki)}",
        f"- Тип проверки: {data.get('tip_proverki', '')}",
        f"- Организация: {data.get('organizaciya', '')}",
        f"- Дата начала: {data.get('data_nachala', '')}",
        f"- Дата окончания: {data.get('data_okonchaniya', '')}",
        f"- Статус: {data.get('status', '')}",
        f"- Выявлено нарушений: {data.get('vyavleno_narusheniy', 0)}",
        f"- Результат: {data.get('rezulstat', '')}",
    ]
    return "\n".join(lines)


async def poisk_narusheniy(ctx: Context, organizaciya: str = "") -> str:
    """Поиск санитарных нарушений по организации.

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список выявленных нарушений с описанием и ссылками на нормативы.
    """
    narusheniya = await client.get_narusheniya(organizaciya)
    if not narusheniya:
        return "Нарушения не найдены."
    rows = [
        (
            n.get("tip_narusheniya", ""),
            n.get("opisanie", ""),
            n.get("normativ", ""),
            n.get("data_vyyavleniya", ""),
            n.get("status", ""),
        )
        for n in narusheniya
    ]
    return markdown_table(
        ["Тип нарушения", "Описание", "Норматив", "Дата выявления", "Статус"],
        rows,
    )


async def spisok_sanpinov(ctx: Context) -> str:
    """Список основных санитарных правил и нормативов (СанПиН).

    Returns:
        Справочник основных СанПиН с кодами и названиями.
    """
    rows = [(s["code"], s["name"]) for s in SANPIN_OSNOVNYE]
    return markdown_table(["Код", "СанПиН"], rows)


async def zhaloby_potrebiteley(ctx: Context, organizaciya: str = "") -> str:
    """Жалобы потребителей, зарегистрированные в Роспотребнадзоре.

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список жалоб с темой, статусом рассмотрения и результатом.
    """
    zhaloby = await client.get_zhaloby(organizaciya)
    if not zhaloby:
        return "Жалобы не найдены."
    rows = [
        (
            z.get("tema", ""),
            z.get("data_podachi", ""),
            z.get("status_rassmotreniya", ""),
            z.get("rezultat", ""),
        )
        for z in zhaloby
    ]
    return markdown_table(
        ["Тема", "Дата подачи", "Статус", "Результат"],
        rows,
    )


async def pokazateli_bezopasnosti(ctx: Context, kod_pokazatelya: str = "") -> str:
    """Показатели эпидемиологической и санитарной безопасности.

    Args:
        kod_pokazatelya: Код показателя (необязательно).

    Returns:
        Список показателей со значениями и предельно допустимыми уровнями.
    """
    pokazateli = await client.get_pokazateli(kod_pokazatelya)
    if not pokazateli:
        return "Показатели безопасности не найдены."
    rows = [
        (
            p.get("kod", ""),
            p.get("nazvanie", ""),
            str(p.get("znachenie", "")),
            str(p.get("pdk", "")),
            p.get("edinitsa", ""),
        )
        for p in pokazateli
    ]
    return markdown_table(
        ["Код", "Показатель", "Значение", "ПДК", "Единица"],
        rows,
    )
