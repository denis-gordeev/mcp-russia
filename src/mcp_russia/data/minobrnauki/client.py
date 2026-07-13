"""HTTP-клиент для модуля Минобрнауки.

Интеграция с реальными API:
    - Рособрнадзор (аккредитация): obrnadzor.gov.ru/opendata
    - Реестр лицензий: obrnadzor.gov.ru/opendata
    - Рейтинг вузов: vuz.minobrnauki.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    OBRNADZOR_AKKREDITATSIYA_ADRES,
    OBRNADZOR_LITSENZIYA_ADRES,
    VUZ_REYTING_ADRES,
)

logger = logging.getLogger(__name__)


async def poisk_akreditovannyh_vuzov(
    nazvanie: str = "",
    inn: str = "",
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Поиск аккредитованных образовательных учреждений через Рособрнадзор.

    Аргументы:
        nazvanie: Название вуза (частичное совпадение).
        inn: ИНН организации.
        subiekt: Регион (субъект РФ).

    Возвращает:
        Список аккредитованных учреждений.
    """
    try:
        dannye = await http_poluchit(OBRNADZOR_AKKREDITATSIYA_ADRES, taimaut=30.0)
        if not isinstance(dannye, list):
            return []
        rezultaty = []
        for zapis in dannye:
            if not isinstance(zapis, dict):
                continue
            if nazvanie and nazvanie.lower() not in zapis.get("fullName", "").lower():
                continue
            if inn and inn != zapis.get("inn", ""):
                continue
            if subiekt and subiekt.lower() not in zapis.get("subjectRF", "").lower():
                continue
            rezultaty.append(_razobrat_akkreditatsiyu(zapis))
        return rezultaty
    except Exception:
        logger.exception("Ошибка при поиске аккредитованных вузов")
        return []


async def info_akkreditacii(inn: str) -> dict[str, Any] | None:
    """Получить информацию об аккредитации образовательного учреждения.

    Аргументы:
        inn: ИНН организации.

    Возвращает:
        Данные об аккредитации или None.
    """
    try:
        dannye = await http_poluchit(OBRNADZOR_AKKREDITATSIYA_ADRES, taimaut=30.0)
        if not isinstance(dannye, list):
            return None
        for zapis in dannye:
            if not isinstance(zapis, dict):
                continue
            if zapis.get("inn") == inn:
                return _razobrat_akkreditatsiyu(zapis)
        return None
    except Exception:
        logger.exception("Ошибка при получении информации об аккредитации")
        return None


async def poisk_licenziy(
    nazvanie: str = "",
    inn: str = "",
) -> list[dict[str, Any]]:
    """Поиск лицензированных образовательных учреждений через Рособрнадзор.

    Аргументы:
        nazvanie: Название вуза (частичное совпадение).
        inn: ИНН организации.

    Возвращает:
        Список лицензированных учреждений.
    """
    try:
        dannye = await http_poluchit(OBRNADZOR_LITSENZIYA_ADRES, taimaut=30.0)
        if not isinstance(dannye, list):
            return []
        rezultaty = []
        for zapis in dannye:
            if not isinstance(zapis, dict):
                continue
            if nazvanie and nazvanie.lower() not in zapis.get("fullName", "").lower():
                continue
            if inn and inn != zapis.get("inn", ""):
                continue
            rezultaty.append(_razobrat_litsenziyu(zapis))
        return rezultaty
    except Exception:
        logger.exception("Ошибка при поиске лицензий")
        return []


async def poluchit_reyting(tip_reytinga: str = "", god: int = 0) -> list[dict[str, Any]]:
    """Получить рейтинг вузов.

    Аргументы:
        tip_reytinga: Тип рейтинга.
        god: Год рейтинга.

    Возвращает:
        Список рейтинговых данных.
    """
    try:
        adres_url = f"{VUZ_REYTING_ADRES}/api/rating"
        parametry: dict[str, Any] = {}
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if not isinstance(dannye, list):
            return []
        return [
            {
                "mesto_v_reytinge": r.get("position", ""),
                "nazvanie": r.get("name", ""),
                "ball": r.get("score", 0),
                "tip_reytinga": r.get("category", tip_reytinga),
                "gorod": r.get("city", ""),
            }
            for r in dannye
            if isinstance(r, dict)
        ]
    except Exception:
        logger.exception("Ошибка при получении рейтинга вузов")
        return []


async def poluchit_granty(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Получить информацию о грантах РНФ.

    Аргументы:
        organizatsiya: Организация-заявитель (необязательно).

    Возвращает:
        Список грантов.
    """
    return _granty_rezervnye(organizatsiya)


async def poluchit_aspirantov(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Получить данные об аспирантах.

    Аргументы:
        организatsiya: Организация (необязательно).

    Возвращает:
        Сведения об аспирантах.
    """
    return []


def _granty_rezervnye(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Справочная информация о фондах, выдающих гранты."""
    return [
        {
            "tip_granta": "Гранты РНФ",
            "nazvanie": "Программа РНФ",
            "rukovoditel": "",
            "summa_finansirovaniya": 0,
            "sostoyanie": "Для подачи заявки: https://rscf.ru",
        },
        {
            "tip_granta": "Гранты РФФИ",
            "nazvanie": "Программа РФФИ",
            "rukovoditel": "",
            "summa_finansirovaniya": 0,
            "sostoyanie": "Для подачи заявки: https://www.rfbr.ru",
        },
    ]


def _razobrat_akkreditatsiyu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи аккредитации из открытых данных Рособрнадзора."""
    return {
        "inn": zapis.get("inn", ""),
        "nazvanie": zapis.get("fullName", "") or zapis.get("shortName", ""),
        "tip": zapis.get("type", ""),
        "gorod": zapis.get("city", ""),
        "subiekt": zapis.get("subjectRF", ""),
        "status_akkreditatsii": zapis.get("accreditationStatus", ""),
        "data_akkreditatsii": zapis.get("accreditationDate", ""),
        "srok_deystviya": zapis.get("validUntil", ""),
        "nomer_svidetelstva": zapis.get("certificateNumber", ""),
        "adres": zapis.get("address", ""),
        "sayt": zapis.get("website", ""),
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }


def _razobrat_litsenziyu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи лицензии из открытых данных Рособрнадзора."""
    return {
        "inn": zapis.get("inn", ""),
        "nazvanie": zapis.get("fullName", "") or zapis.get("shortName", ""),
        "tip": zapis.get("type", ""),
        "gorod": zapis.get("city", ""),
        "subiekt": zapis.get("subjectRF", ""),
        "status_licenzii": zapis.get("licenseStatus", ""),
        "data_licenzii": zapis.get("licenseDate", ""),
        "nomer_licenzii": zapis.get("licenseNumber", ""),
        "srok_deystviya": zapis.get("validUntil", ""),
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }
