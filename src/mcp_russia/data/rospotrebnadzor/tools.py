"""Tools for the Роспотребнадзор feature.

All tool docstrings are in Russian with "(legacy)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from .constants import (
    KATEGORII_OBIEKTOV,
    NAPRAVLENIYA_DEYATELNOSTI,
    REGIONALNYE_UPRAVLENIYA,
    SANPIN_OSNOVNYE,
    TIPY_PROVEROK,
)


def spisok_napravleniy() -> list[dict]:
    """Список направлений деятельности Роспотребнадзора. (legacy — placeholder)

    Returns:
        Список направлений с кодами и названиями.
    """
    return NAPRAVLENIYA_DEYATELNOSTI


def spisok_tipov_proverok() -> list[dict]:
    """Список типов проверок Роспотребнадзора. (legacy — placeholder)

    Returns:
        Список типов проверок (плановая, внеплановая и т.д.).
    """
    return TIPY_PROVEROK


def spisok_kategoriy_obiektov() -> list[dict]:
    """Список категорий объектов надзора. (legacy — placeholder)

    Returns:
        Список категорий объектов (пищевые предприятия, медицина и т.д.).
    """
    return KATEGORII_OBIEKTOV


def spisok_regionalnyh_upravleniy() -> list[dict]:
    """Список региональных управлений Роспотребнадзора. (legacy — placeholder)

    Returns:
        Список управлений по федеральным округам.
    """
    return REGIONALNYE_UPRAVLENIYA


def info_proverki(nomer_proverki: str) -> dict:
    """Подробная информация о проверке. (legacy — placeholder)

    Args:
        nomer_proverki: Номер проверки.

    Returns:
        Информация о проверке (тип, объект, даты, статус, результат).
    """
    return {
        "nomer": nomer_proverki,
        "tip_proverki": "",
        "organizaciya": "",
        "data_nachala": "",
        "data_okonchaniya": "",
        "status": "placeholder — API integration pending",
        "vyavleno_narusheniy": 0,
        "rezulstat": "",
    }


def poisk_narusheniy(organizaciya: str = "") -> list[dict]:
    """Поиск санитарных нарушений по организации. (legacy — placeholder)

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список выявленных нарушений с описанием и ссылками на нормативы.
    """
    return []


def spisok_sanpinov() -> list[dict]:
    """Список основных санитарных правил и нормативов (СанПиН). (legacy — placeholder)

    Returns:
        Справочник основных СанПиН с кодами и названиями.
    """
    return SANPIN_OSNOVNYE


def zhaloby_potrebiteley(organizaciya: str = "") -> list[dict]:
    """Жалобы потребителей, зарегистрированные в Роспотребнадзоре. (legacy — placeholder)

    Args:
        organizaciya: Название организации (необязательно).

    Returns:
        Список жалоб с темой, статусом рассмотрения и результатом.
    """
    return []


def pokazateli_bezopasnosti(kod_pokazatelya: str = "") -> list[dict]:
    """Показатели эпидемиологической и санитарной безопасности. (legacy — placeholder)

    Args:
        kod_pokazatelya: Код показателя (необязательно).

    Returns:
        Список показателей со значениями и предельно допустимыми уровнями.
    """
    return []
