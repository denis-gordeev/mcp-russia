"""Tools for the ФНС feature.

All tool docstrings are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from .constants import (
    KategoriiNalogoplatelshchikov,
    NalogovyeRezhimy,
    StatusyOrganizacii,
    TipyProverok,
    VidyNalogov,
)


def spisok_nalogovyh_rezhimov() -> list[dict]:
    """Список режимов налогообложения в РФ. (legacy — placeholder)

    Returns:
        Список режимов (ОСНО, УСН, ЕНВД, ПСН, ЕСН, НПД).
    """
    return NalogovyeRezhimy


def spisok_vidov_nalogov() -> list[dict]:
    """Список основных видов налогов в РФ. (legacy — placeholder)

    Returns:
        Список видов налогов (НДС, НДФЛ, налог на прибыль и др.).
    """
    return VidyNalogov


def spisok_tipov_proverok() -> list[dict]:
    """Список типов налоговых проверок. (legacy — placeholder)

    Returns:
        Список типов проверок (выездная, камеральная, документарная).
    """
    return TipyProverok


def spisok_statusov_organizaciy() -> list[dict]:
    """Список статусов организаций в ЕГРЮЛ. (legacy — placeholder)

    Returns:
        Список статусов (действующая, ликвидирована и т.д.).
    """
    return StatusyOrganizacii


def spisok_kategoriy_nalogoplatelshchikov() -> list[dict]:
    """Список категорий налогоплательщиков. (legacy — placeholder)

    Returns:
        Список категорий (юрлицо, ИП, самозанятый, физлицо).
    """
    return KategoriiNalogoplatelshchikov


def info_organizacii(inn: str) -> dict:
    """Подробная информация об организации из ЕГРЮЛ. (legacy — placeholder)

    Args:
        inn: ИНН организации (10 цифр).

    Returns:
        Сведения об организации (название, адрес, руководитель, статус).
    """
    return {
        "inn": inn,
        "ogrn": "",
        "nazvanie": "",
        "polnoe_nazvanie": "",
        "yuridicheskiy_adres": "",
        "data_registracii": "",
        "status": "placeholder — API integration pending",
        "vid_deyatelnosti": "",
        "ustroyennyy_kapital": "",
        "rukovoditel": "",
    }


def info_ip(inn: str) -> dict:
    """Подробная информация об ИП из ЕГРИП. (legacy — placeholder)

    Args:
        inn: ИНН индивидуального предпринимателя (12 цифр).

    Returns:
        Сведения об ИП (ФИО, дата регистрации, статус, вид деятельности).
    """
    return {
        "inn": inn,
        "ogrnip": "",
        "fio": "",
        "data_registracii": "",
        "status": "placeholder — API integration pending",
        "vid_deyatelnosti": "",
    }


def proverki_organizacii(inn: str) -> list[dict]:
    """Список налоговых проверок организации. (legacy — placeholder)

    Args:
        inn: ИНН организации.

    Returns:
        Список проверок с типом, периодом, статусом и результатами.
    """
    return []


def nalogovye_nachisleniya(inn: str, period: str = "") -> list[dict]:
    """Налоговые начисления организации или ИП. (legacy — placeholder)

    Args:
        inn: ИНН организации или ИП.
        period: Налоговый период (необязательно, напр. «2025»).

    Returns:
        Список начислений по видам налогов с суммами и статусами оплаты.
    """
    return []
