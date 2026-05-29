"""HTTP-клиент для API ЦИК РФ.

Эндпоинты:
    - https://cikrf.ru — основной сайт ЦИК РФ
    - https://vybory.izbirkom.ru — ГАС «Выборы» (результаты выборов)

Примечание: данный модуль использует публичные данные ЦИК РФ.
Для полноценной интеграции может потребоваться API-ключ.
"""

from __future__ import annotations

from typing import Any

from .constants import (
    CIK_API_BASE,
    DOLZHNOSTI_FEDERAL,
    GODY_VYBOROV,
    PARTII_RF,
    SUBYEKTY_RF,
    TIPOVY_VYBORY,
    VYBORY_API,
)
from .schemas import (
    Dolzhnost,
    Kandidat,
    KandidatKratko,
    PartiaInfo,
    ResultatKandidata,
    SubyektRF,
    TipVyborov,
)


async def tipy_vyborov() -> list[TipVyborov]:
    """Получить список типов выборов."""
    return [TipVyborov(code=v["code"], name=v["name"]) for v in TIPOVY_VYBORY.values()]


async def subyekty_rf() -> list[SubyektRF]:
    """Получить справочник субъектов Российской Федерации."""
    return [SubyektRF(code=s["code"], name=s["name"], okato=s["okato"]) for s in SUBYEKTY_RF]


async def dolzhnosti_federal() -> list[Dolzhnost]:
    """Получить список федеральных избирательных должностей."""
    return [
        Dolzhnost(code=d["code"], name=d["name"], level=d["level"]) for d in DOLZHNOSTI_FEDERAL
    ]


async def partii_rf() -> list[PartiaInfo]:
    """Получить справочник политических партий РФ."""
    return [
        PartiaInfo(name=p["name"], short_name=p["short_name"], color=p["color"]) for p in PARTII_RF
    ]


async def gody_vyborov() -> list[int]:
    """Получить список годов основных федеральных выборов."""
    return GODY_VYBOROV.copy()


async def poisk_kandidata(
    fio: str,
    god: int | None = None,
    region: str | None = None,
) -> list[KandidatKratko]:
    """Поиск кандидата по ФИО.

    Args:
        fio: Фамилия, имя или отчество (частичное совпадение).
        god: Год выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Returns:
        Список найденных кандидатов.
    """
    # Заглушка: в реальности API ЦИК не предоставляет простого поиска по ФИО.
    # Для полноценного поиска потребуется парсинг ГАС «Выборы».
    return []


async def kandidat_podrobno(
    kandidat_id: str,
    god: int | None = None,
) -> Kandidat | None:
    """Получить подробную информацию о кандидате.

    Args:
        kandidat_id: ID кандидата.
        god: Год выборов (необязательно).

    Returns:
        Подробная информация о кандидате или None.
    """
    return None


async def rezultaty_vyborov(
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> list[ResultatKandidata]:
    """Получить результаты выборов.

    Args:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Returns:
        Список результатов кандидатов.
    """
    # Заглушка: для реальных данных нужно обращаться к ГАС «Выборы»
    return []


async def yavka_i_itogi(
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> dict[str, Any]:
    """Получить данные о явке и итогах выборов.

    Args:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Returns:
        Словарь с итогами выборов.
    """
    return {
        "god": god,
        "tip": tip,
        "region": region,
        "yavka_procent": 0.0,
        "vseh_izbirateley": 0,
        "progalosovalo": 0,
        "istochnik": f"{CIK_API_BASE}, {VYBORY_API}",
    }
