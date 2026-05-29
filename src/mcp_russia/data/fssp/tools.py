"""Tools for the ФССП feature.

All tool docstrings are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from .constants import (
    KategoriiDolzhnikov,
    Ogranicheniya,
    OsnovaniyaVozbuzhdeniya,
    StatusyProizvodstva,
    VidyIspolnitelnyhProizvodstv,
)


def spisok_vidov_proizvodstv() -> list[dict]:
    """Список видов исполнительных производств. (legacy — placeholder)

    Returns:
        Список видов (имущественные, неимущественные, штрафы и т.д.).
    """
    return VidyIspolnitelnyhProizvodstv


def spisok_statusov_proizvodstva() -> list[dict]:
    """Список статусов исполнительного производства. (legacy — placeholder)

    Returns:
        Список статусов (возбуждено, в производстве, окончено и т.д.).
    """
    return StatusyProizvodstva


def spisok_ogranicheniy() -> list[dict]:
    """Список видов ограничений, налагаемых судебными приставами. (legacy — placeholder)

    Returns:
        Список ограничений (выезд, управление транспортом, арест счетов и т.д.).
    """
    return Ogranicheniya


def spisok_kategoriy_dolzhnikov() -> list[dict]:
    """Список категорий должников. (legacy — placeholder)

    Returns:
        Список категорий (физлицо, юрлицо, ИП).
    """
    return KategoriiDolzhnikov


def spisok_osnovaniy_vozbuzhdeniya() -> list[dict]:
    """Список оснований возбуждения исполнительного производства. (legacy — placeholder)

    Returns:
        Список оснований (судебный акт, постановление ГИБДД и т.д.).
    """
    return OsnovaniyaVozbuzhdeniya


def info_proizvodstva(nomer: str) -> dict:
    """Подробная информация об исполнительном производстве. (legacy — placeholder)

    Args:
        nomer: Номер исполнительного производства
            (напр.: «12345/23/77001-ИП»).

    Returns:
        Сведения о производстве (должник, взыскатель, сумма, статус).
    """
    return {
        "nomer": nomer,
        "tip_proizvodstva": "",
        "dolzhnik": "",
        "vzyskatel": "",
        "summa_vzyskaniya": None,
        "ostatok_dolga": None,
        "status": "placeholder — API integration pending",
        "data_vozbuzhdeniya": "",
        "osnovanie": "",
        "otdel_pristavov": "",
    }


def poisk_dolzhnika(fio: str, data_rozhdeniya: str = "") -> list[dict]:
    """Поиск исполнительных производств по должнику. (legacy — placeholder)

    Args:
        fio: ФИО должника или название организации.
        data_rozhdeniya: Дата рождения (необязательно, напр.: «01.01.1990»).

    Returns:
        Список исполнительных производств с суммами и статусами.
    """
    return []


def ogranicheniya_dolzhnika(fio: str) -> list[dict]:
    """Ограничения, наложенные на должника. (legacy — placeholder)

    Args:
        fio: ФИО должника или название организации.

    Returns:
        Список ограничений (запрет на выезд, арест счетов и т.д.).
    """
    return []


def rozysk_dolzhnika(fio: str) -> list[dict]:
    """Сведения о розыске должника или имущества. (legacy — placeholder)

    Args:
        fio: ФИО разыскиваемого лица.

    Returns:
        Сведения о розыске (тип, основание, кто объявил).
    """
    return []
