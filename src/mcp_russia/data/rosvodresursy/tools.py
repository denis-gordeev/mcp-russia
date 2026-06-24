"""Инструменты модуля Росводресурсов.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import PRIZNAKI_NAPOLNENIYA


async def spisok_basseynovykh_okrugov(ctx: Context) -> str:
    """Получить список бассейновых округов РФ.

    Возвращает:
        Список бассейновых округов.
    """
    await ctx.info("Запрос списка бассейновых округов...")
    okruga = client.poluchit_spisok_basseynovykh_okrugov()
    rows = [(o["kod"], o["nazvanie"]) for o in okruga]
    header = "**Бассейновые округа Российской Федерации**\n\n"
    return header + tablitsa_v_markdown(["Код", "Бассейновый округ"], rows)


async def spisok_tipov_vodnykh_obektov(ctx: Context) -> str:
    """Получить список типов водных объектов.

    Возвращает:
        Список типов водных объектов и гидрологических данных.
    """
    await ctx.info("Запрос списка типов водных объектов...")
    tipy = client.poluchit_spisok_tipov_vodnykh_obektov()
    gidro = client.poluchit_spisok_tipov_gidro()

    lines = ["**Типы водных объектов**\n"]
    rows = [(t["kod"], t["nazvanie"]) for t in tipy]
    lines.append(tablitsa_v_markdown(["Код", "Тип"], rows))

    lines.append("\n**Типы гидрологических данных**\n")
    rows = [(g["kod"], g["nazvanie"]) for g in gidro]
    lines.append(tablitsa_v_markdown(["Код", "Тип"], rows))

    return "\n".join(lines)


async def spisok_vodokhranilishch(ctx: Context) -> str:
    """Получить список крупных водохранилищ.

    Возвращает:
        Список крупных водохранилищ с объёмом и площадью.
    """
    await ctx.info("Запрос списка водохранилищ...")
    vodokhr = client.poluchit_vodokhranilishche_podrobno()

    rows = [
        (v["nazvanie"], v["region"], str(v.get("obiem_km3", "")), str(v.get("ploshchad_km2", "")))
        for v in vodokhr
    ]
    header = "**Крупные водохранилища РФ**\n\n"
    return header + tablitsa_v_markdown(
        ["Водохранилище", "Регион", "Объём (км³)", "Площадь (км²)"],
        rows,
    )


async def poisk_vodnykh_obektov(
    ctx: Context,
    zapros: str = "",
    tip: str = "",
    basseyn: str = "",
    region: str = "",
) -> str:
    """Поиск водных объектов в Государственном водном реестре.

    Аргументы:
        zapros: Название или часть названия водного объекта.
        tip: Тип водного объекта (reka, ozero, vodokhranilishche и т.д.).
        basseyn: Код бассейнового округа.
        region: Регион.

    Возвращает:
        Список найденных водных объектов.
    """
    await ctx.info(f"Поиск водных объектов: {zapros or 'все'}...")
    obekty = await client.poisk_vodnykh_obektov(
        zapros=zapros,
        tip=tip,
        basseyn=basseyn,
        region=region,
    )
    if not obekty:
        return "Водные объекты не найдены. Попробуйте изменить параметры поиска."
    rows = [
        (
            o.get("nazvanie", ""),
            o.get("tip", ""),
            o.get("basseyn", ""),
            o.get("region", ""),
        )
        for o in obekty
    ]
    return tablitsa_v_markdown(
        ["Название", "Тип", "Бассейн", "Регион"],
        rows,
    )


async def info_vodnogo_obekta(kod: str, ctx: Context) -> str:
    """Получить информацию о водном объекте по коду.

    Аргументы:
        kod: Код водного объекта из Государственного водного реестра.

    Возвращает:
        Информация о водном объекте.
    """
    await ctx.info(f"Запрос информации о водном объекте {kod}...")
    data = await client.info_vodnogo_obekta(kod)

    if not data:
        return (
            f"Водный объект с кодом '{kod}' не найден.\n\n"
            f"Проверьте код в Государственном водном реестре: text.water.ru"
        )

    lines = [
        f"**{data.get('nazvanie', '')}**",
        f"- Тип: {data.get('tip', '')}",
        f"- Бассейн: {data.get('basseyn', '')}",
    ]
    if data.get("dlinna_km"):
        lines.append(f"- Длина: {formatirovat_chislo_ru(data['dlinna_km'], 1)} км")
    if data.get("ploshchad_km2"):
        lines.append(f"- Площадь: {formatirovat_chislo_ru(data['ploshchad_km2'], 1)} км²")
    if data.get("region"):
        lines.append(f"- Регион: {data['region']}")
    if data.get("opisaniye"):
        lines.append(f"- Описание: {data['opisaniye']}")
    lines.append(f"- Источник: {data.get('istochnik', 'Государственный водный реестр')}")
    return "\n".join(lines)


async def gidro_monitoring(
    ctx: Context,
    identifikator_posta: str = "",
    region: str = "",
    tip_dannykh: str = "uroven",
) -> str:
    """Получить данные гидрологического мониторинга с постов ГМВО.

    Аргументы:
        identifikator_posta: Идентификатор гидрологического поста (необязательно).
        region: Регион (необязательно).
        tip_dannykh: Тип данных (uroven, raskhod, temperatura, led, navodnenie).

    Возвращает:
        Гидрологические данные.
    """
    await ctx.info("Запрос данных гидрологического мониторинга...")
    zapisi = await client.poluchit_gidro_dannye(
        identifikator_posta=identifikator_posta,
        region=region,
        tip_dannykh=tip_dannykh,
    )
    if not zapisi:
        return (
            "**Гидрологический мониторинг**\n\n"
            "Данные не получены.\n"
            "Мониторинговые данные доступны на:\n"
            "- ГМВО: https://gmvo.skniigkh.ru\n"
            "- Росводресурсы: https://rosvodresursy.ru"
        )

    rows = [
        (
            z.get("post", ""),
            z.get("vodnyy_obekt", ""),
            z.get("data_izmereniya", ""),
            str(z.get("uroven", "")),
            str(z.get("raskhod", "")),
        )
        for z in zapisi
    ]
    header = f"**Данные гидрологического мониторинга** ({tip_dannykh})\n\n"
    return header + tablitsa_v_markdown(
        ["Пост", "Водный объект", "Дата", "Уровень (м)", "Расход (м³/с)"],
        rows,
    )


async def info_vodokhranilishcha(kod: str, ctx: Context) -> str:
    """Получить информацию о водохранилище по коду.

    Аргументы:
        kod: Код водохранилища.

    Возвращает:
        Информация о водохранилище.
    """
    await ctx.info(f"Запрос информации о водохранилище {kod}...")
    data = await client.poluchit_dannye_vodokhranilishcha(kod)

    if not data:
        vodokhr_list = client.poluchit_vodokhranilishche_podrobno()
        static = next((v for v in vodokhr_list if v["kod"] == kod), None)
        if static:
            lines = [f"**{static['nazvanie']}** ({static['region']})"]
            if static.get("obiem_km3"):
                lines.append(f"- Объём: {formatirovat_chislo_ru(static['obiem_km3'], 2)} км³")
            if static.get("ploshchad_km2"):
                lines.append(
                    f"- Площадь: {formatirovat_chislo_ru(static['ploshchad_km2'], 1)} км²"
                )
            lines.append("- Источник: Справочник Росводресурсов")
            return "\n".join(lines)
        return (
            f"Водохранилище с кодом '{kod}' не найдено.\n\n"
            f"Используйте spisok_vodokhranilishch() для списка водохранилищ."
        )

    lines = [
        f"**{data.get('nazvanie', '')}** ({data.get('region', '')})",
    ]
    if data.get("obiem_km3"):
        lines.append(f"- Объём: {formatirovat_chislo_ru(data['obiem_km3'], 2)} км³")
    if data.get("ploshchad_km2"):
        lines.append(f"- Площадь: {formatirovat_chislo_ru(data['ploshchad_km2'], 1)} км²")
    if data.get("uroven_m") is not None:
        lines.append(f"- Уровень: {formatirovat_chislo_ru(data['uroven_m'], 2)} м")
    nap = data.get("priznak_napolneniya", "")
    if nap:
        nap_name = PRIZNAKI_NAPOLNENIYA.get(nap, nap)
        lines.append(f"- Наполнение: {nap_name}")
    if data.get("data_izmereniya"):
        lines.append(f"- Дата измерения: {data['data_izmereniya']}")
    lines.append(f"- Источник: {data.get('istochnik', 'ГМВО')}")
    return "\n".join(lines)


async def vodopolzovanie_regionov(
    ctx: Context,
    region: str = "",
    god: str = "",
) -> str:
    """Получить данные о водопользовании по регионам.

    Аргументы:
        region: Регион (необязательно).
        god: Год (необязательно).

    Возвращает:
        Данные о водопользовании.
    """
    await ctx.info("Запрос данных о водопользовании...")
    data = await client.poluchit_vodopolzovanie(region=region, god=god)

    if not data:
        filters = []
        if region:
            filters.append(f"регион: {region}")
        if god:
            filters.append(f"год: {god}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Данные о водопользовании{filter_text} недоступны.\n\n"
            f"Данные доступны на сайте Росводресурсов: rosvodresursy.ru"
        )

    rows = [
        (
            v.get("region", ""),
            v.get("god", ""),
            str(v.get("zabrano_vody_km3", "")),
            str(v.get("ispolzovano_vody_km3", "")),
            str(v.get("sbrosheno_stokov_km3", "")),
        )
        for v in data
    ]
    header = f"**Водопользование** — записей: {len(data)}\n\n"
    return header + tablitsa_v_markdown(
        ["Регион", "Год", "Забрано (км³)", "Использовано (км³)", "Сброс стоков (км³)"],
        rows,
    )
