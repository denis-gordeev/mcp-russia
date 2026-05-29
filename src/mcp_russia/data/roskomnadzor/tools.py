"""Tools for the Роскомнадзор feature.

All tool docstrings are in Russian with "(legacy)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from .constants import (
    KATEGORII_NARUSHENIY,
    KATEGORII_PD_OPERATOROV,
    NAPRAVLENIYA_DEYATELNOSTI,
    REGISTRY_RKN,
    TIPY_LICENZIY_SVYAZI,
    TIPY_SMI,
)


def spisok_napravleniy() -> list[dict]:
    """Список направлений деятельности Роскомнадзора. (legacy — placeholder)

    Returns:
        Список направлений с кодами и названиями.
    """
    return NAPRAVLENIYA_DEYATELNOSTI


def spisok_tipov_licenziy() -> list[dict]:
    """Список типов лицензий связи. (legacy — placeholder)

    Returns:
        Список типов лицензий (телефонная, мобильная, интернет и т.д.).
    """
    return TIPY_LICENZIY_SVYAZI


def spisok_kategoriy_narusheniy() -> list[dict]:
    """Список категорий нарушений. (legacy — placeholder)

    Returns:
        Список категорий нарушений (утечка ПД, запрещённый контент и т.д.).
    """
    return KATEGORII_NARUSHENIY


def spisok_reestrov() -> list[dict]:
    """Список реестров Роскомнадзора. (legacy — placeholder)

    Returns:
        Справочник реестров (запрещённые сайты, операторы ПД, ОРИ и т.д.).
    """
    return REGISTRY_RKN


def spisok_tipov_smi() -> list[dict]:
    """Список типов СМИ. (legacy — placeholder)

    Returns:
        Справочник типов СМИ (печатные, сетевые, ТВ, радио и т.д.).
    """
    return TIPY_SMI


def spisok_kategoriy_pd_operatorov() -> list[dict]:
    """Список категорий операторов персональных данных. (legacy — placeholder)

    Returns:
        Справочник категорий операторов ПД.
    """
    return KATEGORII_PD_OPERATOROV


def info_licenzii(nomer_licenzii: str) -> dict:
    """Подробная информация о лицензии связи. (legacy — placeholder)

    Args:
        nomer_licenzii: Номер лицензии.

    Returns:
        Информация о лицензии (тип, организация, даты, статус, территория).
    """
    return {
        "nomer": nomer_licenzii,
        "tip_licenzii": "",
        "organizaciya": "",
        "data_vydachi": "",
        "data_okonchaniya": "",
        "status": "placeholder — API integration pending",
        "territoriya": "",
    }


def poisk_smi(registracionnyy_nomer: str = "") -> list[dict]:
    """Поиск СМИ по регистрационному номеру или названию. (legacy — placeholder)

    Args:
        registracionnyy_nomer: Регистрационный номер СМИ (необязательно).

    Returns:
        Список СМИ с информацией о типе, учредителе, языке.
    """
    return []


def info_operatora_pd(inn: str = "") -> list[dict]:
    """Информация об операторе персональных данных. (legacy — placeholder)

    Args:
        inn: ИНН организации (необязательно).

    Returns:
        Список операторов ПД с типом, целями обработки, статусом.
    """
    return []


def poisk_narusheniy(organizaciya: str = "") -> list[dict]:
    """Поиск нарушений в сфере связи/ИТ. (legacy — placeholder)

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список нарушений с описанием, ссылками на законы, штрафами.
    """
    return []


def zapisi_reestra(reestr_code: str, zapisi_id: str = "") -> list[dict]:
    """Записи из реестра Роскомнадзора. (legacy — placeholder)

    Args:
        reestr_code: Код реестра (blocked_sites, pd_operators, ori и т.д.).
        zapisi_id: ID конкретной записи (необязательно).

    Returns:
        Список записей реестра с основаниями и датами.
    """
    return []
