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

from mcp_russia._shared.formatting import formatirovat_rubli, tablitsa_v_markdown

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

    Возвращает:
        Список типов (земельный участок, здание, помещение и т.д.).
    """
    return TipyNedvizhimosti


def spisok_kategoriy_zemel() -> list[dict]:
    """Список категорий земель по целевому назначению.

    Возвращает:
        Список категорий земель (сельскохозяйственные, населённых пунктов и др.).
    """
    return KategoriiZemel


def spisok_vidov_ispolzovaniya() -> list[dict]:
    """Список видов разрешённого использования земельных участков.

    Возвращает:
        Список видов использования (жилое, общественное, промышленное и др.).
    """
    return VidyIspolzovaniya


def spisok_statusov_obiekta() -> list[dict]:
    """Список статусов учёта объектов недвижимости.

    Возвращает:
        Список статусов (учтённый, ранее учтённый, временный и др.).
    """
    return StatusyObiekta


def spisok_form_sobstvennosti() -> list[dict]:
    """Список форм собственности на недвижимость.

    Возвращает:
        Список форм собственности (частная, государственная, муниципальная и др.).
    """
    return FormySobstvennosti


async def info_obekta(kadastrovyy_nomer: str, kontekst: Context) -> str:
    """Подробная информация об объекте недвижимости по кадастровому номеру.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта
            (напр.: «77:01:0001001:1001»).

    Возвращает:
        Сведения об объекте (тип, адрес, площадь, кадастровая стоимость, статус).
    """
    await kontekst.info(f"Запрос объекта {kadastrovyy_nomer}...")
    obekt = await client.poluchit_obekt(kadastrovyy_nomer)

    if obekt is None:
        return (
            f"**Объект {kadastrovyy_nomer}**\n\n"
            "Объект не найден на публичной кадастровой карте.\n"
            "Проверьте кадастровый номер или воспользуйтесь:\n"
            "https://pkk.rosreestr.ru"
        )

    nazvanie_tipa = {
        "zemelnyy_uchastok": "Земельный участок",
        "zdanie": "Здание",
        "pomeshchenie": "Помещение",
        "sooruzhenie": "Сооружение",
        "obekt_nedostroenny": "Объект незавершённого строительства",
        "mnogokvartirnyy_dom": "Многоквартирный дом",
    }.get(obekt.tip_obekta, obekt.tip_obekta)

    stroki = [
        f"**Кадастровый номер:** {obekt.kadastrovyy_nomer}",
        f"**Тип:** {nazvanie_tipa}",
    ]
    if obekt.adreshnye_svedeniya:
        stroki.append(f"**Адрес:** {obekt.adreshnye_svedeniya}")
    if obekt.ploshchad:
        stroki.append(f"**Площадь:** {obekt.ploshchad} кв.м")
    if obekt.kadastrovaya_stoimost:
        try:
            stoimost_val = float(obekt.kadastrovaya_stoimost)
            stroki.append(f"**Кадастровая стоимость:** {formatirovat_rubli(stoimost_val)}")
        except (ValueError, TypeError):
            stroki.append(f"**Кадастровая стоимость:** {obekt.kadastrovaya_stoimost}")
    if obekt.data_opredeleniya_stoimosti:
        stroki.append(f"**Дата определения стоимости:** {obekt.data_opredeleniya_stoimosti}")
    if obekt.status_ucheta:
        stroki.append(f"**Статус учёта:** {obekt.status_ucheta}")
    if obekt.kategoriya_zemel:
        stroki.append(f"**Категория земель:** {obekt.kategoriya_zemel}")

    stroki.append("\nИсточник: Росреестр / pkk.rosreestr.ru")
    return "\n".join(stroki)


async def kadastrovaya_stoimost(kadastrovyy_nomer: str, kontekst: Context) -> str:
    """Кадастровая стоимость объекта недвижимости.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Возвращает:
        Кадастровая стоимость, дата определения, основание.
    """
    await kontekst.info(f"Запрос кадастровой стоимости {kadastrovyy_nomer}...")
    rezultat = await client.poluchit_kadastrovnuyu_stoimost(kadastrovyy_nomer)

    if rezultat is None:
        return (
            f"**Кадастровый номер:** {kadastrovyy_nomer}\n\n"
            "Кадастровая стоимость не найдена.\n"
            "Проверьте кадастровый номер на https://pkk.rosreestr.ru"
        )

    stroki = [f"**Кадастровый номер:** {rezultat.kadastrovyy_nomer}"]

    if rezultat.stoimost is not None:
        stroki.append(f"**Кадастровая стоимость:** {formatirovat_rubli(rezultat.stoimost)}")
    else:
        stroki.append("**Кадастровая стоимость:** Не определена")

    if rezultat.data_opredeleniya:
        stroki.append(f"**Дата определения:** {rezultat.data_opredeleniya}")
    if rezultat.data_vneseniya_v_egrn:
        stroki.append(f"**Дата внесения в ЕГРН:** {rezultat.data_vneseniya_v_egrn}")
    if rezultat.osnovanie:
        stroki.append(f"**Основание:** {rezultat.osnovanie}")

    stroki.append("\nИсточник: Росреестр / pkk.rosreestr.ru")
    return "\n".join(stroki)


async def prava_na_obekt(kadastrovyy_nomer: str, kontekst: Context) -> str:
    """Сведения о зарегистрированных правах на объект.

    Аргументы:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Возвращает:
        Список зарегистрированных прав (собственность, аренда и т.д.).
    """
    await kontekst.info(f"Запрос прав на объект {kadastrovyy_nomer}...")
    prava = await client.poluchit_prava(kadastrovyy_nomer)

    if not prava:
        return (
            f"**Кадастровый номер:** {kadastrovyy_nomer}\n\n"
            "Сведения о правах отсутствуют или не опубликованы.\n"
            "Полная информация доступна через выписку из ЕГРН:\n"
            "https://rosreestr.gov.ru/wps/portal/p/cc_ib_portal_services"
        )

    stroki_tablitsy = []
    for r in prava:
        stroki_tablitsy.append(
            (
                r.get("tip_prava", ""),
                r.get("sobstvennik", "Не указан"),
                r.get("data_registratsii", ""),
                r.get("nomer_registratsii", ""),
            )
        )

    zagolovok = f"**Зарегистрированные права на объект {kadastrovyy_nomer}**\n\n"
    zagolovok += "Источник: Росреестр / pkk.rosreestr.ru\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Тип права", "Правообладатель", "Дата регистрации", "Номер регистрации"],
        stroki_tablitsy,
    )
