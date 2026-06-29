"""Инструменты модуля Роспотребнадзора."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

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

    Возвращает:
        Список направлений с кодами и названиями.
    """
    stroki_tablitsy = [(n["kod"], n["nazvanie"]) for n in NAPRAVLENIYA_DEYATELNOSTI]
    return tablitsa_v_markdown(["Код", "Направление"], stroki_tablitsy)


async def spisok_tipov_proverok(ctx: Context) -> str:
    """Список типов проверок Роспотребнадзора.

    Возвращает:
        Список типов проверок (плановая, внеплановая и т.д.).
    """
    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in TIPY_PROVEROK]
    return tablitsa_v_markdown(["Код", "Тип проверки"], stroki_tablitsy)


async def spisok_kategoriy_obiektov(ctx: Context) -> str:
    """Список категорий объектов надзора.

    Возвращает:
        Список категорий объектов (пищевые предприятия, медицина и т.д.).
    """
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in KATEGORII_OBIEKTOV]
    return tablitsa_v_markdown(["Код", "Категория объекта"], stroki_tablitsy)


async def spisok_regionalnyh_upravleniy(ctx: Context) -> str:
    """Список региональных управлений Роспотребнадзора.

    Возвращает:
        Список управлений по федеральным округам.
    """
    stroki_tablitsy = [(r["kod"], r["nazvanie"]) for r in REGIONALNYE_UPRAVLENIYA]
    return tablitsa_v_markdown(["Код", "Управление"], stroki_tablitsy)


async def info_proverki(ctx: Context, nomer_proverki: str) -> str:
    """Подробная информация о проверке Роспотребнадзора.

    Аргументы:
        nomer_proverki: Номер проверки.

    Возвращает:
        Информация о проверке (тип, объект, даты, статус, результат).
    """
    await ctx.info(f"Запрос проверки № {nomer_proverki}...")
    data = await client.info_proverki(nomer_proverki)
    if not data:
        return f"Проверка № {nomer_proverki} не найдена."
    stroki = [
        f"**Проверка** № {data.get('nomer', nomer_proverki)}",
        f"- Тип проверки: {data.get('tip_proverki', '')}",
        f"- Организация: {data.get('obekt', '')}",
        f"- ИНН: {data.get('inn', '')}",
        f"- Дата начала: {data.get('data_nachala', '')}",
        f"- Дата окончания: {data.get('data_okonchaniya', '')}",
        f"- Статус: {data.get('sostoyanie', '')}",
        f"- Выявлено нарушений: {data.get('vyavleno_narusheniy', 0)}",
        f"- Результат: {data.get('rezultat', '')}",
        f"- Источник: {data.get('istochnik', 'proverki.rospotrebnadzor.ru')}",
    ]
    return "\n".join(stroki)


async def poisk_proverok(
    ctx: Context,
    inn: str = "",
    nazvanie: str = "",
    subiekt: str = "",
) -> str:
    """Поиск проверок в реестре Роспотребнадзора.

    Аргументы:
        inn: ИНН проверяемого лица (необязательно).
        nazvanie: Название проверяемого лица (необязательно).
        subiekt: Код региона (необязательно).

    Возвращает:
        Список проверок с типом, датами и статусом.
    """
    await ctx.info("Поиск проверок в реестре Роспотребнадзора...")
    proverki = await client.poisk_proverok(
        inn_tseli=inn,
        nazvanie_tseli=nazvanie,
        subiekt=subiekt,
    )
    if not proverki:
        return "Проверки не найдены."
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("tip_proverki", ""),
            p.get("obekt", ""),
            p.get("data_nachala", ""),
            p.get("sostoyanie", ""),
            str(p.get("vyavleno_narusheniy", 0)),
        )
        for p in proverki
    ]
    return tablitsa_v_markdown(
        ["№", "Тип", "Организация", "Дата начала", "Статус", "Нарушений"],
        stroki_tablitsy,
    )


async def plan_proverok(
    ctx: Context,
    god: int = 0,
    subiekt: str = "",
) -> str:
    """План проверок Роспотребнадзора.

    Аргументы:
        god: Год плана проверок.
        subiekt: Код региона (необязательно).

    Возвращает:
        Список запланированных проверок.
    """
    await ctx.info("Запрос плана проверок Роспотребнадзора...")
    proverki = await client.plan_proverok(god=god, subiekt=subiekt)
    if not proverki:
        return (
            "План проверок не получен.\n\n"
            "Актуальный план проверок доступен на:\n"
            "https://proverki.rospotrebnadzor.ru"
        )
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("obekt", ""),
            p.get("tip_proverki", ""),
            p.get("data_nachala", ""),
            p.get("data_okonchaniya", ""),
        )
        for p in proverki
    ]
    return tablitsa_v_markdown(
        ["№", "Организация", "Тип проверки", "Начало", "Окончание"],
        stroki_tablitsy,
    )


async def spisok_sanpinov(ctx: Context) -> str:
    """Список основных санитарных правил и нормативов (СанПиН).

    Возвращает:
        Справочник основных СанПиН с кодами и названиями.
    """
    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in SANPIN_OSNOVNYE]
    return tablitsa_v_markdown(["Код", "СанПиН"], stroki_tablitsy)


async def zhaloby_potrebiteley(ctx: Context, organizaciya: str = "", inn: str = "") -> str:
    """Жалобы потребителей, зарегистрированные через ЗПП Роспотребнадзора.

    Аргументы:
        organizaciya: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список жалоб с темой, статусом рассмотрения и результатом.
    """
    await ctx.info("Поиск жалоб потребителей...")
    zhaloby = await client.poisk_zhalob(organizaciya=organizaciya, inn=inn)
    if not zhaloby:
        return "Жалобы не найдены."
    stroki_tablitsy = [
        (
            z.get("tema", ""),
            z.get("organizaciya", ""),
            z.get("data_podachi", ""),
            z.get("status_rassmotreniya", ""),
            z.get("rezultat", ""),
        )
        for z in zhaloby
    ]
    return tablitsa_v_markdown(
        ["Тема", "Организация", "Дата подачи", "Статус", "Результат"],
        stroki_tablitsy,
    )


async def poisk_narusheniy(ctx: Context, organizaciya: str = "", inn: str = "") -> str:
    """Поиск санитарных нарушений по организации.

    Аргументы:
        organizaciya: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список выявленных нарушений.
    """
    await ctx.info("Поиск нарушений в реестре проверок...")
    proverki = await client.poisk_proverok(
        inn_tseli=inn,
        nazvanie_tseli=organizaciya,
    )
    narusheniya = [p for p in proverki if p.get("vyavleno_narusheniy", 0) > 0]
    if not narusheniya:
        return "Нарушения не найдены."
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("obekt", ""),
            str(p.get("vyavleno_narusheniy", 0)),
            p.get("data_okonchaniya", ""),
            p.get("rezultat", ""),
        )
        for p in narusheniya
    ]
    return tablitsa_v_markdown(
        ["№ проверки", "Организация", "Нарушений", "Дата", "Результат"],
        stroki_tablitsy,
    )


async def pokazateli_bezopasnosti(ctx: Context, kod_pokazatelya: str = "") -> str:
    """Показатели эпидемиологической и санитарной безопасности.

    Аргументы:
        kod_pokazatelya: Код показателя (необязательно).

    Возвращает:
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
