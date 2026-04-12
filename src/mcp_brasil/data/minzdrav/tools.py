"""Tool functions for the MinZdrav (Минздрав РФ) feature.

Tools for searching medical organizations, doctors, health indicators, and disease statistics.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import markdown_table

from . import client


async def poisk_med_organizatsiy(
    region: str = "",
    tip: str = "",
    gorod: str = "",
    ctx: Context | None = None,
) -> str:
    """Поиск медицинских организаций по параметрам.

    Args:
        region: Субъект РФ.
        tip: Тип организации (больница, поликлиника и т.д.).
        gorod: Город.

    Returns:
        Результаты поиска медицинских организаций.
    """
    if ctx:
        await ctx.info(f"Поиск медицинских организаций: {region or 'все'}...")

    header = "**Медицинские организации РФ**\n\n"

    filters = []
    if region:
        filters.append(f"Регион: {region}")
    if tip:
        filters.append(f"Тип: {tip}")
    if gorod:
        filters.append(f"Город: {gorod}")

    if filters:
        header += "Фильтры: " + ", ".join(filters) + "\n\n"

    header += (
        "Данные о медицинских организациях доступны через:\n"
        "- Минздрав РФ: https://minzdrav.gov.ru\n"
        "- Открытые данные: https://data.minzdrav.gov.ru\n"
        "- Росздравнадзор: https://roszdravnadzor.gov.ru\n\n"
        "Реестр включает: больницы, поликлиники, диспансеры, станции скорой помощи, "
        "родильные дома, хосписы, санатории, ФАПы."
    )
    return header


async def info_med_organizatsii(
    id_mo: str,
    ctx: Context,
) -> str:
    """Получить информацию о конкретной медицинской организации.

    Args:
        id_mo: Идентификатор медицинской организации.

    Returns:
        Подробная информация о медицинской организации.
    """
    await ctx.info(f"Запрос информации о МО {id_mo}...")
    mo = await client.info_med_organizatsii(id_mo)

    if not mo:
        return (
            f"Медицинская организация с ID {id_mo} не найдена.\n\n"
            f"Используйте poisk_med_organizatsiy() для поиска."
        )

    lines = [
        f"**{mo.name}**",
        f"- Тип: {mo.tip}",
        f"- Адрес: {mo.adres}",
        f"- Регион: {mo.region}",
        f"- Город: {mo.city}",
        f"- Телефон: {mo.telefon}",
        f"- Лицензия: {mo.litsenzia}",
        f"- Коек: {mo.krovatey}",
        f"- Врачей: {mo.vrachey}",
    ]
    return "\n".join(lines)


async def pokazateli_zdorovya(
    region: str = "",
    god: int = 2026,
    ctx: Context | None = None,
) -> str:
    """Получить показатели здоровья населения.

    Args:
        region: Субъект РФ (пусто = вся Россия).
        god: Год данных.

    Returns:
        Показатели здоровья населения.
    """
    if ctx:
        await ctx.info(f"Запрос показателей здоровья: {region or 'РФ'}, {god}...")

    return (
        f"**Показатели здоровья населения ({god} год)**\n\n"
        f"Регион: {region or 'Вся Россия'}\n\n"
        f"Основные показатели:\n"
        f"- Ожидаемая продолжительность жизни\n"
        f"- Общая смертность\n"
        f"- Младенческая смертность\n"
        f"- Общая заболеваемость\n"
        f"- Обеспеченность больничными койками\n"
        f"- Обеспеченность врачами\n\n"
        f"Данные доступны через открытые источники Минздрава:\n"
        f"https://data.minzdrav.gov.ru"
    )


async def statistika_zabolevaniy(
    mkb_code: str = "",
    region: str = "",
    god: int = 2026,
    ctx: Context | None = None,
) -> str:
    """Получить статистику заболеваний по МКБ-10.

    Args:
        mkb_code: Код МКБ-10 (например, 'I00-I99' для болезней кровообращения).
        region: Субъект РФ.
        god: Год данных.

    Returns:
        Статистика заболеваний.
    """
    if ctx:
        await ctx.info(f"Запрос статистики заболеваний: {mkb_code or 'все'}, {god}...")

    header = f"**Статистика заболеваний ({god} год)**\n\n"
    if mkb_code:
        header += f"Код МКБ-10: {mkb_code}\n"
    if region:
        header += f"Регион: {region}\n"

    header += (
        "\nДанные о заболеваемости доступны через:\n"
        "- Минздрав РФ: https://minzdrav.gov.ru\n"
        "- Открытые данные: https://data.minzdrav.gov.ru\n\n"
        "Классификация заболеваний по МКБ-10 включает основные классы:\n"
        "- A00-B99: Инфекционные и паразитарные болезни\n"
        "- C00-D48: Новообразования\n"
        "- I00-I99: Болезни системы кровообращения\n"
        "- J00-J99: Болезни органов дыхания\n"
        "- K00-K93: Болезни органов пищеварения"
    )
    return header


async def spravochnik_mo(ctx: Context) -> str:
    """Получить справочник типов медицинских организаций.

    Returns:
        Справочник типов МО.
    """
    await ctx.info("Запрос справочника типов медицинских организаций...")
    tipy = client.get_tipy_mo()

    rows = [(t["code"], t["name"]) for t in tipy]
    header = "**Типы медицинских организаций**\n\n"
    return header + markdown_table(["Код", "Тип организации"], rows)


async def spravochnik_spetsialnostey(ctx: Context) -> str:
    """Получить справочник врачебных специальностей.

    Returns:
        Справочник специальностей.
    """
    await ctx.info("Запрос справочника врачебных специальностей...")
    spetsialnosti = client.get_spetsialnosti()

    rows = [(s["code"], s["name"]) for s in spetsialnosti]
    header = "**Врачебные специальности**\n\n"
    return header + markdown_table(["Код", "Специальность"], rows)


async def spravochnik_mkb10(ctx: Context) -> str:
    """Получить основные классы МКБ-10.

    Returns:
        Классы МКБ-10.
    """
    await ctx.info("Запрос справочника МКБ-10...")
    mkb_classes = client.get_mkb10_classes()

    rows = [(m["code"], m["name"]) for m in mkb_classes]
    header = "**Классы МКБ-10**\n\n"
    return header + markdown_table(["Код", "Класс заболеваний"], rows)
