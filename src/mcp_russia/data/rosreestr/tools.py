"""Инструменты модуля Росреестра.

Инструменты для доступа к данным о недвижимости:
- Справочные списки (типы объектов, категории земель, виды использования, статусы, формы собственности)
- Информация об объекте по кадастровому номеру (через pkk.rosreestr.ru)
- Кадастровая стоимость
- Информация о правах

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
    - Использует Context для структурированного логирования и отчётов о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_rub, markdown_table

from . import client
from .constants import (
    FormySobstvennosti,
    KategoriiZemel,
    StatusyObiekta,
    TipyNedvizhimosti,
    VidyIspolzovaniya,
)


def spisok_tipov_nedvizhimosti() -> list[dict]:
    """Список типов объектов недвижимости.

    Returns:
        Список типов (земельный участок, здание, помещение и т.д.).
    """
    return TipyNedvizhimosti


def spisok_kategoriy_zemel() -> list[dict]:
    """Список категорий земель по целевому назначению.

    Returns:
        Список категорий земель (сельскохозяйственные, населённых пунктов и др.).
    """
    return KategoriiZemel


def spisok_vidov_ispolzovaniya() -> list[dict]:
    """Список видов разрешённого использования земельных участков.

    Returns:
        Список видов использования (жилое, общественное, промышленное и др.).
    """
    return VidyIspolzovaniya


def spisok_statusov_obiekta() -> list[dict]:
    """Список статусов учёта объектов недвижимости.

    Returns:
        Список статусов (учтённый, ранее учтённый, временный и др.).
    """
    return StatusyObiekta


def spisok_form_sobstvennosti() -> list[dict]:
    """Список форм собственности на недвижимость.

    Returns:
        Список форм собственности (частная, государственная, муниципальная и др.).
    """
    return FormySobstvennosti


async def info_obekta(kadastrovyy_nomer: str, ctx: Context) -> str:
    """Подробная информация об объекте недвижимости по кадастровому номеру.

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта
            (напр.: «77:01:0001001:1001»).

    Returns:
        Сведения об объекте (тип, адрес, площадь, кадастровая стоимость, статус).
    """
    await ctx.info(f"Запрос объекта {kadastrovyy_nomer}...")
    obekt = await client.poluchit_obekt(kadastrovyy_nomer)

    if obekt is None:
        return (
            f"**Объект {kadastrovyy_nomer}**\n\n"
            "Объект не найден на публичной кадастровой карте.\n"
            "Проверьте кадастровый номер или воспользуйтесь:\n"
            "https://pkk.rosreestr.ru"
        )

    tip_name = {
        "zemelnyy_uchastok": "Земельный участок",
        "zdanie": "Здание",
        "pomeshchenie": "Помещение",
        "sooruzhenie": "Сооружение",
        "obekt_nedostroenny": "Объект незавершённого строительства",
        "mnogokvartirnyy_dom": "Многоквартирный дом",
    }.get(obekt.tip_obekta, obekt.tip_obekta)

    lines = [
        f"**Кадастровый номер:** {obekt.kadastrovyy_nomer}",
        f"**Тип:** {tip_name}",
    ]
    if obekt.adreshnye_svedeniya:
        lines.append(f"**Адрес:** {obekt.adreshnye_svedeniya}")
    if obekt.ploshchad:
        lines.append(f"**Площадь:** {obekt.ploshchad} кв.м")
    if obekt.kadastrovaya_stoimost:
        try:
            stoimost_val = float(obekt.kadastrovaya_stoimost)
            lines.append(f"**Кадастровая стоимость:** {format_rub(stoimost_val)}")
        except (ValueError, TypeError):
            lines.append(f"**Кадастровая стоимость:** {obekt.kadastrovaya_stoimost}")
    if obekt.data_opredeleniya_stoimosti:
        lines.append(f"**Дата определения стоимости:** {obekt.data_opredeleniya_stoimosti}")
    if obekt.status_ucheta:
        lines.append(f"**Статус учёта:** {obekt.status_ucheta}")
    if obekt.kategoriya_zemel:
        lines.append(f"**Категория земель:** {obekt.kategoriya_zemel}")

    lines.append("\nИсточник: Росреестр / pkk.rosreestr.ru")
    return "\n".join(lines)


async def kadastrovaya_stoimost(kadastrovyy_nomer: str, ctx: Context) -> str:
    """Кадастровая стоимость объекта недвижимости.

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Returns:
        Кадастровая стоимость, дата определения, основание.
    """
    await ctx.info(f"Запрос кадастровой стоимости {kadastrovyy_nomer}...")
    result = await client.poluchit_kadastrovnuyu_stoimost(kadastrovyy_nomer)

    if result is None:
        return (
            f"**Кадастровый номер:** {kadastrovyy_nomer}\n\n"
            "Кадастровая стоимость не найдена.\n"
            "Проверьте кадастровый номер на https://pkk.rosreestr.ru"
        )

    lines = [f"**Кадастровый номер:** {result.kadastrovyy_nomer}"]

    if result.stoimost is not None:
        lines.append(f"**Кадастровая стоимость:** {format_rub(result.stoimost)}")
    else:
        lines.append("**Кадастровая стоимость:** Не определена")

    if result.data_opredeleniya:
        lines.append(f"**Дата определения:** {result.data_opredeleniya}")
    if result.data_vneseniya_v_egrn:
        lines.append(f"**Дата внесения в ЕГРН:** {result.data_vneseniya_v_egrn}")
    if result.osnovanie:
        lines.append(f"**Основание:** {result.osnovanie}")

    lines.append("\nИсточник: Росреестр / pkk.rosreestr.ru")
    return "\n".join(lines)


async def prava_na_obekt(kadastrovyy_nomer: str, ctx: Context) -> str:
    """Сведения о зарегистрированных правах на объект.

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Returns:
        Список зарегистрированных прав (собственность, аренда и т.д.).
    """
    await ctx.info(f"Запрос прав на объект {kadastrovyy_nomer}...")
    rights = await client.poluchit_prava(kadastrovyy_nomer)

    if not rights:
        return (
            f"**Кадастровый номер:** {kadastrovyy_nomer}\n\n"
            "Сведения о правах отсутствуют или не опубликованы.\n"
            "Полная информация доступна через выписку из ЕГРН:\n"
            "https://rosreestr.gov.ru/wps/portal/p/cc_ib_portal_services"
        )

    rows = []
    for r in rights:
        rows.append(
            (
                r.get("tip_prava", ""),
                r.get("sobstvennik", "Не указан"),
                r.get("data_registratsii", ""),
                r.get("nomer_registratsii", ""),
            )
        )

    header = f"**Зарегистрированные права на объект {kadastrovyy_nomer}**\n\n"
    header += "Источник: Росреестр / pkk.rosreestr.ru\n\n"
    return header + markdown_table(
        ["Тип права", "Правообладатель", "Дата регистрации", "Номер регистрации"],
        rows,
    )
