"""Инструменты модуля Росводресурсов.

Правила (CONTRIBUTING.md):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import PRIZNAKI_NAPOLNENIYA


async def spisok_basseynovykh_okrugov(kontekst: Context) -> str:
    """Получить список бассейновых округов РФ.

    Возвращает:
        Список бассейновых округов.
    """
    await kontekst.info("Запрос списка бассейновых округов...")
    okruga = client.poluchit_spisok_basseynovykh_okrugov()
    stroki_tablitsy = [(okrug["kod"], okrug["nazvanie"]) for okrug in okruga]
    zagolovok = "**Бассейновые округа Российской Федерации**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Бассейновый округ"], stroki_tablitsy)


async def spisok_tipov_vodnykh_obektov(kontekst: Context) -> str:
    """Получить список типов водных объектов.

    Возвращает:
        Список типов водных объектов и гидрологических данных.
    """
    await kontekst.info("Запрос списка типов водных объектов...")
    tipy = client.poluchit_spisok_tipov_vodnykh_obektov()
    gidro = client.poluchit_spisok_tipov_gidro()

    stroki = ["**Типы водных объектов**\n"]
    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in tipy]
    stroki.append(tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy))

    stroki.append("\n**Типы гидрологических данных**\n")
    stroki_tablitsy = [
        (gidro_stantsiya["kod"], gidro_stantsiya["nazvanie"]) for gidro_stantsiya in gidro
    ]
    stroki.append(tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy))

    return "\n".join(stroki)


async def spisok_vodokhranilishch(kontekst: Context) -> str:
    """Получить список крупных водохранилищ.

    Возвращает:
        Список крупных водохранилищ с объёмом и площадью.
    """
    await kontekst.info("Запрос списка водохранилищ...")
    vodokhr = client.poluchit_vodokhranilishche_podrobno()

    stroki_tablitsy = [
        (
            vodokhranilishche["nazvanie"],
            vodokhranilishche["subiekt"],
            str(vodokhranilishche.get("obiem_km3", "")),
            str(vodokhranilishche.get("ploshchad_km2", "")),
        )
        for vodokhranilishche in vodokhr
    ]
    zagolovok = "**Крупные водохранилища РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Водохранилище", "Регион", "Объём (км³)", "Площадь (км²)"],
        stroki_tablitsy,
    )


async def poisk_vodnykh_obektov(
    kontekst: Context,
    zapros: str = "",
    tip: str = "",
    basseyn: str = "",
    subiekt: str = "",
) -> str:
    """Поиск водных объектов в Государственном водном реестре.

    Аргументы:
        zapros: Название или часть названия водного объекта.
        tip: Тип водного объекта (reka, ozero, vodokhranilishche и т.д.).
        basseyn: Код бассейнового округа.
        subiekt: Регион.

    Возвращает:
        Список найденных водных объектов.
    """
    await kontekst.info(f"Поиск водных объектов: {zapros or 'все'}...")
    obekty = await client.poisk_vodnykh_obektov(
        zapros=zapros,
        tip=tip,
        basseyn=basseyn,
        subiekt=subiekt,
    )
    if not obekty:
        return "Водные объекты не найдены. Попробуйте изменить параметры поиска."
    stroki_tablitsy = [
        (
            obekt.get("nazvanie", ""),
            obekt.get("tip", ""),
            obekt.get("basseyn", ""),
            obekt.get("subiekt", ""),
        )
        for obekt in obekty
    ]
    return tablitsa_v_markdown(
        ["Название", "Тип", "Бассейн", "Регион"],
        stroki_tablitsy,
    )


async def info_vodnogo_obekta(kod: str, kontekst: Context) -> str:
    """Получить информацию о водном объекте по коду.

    Аргументы:
        kod: Код водного объекта из Государственного водного реестра.

    Возвращает:
        Информация о водном объекте.
    """
    await kontekst.info(f"Запрос информации о водном объекте {kod}...")
    dannye = await client.info_vodnogo_obekta(kod)

    if not dannye:
        return (
            f"Водный объект с кодом '{kod}' не найден.\n\n"
            f"Проверьте код в Государственном водном реестре: text.water.ru"
        )

    stroki = [
        f"**{dannye.get('nazvanie', '')}**",
        f"- Тип: {dannye.get('tip', '')}",
        f"- Бассейн: {dannye.get('basseyn', '')}",
    ]
    if dannye.get("dlinna_km"):
        stroki.append(f"- Длина: {formatirovat_chislo_ru(dannye['dlinna_km'], 1)} км")
    if dannye.get("ploshchad_km2"):
        stroki.append(f"- Площадь: {formatirovat_chislo_ru(dannye['ploshchad_km2'], 1)} км²")
    if dannye.get("subiekt"):
        stroki.append(f"- Регион: {dannye['subiekt']}")
    if dannye.get("opisaniye"):
        stroki.append(f"- Описание: {dannye['opisaniye']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'Государственный водный реестр')}")
    return "\n".join(stroki)


async def gidro_monitoring(
    kontekst: Context,
    identifikator_posta: str = "",
    subiekt: str = "",
    tip_dannykh: str = "uroven",
) -> str:
    """Получить данные гидрологического мониторинга с постов ГМВО.

    Аргументы:
        identifikator_posta: Идентификатор гидрологического поста (необязательно).
        subiekt: Регион (необязательно).
        tip_dannykh: Тип данных (uroven, raskhod, temperatura, led, navodnenie).

    Возвращает:
        Гидрологические данные.
    """
    await kontekst.info("Запрос данных гидрологического мониторинга...")
    zapisi = await client.poluchit_gidro_dannye(
        identifikator_posta=identifikator_posta,
        subiekt=subiekt,
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

    stroki_tablitsy = [
        (
            zapis.get("post", ""),
            zapis.get("vodnyy_obekt", ""),
            zapis.get("data_izmereniya", ""),
            str(zapis.get("uroven", "")),
            str(zapis.get("raskhod", "")),
        )
        for zapis in zapisi
    ]
    zagolovok = f"**Данные гидрологического мониторинга** ({tip_dannykh})\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Пост", "Водный объект", "Дата", "Уровень (м)", "Расход (м³/с)"],
        stroki_tablitsy,
    )


async def info_vodokhranilishcha(kod: str, kontekst: Context) -> str:
    """Получить информацию о водохранилище по коду.

    Аргументы:
        kod: Код водохранилища.

    Возвращает:
        Информация о водохранилище.
    """
    await kontekst.info(f"Запрос информации о водохранилище {kod}...")
    dannye = await client.poluchit_dannye_vodokhranilishcha(kod)

    if not dannye:
        vodokhr_spisok = client.poluchit_vodokhranilishche_podrobno()
        statika = next(
            (
                vodokhranilishche
                for vodokhranilishche in vodokhr_spisok
                if vodokhranilishche["kod"] == kod
            ),
            None,
        )
        if statika:
            stroki = [f"**{statika['nazvanie']}** ({statika['subiekt']})"]
            if statika.get("obiem_km3"):
                stroki.append(f"- Объём: {formatirovat_chislo_ru(statika['obiem_km3'], 2)} км³")
            if statika.get("ploshchad_km2"):
                stroki.append(
                    f"- Площадь: {formatirovat_chislo_ru(statika['ploshchad_km2'], 1)} км²"
                )
            stroki.append("- Источник: Справочник Росводресурсов")
            return "\n".join(stroki)
        return (
            f"Водохранилище с кодом '{kod}' не найдено.\n\n"
            f"Используйте spisok_vodokhranilishch() для списка водохранилищ."
        )

    stroki = [
        f"**{dannye.get('nazvanie', '')}** ({dannye.get('subiekt', '')})",
    ]
    if dannye.get("obiem_km3"):
        stroki.append(f"- Объём: {formatirovat_chislo_ru(dannye['obiem_km3'], 2)} км³")
    if dannye.get("ploshchad_km2"):
        stroki.append(f"- Площадь: {formatirovat_chislo_ru(dannye['ploshchad_km2'], 1)} км²")
    if dannye.get("uroven_m") is not None:
        stroki.append(f"- Уровень: {formatirovat_chislo_ru(dannye['uroven_m'], 2)} м")
    nap = dannye.get("priznak_napolneniya", "")
    if nap:
        nap_nazvanie = PRIZNAKI_NAPOLNENIYA.get(nap, nap)
        stroki.append(f"- Наполнение: {nap_nazvanie}")
    if dannye.get("data_izmereniya"):
        stroki.append(f"- Дата измерения: {dannye['data_izmereniya']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'ГМВО')}")
    return "\n".join(stroki)


async def vodopolzovanie_regionov(
    kontekst: Context,
    subiekt: str = "",
    god: str = "",
) -> str:
    """Получить данные о водопользовании по регионам.

    Аргументы:
        subiekt: Регион (необязательно).
        god: Год (необязательно).

    Возвращает:
        Данные о водопользовании.
    """
    await kontekst.info("Запрос данных о водопользовании...")
    dannye = await client.poluchit_vodopolzovanie(subiekt=subiekt, god=god)

    if not dannye:
        filtry = []
        if subiekt:
            filtry.append(f"регион: {subiekt}")
        if god:
            filtry.append(f"год: {god}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Данные о водопользовании{tekst_filtra} недоступны.\n\n"
            f"Данные доступны на сайте Росводресурсов: rosvodresursy.ru"
        )

    stroki_tablitsy = [
        (
            zapis.get("subiekt", ""),
            zapis.get("god", ""),
            str(zapis.get("zabrano_vody_km3", "")),
            str(zapis.get("ispolzovano_vody_km3", "")),
            str(zapis.get("sbrosheno_stokov_km3", "")),
        )
        for zapis in dannye
    ]
    zagolovok = f"**Водопользование** — записей: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Регион", "Год", "Забрано (км³)", "Использовано (км³)", "Сброс стоков (км³)"],
        stroki_tablitsy,
    )
