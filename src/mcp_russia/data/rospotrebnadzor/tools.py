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
    """Подробная информация о проверке Роспотребнадзора.

    Args:
        nomer_proverki: Номер проверки.

    Returns:
        Информация о проверке (тип, объект, даты, статус, результат).
    """
    await ctx.info(f"Запрос проверки № {nomer_proverki}...")
    data = await client.info_proverki(nomer_proverki)
    if not data:
        return f"Проверка № {nomer_proverki} не найдена."
    lines = [
        f"**Проверка** № {data.get('nomer', nomer_proverki)}",
        f"- Тип проверки: {data.get('tip_proverki', '')}",
        f"- Организация: {data.get('obekt', '')}",
        f"- ИНН: {data.get('inn', '')}",
        f"- Дата начала: {data.get('data_nachala', '')}",
        f"- Дата окончания: {data.get('data_okonchaniya', '')}",
        f"- Статус: {data.get('status', '')}",
        f"- Выявлено нарушений: {data.get('vyavleno_narusheniy', 0)}",
        f"- Результат: {data.get('rezultat', '')}",
        f"- Источник: {data.get('istochnik', 'proverki.rospotrebnadzor.ru')}",
    ]
    return "\n".join(lines)


async def poisk_proverok(
    ctx: Context,
    inn: str = "",
    nazvanie: str = "",
    region: str = "",
) -> str:
    """Поиск проверок в реестре Роспотребнадзора.

    Args:
        inn: ИНН проверяемого лица (необязательно).
        nazvanie: Название проверяемого лица (необязательно).
        region: Код региона (необязательно).

    Returns:
        Список проверок с типом, датами и статусом.
    """
    await ctx.info("Поиск проверок в реестре Роспотребнадзора...")
    proverki = await client.poisk_proverok(
        target_inn=inn,
        target_name=nazvanie,
        region=region,
    )
    if not proverki:
        return "Проверки не найдены."
    rows = [
        (
            p.get("nomer", ""),
            p.get("tip_proverki", ""),
            p.get("obekt", ""),
            p.get("data_nachala", ""),
            p.get("status", ""),
            str(p.get("vyavleno_narusheniy", 0)),
        )
        for p in proverki
    ]
    return markdown_table(
        ["№", "Тип", "Организация", "Дата начала", "Статус", "Нарушений"],
        rows,
    )


async def plan_proverok(
    ctx: Context,
    god: int = 0,
    region: str = "",
) -> str:
    """План проверок Роспотребнадзора.

    Args:
        god: Год плана проверок.
        region: Код региона (необязательно).

    Returns:
        Список запланированных проверок.
    """
    await ctx.info("Запрос плана проверок Роспотребнадзора...")
    proverki = await client.plan_proverok(god=god, region=region)
    if not proverki:
        return (
            "План проверок не получен.\n\n"
            "Актуальный план проверок доступен на:\n"
            "https://proverki.rospotrebnadzor.ru"
        )
    rows = [
        (
            p.get("nomer", ""),
            p.get("obekt", ""),
            p.get("tip_proverki", ""),
            p.get("data_nachala", ""),
            p.get("data_okonchaniya", ""),
        )
        for p in proverki
    ]
    return markdown_table(
        ["№", "Организация", "Тип проверки", "Начало", "Окончание"],
        rows,
    )


async def spisok_sanpinov(ctx: Context) -> str:
    """Список основных санитарных правил и нормативов (СанПиН).

    Returns:
        Справочник основных СанПиН с кодами и названиями.
    """
    rows = [(s["code"], s["name"]) for s in SANPIN_OSNOVNYE]
    return markdown_table(["Код", "СанПиН"], rows)


async def zhaloby_potrebiteley(ctx: Context, organizaciya: str = "", inn: str = "") -> str:
    """Жалобы потребителей, зарегистрированные через ЗПП Роспотребнадзора.

    Args:
        organizaciya: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Returns:
        Список жалоб с темой, статусом рассмотрения и результатом.
    """
    await ctx.info("Поиск жалоб потребителей...")
    zhaloby = await client.poisk_zhalob(organizaciya=organizaciya, inn=inn)
    if not zhaloby:
        return "Жалобы не найдены."
    rows = [
        (
            z.get("tema", ""),
            z.get("organizaciya", ""),
            z.get("data_podachi", ""),
            z.get("status_rassmotreniya", ""),
            z.get("rezultat", ""),
        )
        for z in zhaloby
    ]
    return markdown_table(
        ["Тема", "Организация", "Дата подачи", "Статус", "Результат"],
        rows,
    )


async def poisk_narusheniy(ctx: Context, organizaciya: str = "", inn: str = "") -> str:
    """Поиск санитарных нарушений по организации.

    Args:
        organizaciya: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Returns:
        Список выявленных нарушений.
    """
    await ctx.info("Поиск нарушений в реестре проверок...")
    proverki = await client.poisk_proverok(
        target_inn=inn,
        target_name=organizaciya,
    )
    narusheniya = [p for p in proverki if p.get("vyavleno_narusheniy", 0) > 0]
    if not narusheniya:
        return "Нарушения не найдены."
    rows = [
        (
            p.get("nomer", ""),
            p.get("obekt", ""),
            str(p.get("vyavleno_narusheniy", 0)),
            p.get("data_okonchaniya", ""),
            p.get("rezultat", ""),
        )
        for p in narusheniya
    ]
    return markdown_table(
        ["№ проверки", "Организация", "Нарушений", "Дата", "Результат"],
        rows,
    )


async def pokazateli_bezopasnosti(ctx: Context, kod_pokazatelya: str = "") -> str:
    """Показатели эпидемиологической и санитарной безопасности.

    Args:
        kod_pokazatelya: Код показателя (необязательно).

    Returns:
        Информация об источниках показателей безопасности.
    """
    return (
        "**Показатели эпидемиологической и санитарной безопасности**\n\n"
        "Данные доступны через:\n"
        "- Открытые данные Роспотребнадзора: https://rospotrebnadzor.ru/opendata\n"
        "- ЕМИСС: https://fedstat.ru\n"
        "- Статистика заболеваемости: https://rospotrebnadzor.ru/activities/statistical-data\n\n"
        "Для получения конкретных данных используйте API ЕМИСС."
    )
