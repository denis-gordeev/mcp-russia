"""Tools for the Роскомнадзор feature."""

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

    Returns:
        Список направлений с кодами и названиями.
    """
    rows = [(n["code"], n["name"]) for n in NAPRAVLENIYA_DEYATELNOSTI]
    return markdown_table(["Код", "Направление"], rows)


async def spisok_tipov_licenziy(ctx: Context) -> str:
    """Список типов лицензий связи.

    Returns:
        Список типов лицензий (телефонная, мобильная, интернет и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TIPY_LICENZIY_SVYAZI]
    return markdown_table(["Код", "Тип лицензии"], rows)


async def spisok_kategoriy_narusheniy(ctx: Context) -> str:
    """Список категорий нарушений.

    Returns:
        Список категорий нарушений (утечка ПД, запрещённый контент и т.д.).
    """
    rows = [(k["code"], k["name"]) for k in KATEGORII_NARUSHENIY]
    return markdown_table(["Код", "Категория нарушения"], rows)


async def spisok_reestrov(ctx: Context) -> str:
    """Список реестров Роскомнадзора.

    Returns:
        Справочник реестров (запрещённые сайты, операторы ПД, ОРИ и т.д.).
    """
    rows = [(r["code"], r["name"]) for r in REGISTRY_RKN]
    return markdown_table(["Код", "Реестр"], rows)


async def spisok_tipov_smi(ctx: Context) -> str:
    """Список типов СМИ.

    Returns:
        Справочник типов СМИ (печатные, сетевые, ТВ, радио и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TIPY_SMI]
    return markdown_table(["Код", "Тип СМИ"], rows)


async def spisok_kategoriy_pd_operatorov(ctx: Context) -> str:
    """Список категорий операторов персональных данных.

    Returns:
        Справочник категорий операторов ПД.
    """
    rows = [(k["code"], k["name"]) for k in KATEGORII_PD_OPERATOROV]
    return markdown_table(["Код", "Категория оператора"], rows)


async def info_licenzii(ctx: Context, nomer_licenzii: str) -> str:
    """Подробная информация о лицензии связи.

    Args:
        nomer_licenzii: Номер лицензии.

    Returns:
        Информация о лицензии (тип, организация, даты, статус, территория).
    """
    data = await client.get_licenziya(nomer_licenzii)
    if not data:
        return f"Лицензия № {nomer_licenzii} не найдена."
    lines = [
        f"**Лицензия связи** № {data.get('nomer', nomer_licenzii)}",
        f"- Тип лицензии: {data.get('tip_licenzii', '')}",
        f"- Организация: {data.get('organizaciya', '')}",
        f"- Дата выдачи: {data.get('data_vydachi', '')}",
        f"- Дата окончания: {data.get('data_okonchaniya', '')}",
        f"- Статус: {data.get('status', '')}",
        f"- Территория: {data.get('territoriya', '')}",
    ]
    return "\n".join(lines)


async def poisk_smi(ctx: Context, registracionnyy_nomer: str = "") -> str:
    """Поиск СМИ по регистрационному номеру или названию.

    Args:
        registracionnyy_nomer: Регистрационный номер СМИ (необязательно).

    Returns:
        Список СМИ с информацией о типе, учредителе, языке.
    """
    smi = await client.get_smi(registracionnyy_nomer)
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


async def info_operatora_pd(ctx: Context, inn: str = "") -> str:
    """Информация об операторе персональных данных.

    Args:
        inn: ИНН организации (необязательно).

    Returns:
        Список операторов ПД с типом, целями обработки, статусом.
    """
    operatory = await client.get_operator_pd(inn)
    if not operatory:
        return "Операторы персональных данных не найдены."
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


async def poisk_narusheniy(ctx: Context, organizaciya: str = "") -> str:
    """Поиск нарушений в сфере связи/ИТ.

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список нарушений с описанием, ссылками на законы, штрафами.
    """
    narusheniya = await client.get_narusheniya(organizaciya)
    if not narusheniya:
        return "Нарушения не найдены."
    rows = [
        (
            n.get("kategoriya_narusheniya", ""),
            n.get("opisanie", ""),
            n.get("normativ", ""),
            str(n.get("shtraf", "")),
            n.get("data_vyyavleniya", ""),
        )
        for n in narusheniya
    ]
    return markdown_table(
        ["Категория", "Описание", "Норматив", "Штраф (₽)", "Дата выявления"],
        rows,
    )


async def zapisi_reestra(ctx: Context, reestr_code: str, zapisi_id: str = "") -> str:
    """Записи из реестра Роскомнадзора.

    Args:
        reestr_code: Код реестра (blocked_sites, pd_operators, ori и т.д.).
        zapisi_id: ID конкретной записи (необязательно).

    Returns:
        Список записей реестра с основаниями и датами.
    """
    if zapisi_id:
        data = await client.get_zapis_reestra(reestr_code, zapisi_id)
        if not data:
            return f"Запись {zapisi_id} в реестре «{reestr_code}» не найдена."
        lines = [
            f"**Запись реестра** {reestr_code}/{zapisi_id}",
        ]
        for key, value in data.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    return f"Укажите ID записи для поиска в реестре «{reestr_code}»."
