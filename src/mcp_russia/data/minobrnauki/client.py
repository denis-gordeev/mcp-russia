"""HTTP-клиент для модуля Минобрнауки.

Интеграция с реальными API:
    - Рособрнадзор (аккредитация): obrnadzor.gov.ru/opendata
    - Реестр лицензий: obrnadzor.gov.ru/opendata
    - Рейтинг вузов: vuz.minobrnauki.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    OBRNADZOR_ACCRED_URL,
    OBRNADZOR_LICENSE_URL,
    VUZ_RATING_URL,
)

logger = logging.getLogger(__name__)


async def poisk_akreditovannyh_vuzov(
    nazvanie: str = "",
    inn: str = "",
    region: str = "",
) -> list[dict[str, Any]]:
    """Поиск аккредитованных образовательных учреждений через Рособрнадзор.

    Аргументы:
        nazvanie: Название вуза (частичное совпадение).
        inn: ИНН организации.
        region: Регион (субъект РФ).

    Возвращает:
        Список аккредитованных учреждений.
    """
    try:
        data = await http_get(OBRNADZOR_ACCRED_URL, timeout=30.0)
        if not isinstance(data, list):
            return []
        results = []
        for item in data:
            if not isinstance(item, dict):
                continue
            if nazvanie and nazvanie.lower() not in item.get("fullName", "").lower():
                continue
            if inn and inn != item.get("inn", ""):
                continue
            if region and region.lower() not in item.get("subjectRF", "").lower():
                continue
            results.append(_parse_akkreditaciya(item))
        return results
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
        data = await http_get(OBRNADZOR_ACCRED_URL, timeout=30.0)
        if not isinstance(data, list):
            return None
        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("inn") == inn:
                return _parse_akkreditaciya(item)
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
        data = await http_get(OBRNADZOR_LICENSE_URL, timeout=30.0)
        if not isinstance(data, list):
            return []
        results = []
        for item in data:
            if not isinstance(item, dict):
                continue
            if nazvanie and nazvanie.lower() not in item.get("fullName", "").lower():
                continue
            if inn and inn != item.get("inn", ""):
                continue
            results.append(_parse_licenziya(item))
        return results
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
        url = f"{VUZ_RATING_URL}/api/rating"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        if not isinstance(data, list):
            return []
        return [
            {
                "mesto_v_reytinge": r.get("position", ""),
                "nazvanie": r.get("name", ""),
                "ball": r.get("score", 0),
                "tip_reytinga": r.get("category", tip_reytinga),
                "gorod": r.get("city", ""),
            }
            for r in data
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
    return _granty_fallback(organizatsiya)


async def poluchit_aspirantov(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Получить данные об аспирантах.

    Аргументы:
        организatsiya: Организация (необязательно).

    Возвращает:
        Сведения об аспирантах.
    """
    return []


def _granty_fallback(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Справочная информация о фондах, выдающих гранты."""
    return [
        {
            "tip_granta": "Гранты РНФ",
            "nazvanie": "Программа РНФ",
            "rukovoditel": "",
            "summa_finansirovaniya": 0,
            "status": "Для подачи заявки: https://rscf.ru",
        },
        {
            "tip_granta": "Гранты РФФИ",
            "nazvanie": "Программа РФФИ",
            "rukovoditel": "",
            "summa_finansirovaniya": 0,
            "status": "Для подачи заявки: https://www.rfbr.ru",
        },
    ]


def _parse_akkreditaciya(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи аккредитации из открытых данных Рособрнадзора."""
    return {
        "inn": item.get("inn", ""),
        "nazvanie": item.get("fullName", "") or item.get("shortName", ""),
        "tip": item.get("type", ""),
        "gorod": item.get("city", ""),
        "region": item.get("subjectRF", ""),
        "status_akkreditatsii": item.get("accreditationStatus", ""),
        "data_akkreditatsii": item.get("accreditationDate", ""),
        "srok_deystviya": item.get("validUntil", ""),
        "nomer_svidetelstva": item.get("certificateNumber", ""),
        "adres": item.get("address", ""),
        "sayt": item.get("website", ""),
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }


def _parse_licenziya(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи лицензии из открытых данных Рособрнадзора."""
    return {
        "inn": item.get("inn", ""),
        "nazvanie": item.get("fullName", "") or item.get("shortName", ""),
        "tip": item.get("type", ""),
        "gorod": item.get("city", ""),
        "region": item.get("subjectRF", ""),
        "status_licenzii": item.get("licenseStatus", ""),
        "data_licenzii": item.get("licenseDate", ""),
        "nomer_licenzii": item.get("licenseNumber", ""),
        "srok_deystviya": item.get("validUntil", ""),
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }
