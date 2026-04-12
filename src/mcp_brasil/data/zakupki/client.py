"""HTTP client for the Zakupki (ЕИС закупок) API.

Endpoints:
    - https://zakupki.gov.ru — Единая информационная система в сфере закупок
    - https://data.zakupki.gov.ru — Открытые данные ЕИС
"""

from __future__ import annotations

from .constants import (
    OTRASLI,
    SPOSOBY_ZAKUPOK,
    STATUSY_ZAKUPOK,
    TIPLY_DANNYKH,
)
from .schemas import Kontrakt, PlanZakupki, Postavshchik, Zakazchik, Zakupka


async def poisk_zakupok(
    query: str = "",
    zakon: str = "",
    region: str = "",
    status: str = "",
    limit: int = 20,
) -> list[Zakupka]:
    """Поиск закупок в ЕИС по параметрам.

    Args:
        query: Поисковый запрос (название закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        region: Регион заказчика.
        status: Статус закупки.
        limit: Максимальное количество результатов.

    Returns:
        Список закупок.
    """
    # Placeholder — реальная интеграция с API ЕИС требует отдельной работы
    return []


async def poluchit_zakupku(id_zakupki: str) -> Zakupka | None:
    """Получить подробную информацию о конкретной закупке.

    Args:
        id_zakupki: Идентификатор закупки в ЕИС.

    Returns:
        Данные закупки или None.
    """
    return None


async def poisk_kontraktov(
    contractor_inn: str = "",
    zakazchik_inn: str = "",
    limit: int = 20,
) -> list[Kontrakt]:
    """Поиск контрактов в реестре.

    Args:
        contractor_inn: ИНН поставщика.
        zakazchik_inn: ИНН заказчика.
        limit: Максимальное количество результатов.

    Returns:
        Список контрактов.
    """
    return []


async def info_zakazchika(inn: str) -> Zakazchik | None:
    """Получить информацию о заказчике по ИНН.

    Args:
        inn: ИНН заказчика.

    Returns:
        Данные заказчика или None.
    """
    return None


async def info_postavshchika(inn: str) -> Postavshchik | None:
    """Получить информацию о поставщике по ИНН.

    Args:
        inn: ИНН поставщика.

    Returns:
        Данные поставщика или None.
    """
    return None


async def plany_zakupok(year: int = 2026, organizer_inn: str = "") -> list[PlanZakupki]:
    """Получить планы-графики закупок.

    Args:
        year: Год плана.
        organizer_inn: ИНН организатора (опционально).

    Returns:
        Список планов-графиков.
    """
    return []


def get_tipy_dannykh() -> list[dict[str, str]]:
    """Получить список типов данных ЕИС."""
    return TIPLY_DANNYKH


def get_sposoby_zakupok() -> list[dict[str, str]]:
    """Получить список способов определения поставщиков."""
    return SPOSOBY_ZAKUPOK


def get_otrasli() -> list[dict[str, str]]:
    """Получить список основных отраслей."""
    return OTRASLI


def get_statusy_zakupok() -> list[dict[str, str]]:
    """Получить список статусов закупок."""
    return STATUSY_ZAKUPOK
