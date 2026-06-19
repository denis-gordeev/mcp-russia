"""Инструменты модуля Роскомнадзора."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import (
    KATEGORII_NARUSHENIY,
    KATEGORII_PD_OPERATOROV,
    NAPRAVLENIYA_DEYATELNOSTI,
    REGISTRY_RKN,
    TIPY_LICENZIY_SVYAZI,
    TIPY_SMI,
)


async def spisok_napravleniy(ctx: Context) -> str:
    """Список направлений деятельности Роскомнадзора.

    Возвращает:
        Список направлений с кодами и названиями.
    """
    rows = [(n["kod"], n["nazvanie"]) for n in NAPRAVLENIYA_DEYATELNOSTI]
    return markdown_table(["Код", "Направление"], rows)


async def spisok_tipov_licenziy(ctx: Context) -> str:
    """Список типов лицензий связи.

    Возвращает:
        Список типов лицензий (телефонная, мобильная, интернет и т.д.).
    """
    rows = [(t["kod"], t["nazvanie"]) for t in TIPY_LICENZIY_SVYAZI]
    return markdown_table(["Код", "Тип лицензии"], rows)


async def spisok_kategoriy_narusheniy(ctx: Context) -> str:
    """Список категорий нарушений.

    Возвращает:
        Список категорий нарушений (утечка ПД, запрещённый контент и т.д.).
    """
    rows = [(k["kod"], k["nazvanie"]) for k in KATEGORII_NARUSHENIY]
    return markdown_table(["Код", "Категория нарушения"], rows)


async def spisok_reestrov(ctx: Context) -> str:
    """Список реестров Роскомнадзора.

    Возвращает:
        Справочник реестров (запрещённые сайты, операторы ПД, ОРИ и т.д.).
    """
    rows = [(r["kod"], r["nazvanie"]) for r in REGISTRY_RKN]
    return markdown_table(["Код", "Реестр"], rows)


async def spisok_tipov_smi(ctx: Context) -> str:
    """Список типов СМИ.

    Возвращает:
        Справочник типов СМИ (печатные, сетевые, ТВ, радио и т.д.).
    """
    rows = [(t["kod"], t["nazvanie"]) for t in TIPY_SMI]
    return markdown_table(["Код", "Тип СМИ"], rows)


async def spisok_kategoriy_pd_operatorov(ctx: Context) -> str:
    """Список категорий операторов персональных данных.

    Возвращает:
        Справочник категорий операторов ПД.
    """
    rows = [(k["kod"], k["nazvanie"]) for k in KATEGORII_PD_OPERATOROV]
    return markdown_table(["Код", "Категория оператора"], rows)


async def info_licenzii(ctx: Context, nomer_licenzii: str = "", inn: str = "") -> str:
    """Информация о лицензии связи.

    Аргументы:
        nomer_licenzii: Номер лицензии (необязательно).
        inn: ИНН лицензиата (необязательно).

    Возвращает:
        Информация о лицензии (тип, организация, даты, статус, территория).
    """
    await ctx.info("Запрос информации о лицензии связи...")
    licenzii = await client.poisk_licenziy(nomer=nomer_licenzii, inn=inn)
    if not licenzii:
        return "Лицензия не найдена.\n\nРеестр лицензий связи: https://rkn.gov.ru/licenses"
    data = licenzii[0]
    lines = [
        f"**Лицензия связи** № {data.get('nomer', nomer_licenzii)}",
        f"- Организация: {data.get('organizaciya', '')}",
        f"- Тип лицензии: {data.get('tip_licenzii', '')}",
        f"- Дата выдачи: {data.get('data_vydachi', '')}",
        f"- Дата окончания: {data.get('data_okonchaniya', '')}",
        f"- Статус: {data.get('status', '')}",
        f"- Территория: {data.get('territoriya', '')}",
        f"- Источник: {data.get('istochnik', 'Роскомнадзор')}",
    ]
    return "\n".join(lines)


async def poisk_smi(ctx: Context, registracionnyy_nomer: str = "", nazvanie: str = "") -> str:
    """Поиск СМИ по регистрационному номеру или названию.

    Аргументы:
        registracionnyy_nomer: Регистрационный номер СМИ (необязательно).
        nazvanie: Название СМИ (необязательно).

    Возвращает:
        Список СМИ с информацией о типе, учредителе, языке.
    """
    await ctx.info("Поиск СМИ в реестре Роскомнадзора...")
    smi = await client.poisk_smi(
        registracionnyy_nomer=registracionnyy_nomer,
        nazvanie=nazvanie,
    )
    if not smi:
        return "СМИ не найдены."
    rows = [
        (
            s.get("registracionnyy_nomer", ""),
            s.get("nazvanie", ""),
            s.get("tip_smi", ""),
            s.get("uchreditel", ""),
            s.get("yazyk", ""),
        )
        for s in smi
    ]
    return markdown_table(
        ["Рег. номер", "Название", "Тип", "Учредитель", "Язык"],
        rows,
    )


async def info_operatora_pd(ctx: Context, inn: str = "", nazvanie: str = "") -> str:
    """Информация об операторе персональных данных.

    Аргументы:
        inn: ИНН организации (необязательно).
        nazvanie: Название организации (необязательно).

    Возвращает:
        Список операторов ПД с типом, целями обработки, статусом.
    """
    await ctx.info("Поиск оператора ПД в реестре Роскомнадзора...")
    operatory = await client.poisk_operatora_pd(inn=inn, nazvanie=nazvanie)
    if not operatory:
        return (
            "Операторы персональных данных не найдены.\n\n"
            "Реестр операторов ПД: https://rkn.gov.ru/pdn"
        )
    rows = [
        (
            o.get("naimenovanie", ""),
            o.get("inn", ""),
            o.get("kategoriya", ""),
            o.get("tsel_obrabotki", ""),
            o.get("status", ""),
        )
        for o in operatory
    ]
    return markdown_table(
        ["Наименование", "ИНН", "Категория", "Цель обработки", "Статус"],
        rows,
    )


async def poisk_narusheniy(ctx: Context, organizaciya: str = "", inn: str = "") -> str:
    """Поиск нарушений в сфере связи/ИТ.

    Аргументы:
        организационный: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Информация о реестрах нарушений Роскомнадзора.
    """
    return (
        "**Нарушения в сфере связи и ИТ**\n\n"
        "Данные о нарушениях доступны через:\n"
        "- Открытые данные Роскомнадзора: https://rkn.gov.ru/it/opendata\n"
        "- Реестр запрещённых сайтов: https://eais.rkn.gov.ru\n"
        "- Реестр ПД: https://rkn.gov.ru/pdn\n\n"
        "Для проверки конкретного домена используйте инструмент proverka_blokirovki."
    )


async def proverka_blokirovki(ctx: Context, domen: str) -> str:
    """Проверка наличия сайта в реестре запрещённых сайтов.

    Аргументы:
        domen: Доменное имя для проверки (напр. «example.com»).

    Возвращает:
        Информация о наличии сайта в реестре блокировок.
    """
    await ctx.info(f"Проверка блокировки {domen}...")
    data = await client.proverka_blokirovki(domen)
    if data.get("blokirovka"):
        lines = [
            f"**Домен {domen} — ЗАБЛОКИРОВАН**",
            f"- Основание: {data.get('osnovanie', '')}",
            f"- Дата включения: {data.get('data_vklyucheniya', '')}",
            f"- Решившие органы: {data.get('organy', '')}",
            f"- Источник: {data.get('istochnik', 'ЕАИС')}",
        ]
    else:
        lines = [
            f"**Домен {domen} — НЕ найден** в реестре запрещённых сайтов",
            f"- Источник: {data.get('istochnik', 'ЕАИС (eais.rkn.gov.ru)')}",
        ]
    return "\n".join(lines)


async def poisk_ori(ctx: Context, nazvanie: str = "", inn: str = "") -> str:
    """Поиск организаторов распространения информации (ОРИ).

    Аргументы:
        nazvanie: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список ОРИ с типом, статусом, основанием включения.
    """
    await ctx.info("Поиск ОРИ в реестре Роскомнадзора...")
    ori = await client.poisk_ori(nazvanie=nazvanie, inn=inn)
    if not ori:
        return (
            "Организаторы распространения информации не найдены.\n\n"
            "Реестр ОРИ: https://rkn.gov.ru/registry-ori"
        )
    rows = [
        (
            o.get("naimenovanie", ""),
            o.get("inn", ""),
            o.get("tip", ""),
            o.get("status", ""),
            o.get("data_vklyucheniya", ""),
        )
        for o in ori
    ]
    return markdown_table(
        ["Наименование", "ИНН", "Тип ОРИ", "Статус", "Дата включения"],
        rows,
    )


async def zapisi_reestra(ctx: Context, kod_reestra: str, identifikator_zapisi: str = "") -> str:
    """Информация о реестре Роскомнадзора.

    Аргументы:
        kod_reestra: Код реестра (zapreshchennye_sayty, operatory_pd, ori и т.д.).
        identifikator_zapisi: ID конкретной записи (необязательно).

    Возвращает:
        Описание реестра и ссылка на источник.
    """
    reestr = next((r for r in REGISTRY_RKN if r["kod"] == kod_reestra), None)
    if not reestr:
        return f"Реестр «{kod_reestra}» не найден. Используйте spisok_reestrov()."
    lines = [
        f"**{reestr['nazvanie']}**",
        f"- Код: {reestr['kod']}",
        f"- URL: {reestr['ssylka']}",
    ]
    return "\n".join(lines)
