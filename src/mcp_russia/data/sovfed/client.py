"""HTTP-клиент для модуля Совета Федерации РФ.

Интеграция с реальными API:
    - Официальный сайт Совета Федерации: sovfed.ru
    - Открытые данные data.gov.ru: датасеты Совета Федерации
    - Сенаторы, комитеты, законопроекты через API sovfed.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    DATA_GOV_RU_SOVFED,
    KOMISSII_SOVFEDA,
    KOMITETY_SOVFEDA,
    SENATORY_SPRAVOCHNIK,
    SOVFED_API_BASE,
)

logger = logging.getLogger(__name__)


async def poisk_senatorov(
    region: str = "",
    komitet: str = "",
) -> list[dict[str, Any]]:
    """Поиск сенаторов Совета Федерации.

    Args:
        region: Регион представительства.
        komitet: Комитет.

    Returns:
        Список сенаторов.
    """
    try:
        url = f"{SOVFED_API_BASE}/senators"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        if komitet:
            params["committee"] = komitet
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_senator(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен, пробуем data.gov.ru")

    try:
        url = f"{DATA_GOV_RU_SOVFED}"
        params: dict[str, Any] = {"organization": "sovet_federatsii", "limit": 50}
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_senator(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("data.gov.ru API недоступен")

    if region or komitet:
        return [
            s
            for s in SENATORY_SPRAVOCHNIK
            if (not region or region.lower() in s.get("region", "").lower())
            and (not komitet or komitet.lower() in s.get("komitet", "").lower())
        ]

    return SENATORY_SPRAVOCHNIK


async def info_senatora(senator_id: str) -> dict[str, Any] | None:
    """Получить подробную информацию о сенаторе.

    Args:
        senator_id: Идентификатор или фамилия сенатора.

    Returns:
        Данные сенатора или None.
    """
    try:
        url = f"{SOVFED_API_BASE}/senators/{senator_id}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_senator(data)
    except Exception:
        logger.debug("sovfed.ru API недоступен для сенатора %s", senator_id)

    for s in SENATORY_SPRAVOCHNIK:
        if senator_id in (s.get("familiya", ""), str(s.get("nomer", ""))):
            return s
    return None


async def spisok_komitetov() -> list[dict[str, Any]]:
    """Получить список комитетов Совета Федерации из API sovfed.ru."""
    try:
        url = f"{SOVFED_API_BASE}/committees"
        data = await http_get(url, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_komitet(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для комитетов")

    return []


async def spisok_komissiy() -> list[dict[str, Any]]:
    """Получить список комиссий Совета Федерации из API sovfed.ru."""
    try:
        url = f"{SOVFED_API_BASE}/commissions"
        data = await http_get(url, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_komitet(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для комиссий")

    return []


async def poisk_zakonoproektov(
    status: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Поиск законопроектов Совета Федерации.

    Args:
        status: Статус законопроекта.
        god: Год рассмотрения.

    Returns:
        Список законопроектов.
    """
    try:
        url = f"{SOVFED_API_BASE}/bills"
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_zakonoproekt(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для законопроектов")
        return []


async def spisok_zasedaniy(god: int = 0) -> list[dict[str, Any]]:
    """Получить список заседаний Совета Федерации.

    Args:
        god: Год.

    Returns:
        Список заседаний.
    """
    try:
        url = f"{SOVFED_API_BASE}/sessions"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_zasedanie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для заседаний")
        return []


def get_komitety_list() -> list[dict[str, str]]:
    """Вернуть справочник комитетов Совета Федерации."""
    return KOMITETY_SOVFEDA


def get_komissii_list() -> list[dict[str, str]]:
    """Вернуть справочник комиссий Совета Федерации."""
    return KOMISSII_SOVFEDA


def _extract_list(data: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _parse_senator(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных сенатора."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "familiya": data.get("lastName", "") or data.get("familiya", ""),
        "imya": data.get("firstName", "") or data.get("imya", ""),
        "otchestvo": data.get("middleName", "") or data.get("otchestvo", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "dolzhnost": data.get("position", "") or data.get("dolzhnost", ""),
        "komitet": data.get("committee", "") or data.get("komitet", ""),
        "frakciya": data.get("faction", "") or data.get("frakciya", ""),
        "data_naznacheniya": data.get("appointmentDate", "") or data.get("data_naznacheniya", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _parse_komitet(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных комитета/комиссии."""
    return {
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "predsedatel": data.get("chairman", "") or data.get("predsedatel", ""),
        "kolichestvo_chlenov": data.get("membersCount", 0) or data.get("kolichestvo_chlenov", 0),
        "napravlenie": data.get("direction", "") or data.get("napravlenie", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _parse_zasedanie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных заседания."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "data": data.get("date", "") or data.get("data", ""),
        "status": data.get("status", ""),
        "povestka": data.get("agenda", "") or data.get("povestka", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _parse_zakonoproekt(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных законопроекта."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "status": data.get("status", ""),
        "data_rassmotreniya": data.get("reviewDate", "") or data.get("data_rassmotreniya", ""),
        "iniciator": data.get("initiator", "") or data.get("iniciator", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }
