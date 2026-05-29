"""Tools for the Росреестр feature.

All tool docstrings are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from .constants import (
    FormySobstvennosti,
    KategoriiZemel,
    StatusyObiekta,
    TipyNedvizhimosti,
    VidyIspolzovaniya,
)


def spisok_tipov_nedvizhimosti() -> list[dict]:
    """Список типов объектов недвижимости. (legacy — placeholder)

    Returns:
        Список типов (земельный участок, здание, помещение и т.д.).
    """
    return TipyNedvizhimosti


def spisok_kategoriy_zemel() -> list[dict]:
    """Список категорий земель по целевому назначению. (legacy — placeholder)

    Returns:
        Список категорий земель (сельскохозяйственные, населённых пунктов и др.).
    """
    return KategoriiZemel


def spisok_vidov_ispolzovaniya() -> list[dict]:
    """Список видов разрешённого использования земельных участков. (legacy — placeholder)

    Returns:
        Список видов использования (жилое, общественное, промышленное и др.).
    """
    return VidyIspolzovaniya


def spisok_statusov_obiekta() -> list[dict]:
    """Список статусов учёта объектов недвижимости. (legacy — placeholder)

    Returns:
        Список статусов (учтённый, ранее учтённый, временный и др.).
    """
    return StatusyObiekta


def spisok_form_sobstvennosti() -> list[dict]:
    """Список форм собственности на недвижимость. (legacy — placeholder)

    Returns:
        Список форм собственности (частная, государственная, муниципальная и др.).
    """
    return FormySobstvennosti


def info_obekta(kadastrovyy_nomer: str) -> dict:
    """Подробная информация об объекте недвижимости. (legacy — placeholder)

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта
            (напр.: «77:01:0001001:1001»).

    Returns:
        Сведения об объекте (тип, адрес, площадь, кадастровая стоимость, статус).
    """
    return {
        "kadastrovyy_nomer": kadastrovyy_nomer,
        "tip_obekta": "",
        "adreshnye_svedeniya": "",
        "ploshchad": "",
        "kadastrovaya_stoimost": "",
        "data_opredeleniya_stoimosti": "",
        "status_ucheta": "placeholder — API integration pending",
        "kategoriya_zemel": "",
    }


def kadastrovaya_stoimost(kadastrovyy_nomer: str) -> dict:
    """Кадастровая стоимость объекта недвижимости. (legacy — placeholder)

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Returns:
        Кадастровая стоимость, дата определения, основание.
    """
    return {
        "kadastrovyy_nomer": kadastrovyy_nomer,
        "stoimost": None,
        "data_opredeleniya": "",
        "data_vneseniya_v_egrn": "",
        "osnovanie": "placeholder — API integration pending",
    }


def prava_na_obekt(kadastrovyy_nomer: str) -> list[dict]:
    """Сведения о зарегистрированных правах на объект. (legacy — placeholder)

    Args:
        kadastrovyy_nomer: Кадастровый номер объекта.

    Returns:
        Список зарегистрированных прав (собственность, аренда и т.д.).
    """
    return []
