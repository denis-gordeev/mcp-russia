"""HTTP client for the MinZdrav (Минздрав РФ) API.

Endpoints:
    - https://minzdrav.gov.ru — Министерство здравоохранения РФ
    - https://data.minzdrav.gov.ru — Открытые данные Минздрава
    - https://roszdravnadzor.gov.ru — Росздравнадзор
"""

from __future__ import annotations

from .constants import (
    FEDERALNYE_OKRUGA,
    MKB10_CLASSES,
    POKAZATELI_ZDOROVYA,
    SPETSIALNOSTI_VRACHEY,
    TIPLY_MO,
)
from .schemas import MedOrganizatsia, PokazatelZdorovya, VrachebnyyKadr, ZabolevanieStat


async def poisk_med_organizatsiy(
    region: str = "",
    tip: str = "",
    gorod: str = "",
    limit: int = 20,
) -> list[MedOrganizatsia]:
    """Поиск медицинских организаций по параметрам.

    Args:
        region: Субъект РФ.
        tip: Тип организации (больница, поликлиника и т.д.).
        gorod: Город.
        limit: Максимальное количество результатов.

    Returns:
        Список медицинских организаций.
    """
    # Placeholder — реальная интеграция с API Минздрава требует отдельной работы
    return []


async def info_med_organizatsii(id_mo: str) -> MedOrganizatsia | None:
    """Получить подробную информацию о медицинской организации.

    Args:
        id_mo: Идентификатор медицинской организации.

    Returns:
        Данные организации или None.
    """
    return None


async def poisk_vrachey(
    familiya: str = "",
    spetsialnost: str = "",
    organizatsia_id: str = "",
    limit: int = 20,
) -> list[VrachebnyyKadr]:
    """Поиск врачей по параметрам.

    Args:
        familiya: Фамилия врача.
        spetsialnost: Специальность.
        organizatsia_id: ID организации.
        limit: Максимальное количество результатов.

    Returns:
        Список врачей.
    """
    return []


async def pokazateli_zdorovya(
    region: str = "",
    god: int = 2026,
    kod_pokazatelya: str = "",
) -> list[PokazatelZdorovya]:
    """Получить показатели здоровья населения.

    Args:
        region: Субъект РФ (пусто = вся Россия).
        god: Год данных.
        kod_pokazatelya: Код показателя (опционально).

    Returns:
        Список показателей здоровья.
    """
    return []


async def statistika_zabolevaniy(
    mkb_code: str = "",
    region: str = "",
    god: int = 2026,
) -> list[ZabolevanieStat]:
    """Получить статистику заболеваний.

    Args:
        mkb_code: Код МКБ-10.
        region: Субъект РФ.
        god: Год данных.

    Returns:
        Статистика заболеваний.
    """
    return []


def get_tipy_mo() -> list[dict[str, str]]:
    """Получить список типов медицинских организаций."""
    return TIPLY_MO


def get_spetsialnosti() -> list[dict[str, str]]:
    """Получить список специальностей врачей."""
    return SPETSIALNOSTI_VRACHEY


def get_mkb10_classes() -> list[dict[str, str]]:
    """Получить основные классы МКБ-10."""
    return MKB10_CLASSES


def get_federalnyye_okruga() -> list[dict[str, str]]:
    """Получить список федеральных округов."""
    return FEDERALNYE_OKRUGA


def get_pokazateli_zdorovya_list() -> list[dict[str, str]]:
    """Получить список основных показателей здоровья."""
    return POKAZATELI_ZDOROVYA
