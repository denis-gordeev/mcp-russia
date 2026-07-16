"""Инструменты модуля Роскомнадзора."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import (
    KATEGORII_NARUSHENIY,
    KATEGORII_PD_OPERATOROV,
    NAPRAVLENIYA_DEYATELNOSTI,
    REESTR_RKN,
    TIPY_LICENZIY_SVYAZI,
    TIPY_SMI,
)


async def spisok_napravleniy(kontekst: Context) -> str:
    """Список направлений деятельности Роскомнадзора.

    Возвращает:
        Список направлений с кодами и названиями.
    """
    stroki_tablitsy = [
        (napravlenie["kod"], napravlenie["nazvanie"]) for napravlenie in NAPRAVLENIYA_DEYATELNOSTI
    ]
    return tablitsa_v_markdown(["Код", "Направление"], stroki_tablitsy)


async def spisok_tipov_licenziy(kontekst: Context) -> str:
    """Список типов лицензий связи.

    Возвращает:
        Список типов лицензий (телефонная, мобильная, интернет и т.д.).
    """
    stroki_tablitsy = [
        (tip_licenzii["kod"], tip_licenzii["nazvanie"]) for tip_licenzii in TIPY_LICENZIY_SVYAZI
    ]
    return tablitsa_v_markdown(["Код", "Тип лицензии"], stroki_tablitsy)


async def spisok_kategoriy_narusheniy(kontekst: Context) -> str:
    """Список категорий нарушений.

    Возвращает:
        Список категорий нарушений (утечка ПД, запрещённый контент и т.д.).
    """
    stroki_tablitsy = [
        (kategoriya["kod"], kategoriya["nazvanie"]) for kategoriya in KATEGORII_NARUSHENIY
    ]
    return tablitsa_v_markdown(["Код", "Категория нарушения"], stroki_tablitsy)


async def spisok_reestrov(kontekst: Context) -> str:
    """Список реестров Роскомнадзора.

    Возвращает:
        Справочник реестров (запрещённые сайты, операторы ПД, ОРИ и т.д.).
    """
    stroki_tablitsy = [(reestr["kod"], reestr["nazvanie"]) for reestr in REESTR_RKN]
    return tablitsa_v_markdown(["Код", "Реестр"], stroki_tablitsy)


async def spisok_tipov_smi(kontekst: Context) -> str:
    """Список типов СМИ.

    Возвращает:
        Справочник типов СМИ (печатные, сетевые, ТВ, радио и т.д.).
    """
    stroki_tablitsy = [(tip_smi["kod"], tip_smi["nazvanie"]) for tip_smi in TIPY_SMI]
    return tablitsa_v_markdown(["Код", "Тип СМИ"], stroki_tablitsy)


async def spisok_kategoriy_pd_operatorov(kontekst: Context) -> str:
    """Список категорий операторов персональных данных.

    Возвращает:
        Справочник категорий операторов ПД.
    """
    stroki_tablitsy = [
        (kategoriya["kod"], kategoriya["nazvanie"]) for kategoriya in KATEGORII_PD_OPERATOROV
    ]
    return tablitsa_v_markdown(["Код", "Категория оператора"], stroki_tablitsy)


async def info_licenzii(kontekst: Context, nomer_licenzii: str = "", inn: str = "") -> str:
    """Информация о лицензии связи.

    Аргументы:
        nomer_licenzii: Номер лицензии (необязательно).
        inn: ИНН лицензиата (необязательно).

    Возвращает:
        Информация о лицензии (тип, организация, даты, статус, территория).
    """
    await kontekst.info("Запрос информации о лицензии связи...")
    licenzii = await client.poisk_licenziy(nomer=nomer_licenzii, inn=inn)
    if not licenzii:
        return "Лицензия не найдена.\n\nРеестр лицензий связи: https://rkn.gov.ru/licenses"
    dannye = licenzii[0]
    stroki = [
        f"**Лицензия связи** № {dannye.get('nomer', nomer_licenzii)}",
        f"- Организация: {dannye.get('organizaciya', '')}",
        f"- Тип лицензии: {dannye.get('tip_licenzii', '')}",
        f"- Дата выдачи: {dannye.get('data_vydachi', '')}",
        f"- Дата окончания: {dannye.get('data_okonchaniya', '')}",
        f"- Статус: {dannye.get('sostoyanie', '')}",
        f"- Территория: {dannye.get('territoriya', '')}",
        f"- Источник: {dannye.get('istochnik', 'Роскомнадзор')}",
    ]
    return "\n".join(stroki)


async def poisk_smi(kontekst: Context, registracionnyy_nomer: str = "", nazvanie: str = "") -> str:
    """Поиск СМИ по регистрационному номеру или названию.

    Аргументы:
        registracionnyy_nomer: Регистрационный номер СМИ (необязательно).
        nazvanie: Название СМИ (необязательно).

    Возвращает:
        Список СМИ с информацией о типе, учредителе, языке.
    """
    await kontekst.info("Поиск СМИ в реестре Роскомнадзора...")
    smi = await client.poisk_smi(
        registracionnyy_nomer=registracionnyy_nomer,
        nazvanie=nazvanie,
    )
    if not smi:
        return "СМИ не найдены."
    stroki_tablitsy = [
        (
            sredstvo.get("registracionnyy_nomer", ""),
            sredstvo.get("nazvanie", ""),
            sredstvo.get("tip_smi", ""),
            sredstvo.get("uchreditel", ""),
            sredstvo.get("yazyk", ""),
        )
        for sredstvo in smi
    ]
    return tablitsa_v_markdown(
        ["Рег. номер", "Название", "Тип", "Учредитель", "Язык"],
        stroki_tablitsy,
    )


async def info_operatora_pd(kontekst: Context, inn: str = "", nazvanie: str = "") -> str:
    """Информация об операторе персональных данных.

    Аргументы:
        inn: ИНН организации (необязательно).
        nazvanie: Название организации (необязательно).

    Возвращает:
        Список операторов ПД с типом, целями обработки, статусом.
    """
    await kontekst.info("Поиск оператора ПД в реестре Роскомнадзора...")
    operatory = await client.poisk_operatora_pd(inn=inn, nazvanie=nazvanie)
    if not operatory:
        return (
            "Операторы персональных данных не найдены.\n\n"
            "Реестр операторов ПД: https://rkn.gov.ru/pdn"
        )
    stroki_tablitsy = [
        (
            operator.get("naimenovanie", ""),
            operator.get("inn", ""),
            operator.get("kategoriya", ""),
            operator.get("tsel_obrabotki", ""),
            operator.get("sostoyanie", ""),
        )
        for operator in operatory
    ]
    return tablitsa_v_markdown(
        ["Наименование", "ИНН", "Категория", "Цель обработки", "Статус"],
        stroki_tablitsy,
    )


async def poisk_narusheniy(kontekst: Context, organizaciya: str = "", inn: str = "") -> str:
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


async def proverka_blokirovki(kontekst: Context, domen: str) -> str:
    """Проверка наличия сайта в реестре запрещённых сайтов.

    Аргументы:
        domen: Доменное имя для проверки (напр. «example.com»).

    Возвращает:
        Информация о наличии сайта в реестре блокировок.
    """
    await kontekst.info(f"Проверка блокировки {domen}...")
    dannye = await client.proverka_blokirovki(domen)
    if dannye.get("blokirovka"):
        stroki = [
            f"**Домен {domen} — ЗАБЛОКИРОВАН**",
            f"- Основание: {dannye.get('osnovanie', '')}",
            f"- Дата включения: {dannye.get('data_vklyucheniya', '')}",
            f"- Решившие органы: {dannye.get('organy', '')}",
            f"- Источник: {dannye.get('istochnik', 'ЕАИС')}",
        ]
    else:
        stroki = [
            f"**Домен {domen} — НЕ найден** в реестре запрещённых сайтов",
            f"- Источник: {dannye.get('istochnik', 'ЕАИС (eais.rkn.gov.ru)')}",
        ]
    return "\n".join(stroki)


async def poisk_ori(kontekst: Context, nazvanie: str = "", inn: str = "") -> str:
    """Поиск организаторов распространения информации (ОРИ).

    Аргументы:
        nazvanie: Название организации (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список ОРИ с типом, статусом, основанием включения.
    """
    await kontekst.info("Поиск ОРИ в реестре Роскомнадзора...")
    ori = await client.poisk_ori(nazvanie=nazvanie, inn=inn)
    if not ori:
        return (
            "Организаторы распространения информации не найдены.\n\n"
            "Реестр ОРИ: https://rkn.gov.ru/registry-ori"
        )
    stroki_tablitsy = [
        (
            zapis.get("naimenovanie", ""),
            zapis.get("inn", ""),
            zapis.get("tip", ""),
            zapis.get("sostoyanie", ""),
            zapis.get("data_vklyucheniya", ""),
        )
        for zapis in ori
    ]
    return tablitsa_v_markdown(
        ["Наименование", "ИНН", "Тип ОРИ", "Статус", "Дата включения"],
        stroki_tablitsy,
    )


async def zapisi_reestra(
    kontekst: Context, kod_reestra: str, identifikator_zapisi: str = ""
) -> str:
    """Информация о реестре Роскомнадзора.

    Аргументы:
        kod_reestra: Код реестра (zapreshchennye_sayty, operatory_pd, ori и т.д.).
        identifikator_zapisi: ID конкретной записи (необязательно).

    Возвращает:
        Описание реестра и ссылка на источник.
    """
    reestr = next(
        (zapis_reestra for zapis_reestra in REESTR_RKN if zapis_reestra["kod"] == kod_reestra),
        None,
    )
    if not reestr:
        return f"Реестр «{kod_reestra}» не найден. Используйте spisok_reestrov()."
    stroki = [
        f"**{reestr['nazvanie']}**",
        f"- Код: {reestr['kod']}",
        f"- URL: {reestr['ssylka']}",
    ]
    return "\n".join(stroki)
