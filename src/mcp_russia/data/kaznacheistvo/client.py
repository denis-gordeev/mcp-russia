"""HTTP-клиент для модуля Федерального казначейства.

Интеграция с реальными API:
    - Федеральное казначейство: roskazna.gov.ru
    - Портал бюджетных данных: budget.gov.ru/api
    - Открытые данные: data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    BUDGET_GOV_RU_BASE,
    KATEGORII_RASKHODOV,
    KAZNACHEISTVO_API_BASE,
    ROSKAZNA_OPENDATA_BASE,
    VIDY_BUDZHETOV,
)

logger = logging.getLogger(__name__)


async def poluchit_ispolnenie_byudzheta(
    god: int = 0,
    tip: str = "",
) -> dict[str, Any] | None:
    """Получить данные об исполнении федерального бюджета.

    Args:
        god: Год.
        tip: Тип бюджета.

    Returns:
        Данные об исполнении бюджета или None.
    """
    try:
        url = f"{BUDGET_GOV_RU_BASE}/v1/execution"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        if tip:
            params["budgetType"] = tip
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            return _parse_ispolnenie_byudzheta(data)
    except Exception:
        logger.debug("budget.gov.ru API недоступен")

    try:
        url = f"{KAZNACHEISTVO_API_BASE}/execution"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        if tip:
            params["budgetType"] = tip
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            return _parse_ispolnenie_byudzheta(data)
    except Exception:
        logger.debug("roskazna.gov.ru API недоступен")

    return None


async def poisk_uchastnikov_bp(
    inn: str = "",
    nazvanie: str = "",
) -> list[dict[str, Any]]:
    """Поиск участников бюджетного процесса.

    Args:
        inn: ИНН организации.
        nazvanie: Название организации.

    Returns:
        Список участников бюджетного процесса.
    """
    try:
        url = f"{ROSKAZNA_OPENDATA_BASE}/participants"
        params: dict[str, str] = {}
        if inn:
            params["inn"] = inn
        if nazvanie:
            params["name"] = nazvanie
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_uchastnik_bp(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("roskazna.gov.ru открытые данные недоступны")
        return []


async def poisk_uchrezhdeniy(
    inn: str = "",
    nazvanie: str = "",
    tip: str = "",
) -> list[dict[str, Any]]:
    """Поиск казённых учреждений.

    Args:
        inn: ИНН учреждения.
        nazvanie: Название учреждения.
        tip: Тип учреждения.

    Returns:
        Список учреждений.
    """
    try:
        url = f"{ROSKAZNA_OPENDATA_BASE}/institutions"
        params: dict[str, str] = {}
        if inn:
            params["inn"] = inn
        if nazvanie:
            params["name"] = nazvanie
        if tip:
            params["type"] = tip
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_uchrezhdenie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("roskazna.gov.ru открытые данные недоступны")
        return []


async def poluchit_mezhbyudzhetnye(
    god: int = 0,
    region: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о межбюджетных трансфертах.

    Args:
        god: Год.
        region: Регион.

    Returns:
        Список межбюджетных трансфертов.
    """
    try:
        url = f"{BUDGET_GOV_RU_BASE}/v1/interbudget"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_mezhbyudzhetnyy_transfer(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("budget.gov.ru API недоступен для межбюджетных трансфертов")
        return []


async def poluchit_byudzhetnuyu_smetu(nomer: str) -> dict[str, Any] | None:
    """Получить бюджетную смету по номеру.

    Args:
        nomer: Номер сметы.

    Returns:
        Данные бюджетной сметы или None.
    """
    try:
        url = f"{KAZNACHEISTVO_API_BASE}/estimates/{nomer}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_byudzhetnaya_smeta(data)
    except Exception:
        logger.debug("roskazna.gov.ru API недоступен для сметы №%s", nomer)
        return None


def get_vidy_byudzhetov_list() -> list[dict[str, str]]:
    """Вернуть справочник видов бюджетов."""
    return VIDY_BUDZHETOV


def get_kategorii_raskhodov_list() -> list[dict[str, str]]:
    """Вернуть справочник категорий расходов."""
    return KATEGORII_RASKHODOV


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


def _parse_ispolnenie_byudzheta(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об исполнении бюджета."""
    return {
        "period": data.get("period", "") or data.get("year", ""),
        "tip": data.get("budgetType", "") or data.get("tip", ""),
        "dohody": data.get("revenue") or data.get("income") or data.get("dohody"),
        "raskhody": data.get("expenditure") or data.get("expenses") or data.get("raskhody"),
        "deficit": data.get("deficit"),
        "status": data.get("status", ""),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _parse_uchastnik_bp(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных участника бюджетного процесса."""
    return {
        "inn": data.get("inn", "") or data.get("id", ""),
        "nazvanie": data.get("name", "") or data.get("nazvanie", ""),
        "tip_uchastnika": data.get("participantType", "") or data.get("tip_uchastnika", ""),
        "byudzhet": data.get("budget", "") or data.get("byudzhet", ""),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }


def _parse_uchrezhdenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных казённого учреждения."""
    return {
        "inn": data.get("inn", "") or data.get("id", ""),
        "nazvanie": data.get("name", "") or data.get("nazvanie", ""),
        "tip": data.get("type", "") or data.get("tip", ""),
        "osnovnoj_vid_deyatelnosti": data.get("mainActivity", "")
        or data.get("osnovnoj_vid_deyatelnosti", ""),
        "osnovanie": data.get("basis", "") or data.get("osnovanie", ""),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }


def _parse_mezhbyudzhetnyy_transfer(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных межбюджетного трансферта."""
    return {
        "vid": data.get("type", "") or data.get("vid", ""),
        "otpravitel": data.get("sender", "") or data.get("otpravitel", ""),
        "poluchatel": data.get("receiver", "") or data.get("poluchatel", ""),
        "summa": data.get("amount") or data.get("summa"),
        "god": str(data.get("year", "")) or data.get("god", ""),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _parse_byudzhetnaya_smeta(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных бюджетной сметы."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "tip": data.get("type", "") or data.get("tip", ""),
        "god": str(data.get("year", "")) or data.get("god", ""),
        "dohody": data.get("revenue") or data.get("income") or data.get("dohody"),
        "raskhody": data.get("expenditure") or data.get("expenses") or data.get("raskhody"),
        "deficit": data.get("deficit"),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }
