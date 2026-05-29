"""HTTP client for the Kad Arbitrazh (Картотека арбитражных дел) API.

Endpoints:
    - https://kad.arbitr.ru — Картотека арбитражных дел (КАД)
    - https://kad.arbitr.ru/Search — Поиск дел
    - https://kad.arbitr.ru/Case/ — Страница дела
"""

from __future__ import annotations

from .constants import (
    ARBITRAZHNYE_SUDY,
    INSTANTSII_SUDOV,
    KATEGORII_DEL,
    STATUSY_DEL,
    TIPLY_AKTOV,
)
from .schemas import StoronaDela, SudebnoeDelo, SudebnoeZasedanie, SudebnyyAkt, Sudy


async def poisk_del(
    number: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    category: str = "",
    status: str = "",
    sudya: str = "",
    limit: int = 20,
) -> list[SudebnoeDelo]:
    """Поиск дел в Картотеке арбитражных дел.

    Args:
        number: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        category: Категория дела (банкротство, налоговые и т.д.).
        status: Статус дела.
        sudya: Судья.
        limit: Максимальное количество результатов.

    Returns:
        Список судебных дел.
    """
    # Placeholder — реальная интеграция с КАД требует парсинга
    return []


async def info_dela(number: str) -> SudebnoeDelo | None:
    """Получить подробную информацию о судебном деле.

    Args:
        number: Номер дела.

    Returns:
        Данные дела или None.
    """
    return None


async def akty_po_delu(number: str) -> list[SudebnyyAkt]:
    """Получить судебные акты по делу.

    Args:
        number: Номер дела.

    Returns:
        Список судебных актов.
    """
    return []


async def info_akta(id_akta: str) -> SudebnyyAkt | None:
    """Получить подробную информацию о судебном акте.

    Args:
        id_akta: Идентификатор судебного акта.

    Returns:
        Данные акта или None.
    """
    return None


async def zasedaniya_po_delu(
    number: str,
) -> list[SudebnoeZasedanie]:
    """Получить информацию о заседаниях по делу.

    Args:
        number: Номер дела.

    Returns:
        Список заседаний.
    """
    return []


async def poisk_sudey(
    familiya: str = "",
    sud_name: str = "",
) -> list[Sudy]:
    """Поиск судей арбитражных судов.

    Args:
        familiya: Фамилия судьи.
        sud_name: Наименование суда.

    Returns:
        Список судей.
    """
    return []


async def storony_dela(number: str) -> list[StoronaDela]:
    """Получить стороны судебного дела.

    Args:
        number: Номер дела.

    Returns:
        Список сторон (истцы и ответчики).
    """
    return []


def get_instantsii() -> list[dict[str, str]]:
    """Получить инстанции арбитражных судов."""
    return INSTANTSII_SUDOV


def get_kategorii_del() -> list[dict[str, str]]:
    """Получить категории дел."""
    return KATEGORII_DEL


def get_statusy_del() -> list[dict[str, str]]:
    """Получить статусы дел."""
    return STATUSY_DEL


def get_tipy_aktov() -> list[dict[str, str]]:
    """Получить типы судебных актов."""
    return TIPLY_AKTOV


def get_sudy() -> list[dict[str, str]]:
    """Получить список арбитражных судов по округам."""
    return ARBITRAZHNYE_SUDY
