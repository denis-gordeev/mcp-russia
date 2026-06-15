"""HTTP-клиент для модуля Счётной палаты РФ.

Интеграция с реальными API:
    - Открытые данные Счётной палаты: ach.gov.ru
    - Портал бюджетных данных: budget.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    ACH_API_BASE,
    BUDGET_GOV_RU_BASE,
    NAPRAVLENIYA_KONTROLYA,
    SUBIEKTY_AUDITA,
    TIPY_MEROPRIYATIY,
)

logger = logging.getLogger(__name__)


async def poisk_kontrolnyh_meropriyatiy(
    napravlenie: str = "",
    status: str = "",
    god: int = 0,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Поиск контрольных мероприятий Счётной палаты.

    Args:
        napravlenie: Код направления контроля.
        status: Статус мероприятия.
        god: Год.
        limit: Максимум результатов.

    Returns:
        Список контрольных мероприятий.
    """
    try:
        url = f"{ACH_API_BASE}/controls"
        params: dict[str, Any] = {"limit": limit}
        if napravlenie:
            params["direction"] = napravlenie
        if status:
            params["status"] = status
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_kontrolnoe_meropriyatie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске контрольных мероприятий")
        return []


async def poluchit_kontrolnoe_meropriyatie(nomer: str) -> dict[str, Any] | None:
    """Получить контрольное мероприятие по номеру.

    Args:
        nomer: Номер мероприятия.

    Returns:
        Данные о мероприятии или None.
    """
    try:
        url = f"{ACH_API_BASE}/controls/{nomer}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_kontrolnoe_meropriyatie(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении мероприятия №%s", nomer)
        return None


async def poluchit_auditorskoe_zaklyuchenie(nomer: str) -> dict[str, Any] | None:
    """Получить аудиторское заключение по номеру.

    Args:
        nomer: Номер заключения.

    Returns:
        Данные о заключении или None.
    """
    try:
        url = f"{ACH_API_BASE}/conclusions/{nomer}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_auditorskoe_zaklyuchenie(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении заключения №%s", nomer)
        return None


async def poluchit_byudzhet_ispolnenie(
    period: str = "",
) -> dict[str, Any] | None:
    """Получить данные об исполнении федерального бюджета.

    Args:
        period: Период (год или квартал).

    Returns:
        Данные об исполнении бюджета или None.
    """
    try:
        url = f"{BUDGET_GOV_RU_BASE}/execution"
        params: dict[str, str] = {}
        if period:
            params["period"] = period
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            return _parse_byudzhet_ispolnenie(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении данных об исполнении бюджета")
        return None


async def poisk_narusheniy(
    organizaciya: str = "",
    tip: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Поиск выявленных нарушений.

    Args:
        organizaciya: Организация.
        tip: Тип нарушения.
        god: Год.

    Returns:
        Список нарушений.
    """
    try:
        url = f"{ACH_API_BASE}/violations"
        params: dict[str, Any] = {}
        if organizaciya:
            params["organization"] = organizaciya
        if tip:
            params["type"] = tip
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_narushenie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске нарушений")
        return []


def get_napravleniya_list() -> list[dict[str, str]]:
    """Вернуть справочник направлений контроля."""
    return NAPRAVLENIYA_KONTROLYA


def get_tipy_meropriyatiy_list() -> list[dict[str, str]]:
    """Вернуть справочник типов контрольных мероприятий."""
    return TIPY_MEROPRIYATIY


def get_subiekty_audita_list() -> list[dict[str, str]]:
    """Вернуть справочник субъектов аудита."""
    return SUBIEKTY_AUDITA


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


def _parse_kontrolnoe_meropriyatie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных контрольного мероприятия."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "tip": data.get("type", "") or data.get("tip", ""),
        "napravlenie": data.get("direction", "") or data.get("napravlenie", ""),
        "data_nachala": data.get("startDate", "") or data.get("data_nachala", ""),
        "data_okonchaniya": data.get("endDate", "") or data.get("data_okonchaniya", ""),
        "status": data.get("status", ""),
        "obiem_sredstv": data.get("amount") or data.get("obiem_sredstv"),
        "valyuta": "руб.",
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }


def _parse_auditorskoe_zaklyuchenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных аудиторского заключения."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "data_publikacii": data.get("publishDate", "") or data.get("data_publikacii", ""),
        "obekt_audita": data.get("auditObject", "") or data.get("obekt_audita", ""),
        "napravlenie": data.get("direction", "") or data.get("napravlenie", ""),
        "vyavleno_narusheniy": data.get("violationsCount", 0)
        or data.get("vyavleno_narusheniy", 0),
        "summa_narusheniy": data.get("violationsAmount") or data.get("summa_narusheniy"),
        "rekomendacii": data.get("recommendations", []) or data.get("rekomendacii", []),
        "ispolnenie": data.get("execution", "") or data.get("ispolnenie", ""),
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }


def _parse_byudzhet_ispolnenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об исполнении бюджета."""
    return {
        "period": data.get("period", "") or data.get("year", ""),
        "dohody": data.get("revenue") or data.get("income") or data.get("dohody"),
        "raskhody": data.get("expenditure") or data.get("expenses") or data.get("raskhody"),
        "deficit": data.get("deficit"),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _parse_narushenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о нарушении."""
    return {
        "opisanie": data.get("description", "") or data.get("opisanie", ""),
        "summa": data.get("amount") or data.get("summa"),
        "tip_narusheniya": data.get("type", "") or data.get("tip_narusheniya", ""),
        "organizaciya": data.get("organization", "") or data.get("organizaciya", ""),
        "norma_prava": data.get("legalNorm", "") or data.get("norma_prava", ""),
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }
