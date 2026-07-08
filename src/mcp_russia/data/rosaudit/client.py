"""HTTP-клиент для модуля Счётной палаты РФ.

Интеграция с реальными API:
    - Открытые данные Счётной палаты: ach.gov.ru
    - Портал бюджетных данных: budget.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    ACH_BAZA_API,
    BUDGET_GOV_RU_BAZA,
    NAPRAVLENIYA_KONTROLYA,
    SUBIEKTY_AUDITA,
    TIPY_MEROPRIYATIY,
)

logger = logging.getLogger(__name__)


async def poisk_kontrolnyh_meropriyatiy(
    napravlenie: str = "",
    sostoyanie: str = "",
    god: int = 0,
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск контрольных мероприятий Счётной палаты.

    Аргументы:
        napravlenie: Код направления контроля.
        sostoyanie: Статус мероприятия.
        god: Год.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список контрольных мероприятий.
    """
    try:
        adres_url = f"{ACH_BAZA_API}/controls"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if napravlenie:
            parametry["direction"] = napravlenie
        if sostoyanie:
            parametry["status"] = sostoyanie
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_kontrolnoe_meropriyatie(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске контрольных мероприятий")
        return []


async def poluchit_kontrolnoe_meropriyatie(nomer: str) -> dict[str, Any] | None:
    """Получить контрольное мероприятие по номеру.

    Аргументы:
        nomer: Номер мероприятия.

    Возвращает:
        Данные о мероприятии или None.
    """
    try:
        adres_url = f"{ACH_BAZA_API}/controls/{nomer}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_kontrolnoe_meropriyatie(dannye)
        return None
    except Exception:
        logger.exception("Ошибка при получении мероприятия №%s", nomer)
        return None


async def poluchit_auditorskoe_zaklyuchenie(nomer: str) -> dict[str, Any] | None:
    """Получить аудиторское заключение по номеру.

    Аргументы:
        nomer: Номер заключения.

    Возвращает:
        Данные о заключении или None.
    """
    try:
        adres_url = f"{ACH_BAZA_API}/conclusions/{nomer}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_auditorskoe_zaklyuchenie(dannye)
        return None
    except Exception:
        logger.exception("Ошибка при получении заключения №%s", nomer)
        return None


async def poluchit_byudzhet_ispolnenie(
    period: str = "",
) -> dict[str, Any] | None:
    """Получить данные об исполнении федерального бюджета.

    Аргументы:
        period: Период (год или квартал).

    Возвращает:
        Данные об исполнении бюджета или None.
    """
    try:
        adres_url = f"{BUDGET_GOV_RU_BAZA}/execution"
        parametry: dict[str, str] = {}
        if period:
            parametry["period"] = period
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_ispolnenie_byudzheta(dannye)
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

    Аргументы:
        organizaciya: Организация.
        tip: Тип нарушения.
        god: Год.

    Возвращает:
        Список нарушений.
    """
    try:
        adres_url = f"{ACH_BAZA_API}/violations"
        parametry: dict[str, Any] = {}
        if organizaciya:
            parametry["organization"] = organizaciya
        if tip:
            parametry["type"] = tip
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_narushenie(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске нарушений")
        return []


def poluchit_spisok_napravleniy() -> list[dict[str, str]]:
    """Вернуть справочник направлений контроля."""
    return NAPRAVLENIYA_KONTROLYA


def poluchit_spisok_tipov_meropriyatiy() -> list[dict[str, str]]:
    """Вернуть справочник типов контрольных мероприятий."""
    return TIPY_MEROPRIYATIY


def poluchit_spisok_subiektov_audita() -> list[dict[str, str]]:
    """Вернуть справочник субъектов аудита."""
    return SUBIEKTY_AUDITA


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for klyuch in ("data", "items", "results", "records"):
            znachenie_spiska = dannye.get(klyuch)
            if isinstance(znachenie_spiska, list):
                return znachenie_spiska
    return []


def _razobrat_kontrolnoe_meropriyatie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных контрольного мероприятия."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "tip": dannye.get("type", "") or dannye.get("tip", ""),
        "napravlenie": dannye.get("direction", "") or dannye.get("napravlenie", ""),
        "data_nachala": dannye.get("startDate", "") or dannye.get("data_nachala", ""),
        "data_okonchaniya": dannye.get("endDate", "") or dannye.get("data_okonchaniya", ""),
        "sostoyanie": dannye.get("status", ""),
        "obiem_sredstv": dannye.get("amount") or dannye.get("obiem_sredstv"),
        "valyuta": "руб.",
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }


def _razobrat_auditorskoe_zaklyuchenie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных аудиторского заключения."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "data_publikacii": dannye.get("publishDate", "") or dannye.get("data_publikacii", ""),
        "obekt_audita": dannye.get("auditObject", "") or dannye.get("obekt_audita", ""),
        "napravlenie": dannye.get("direction", "") or dannye.get("napravlenie", ""),
        "vyavleno_narusheniy": dannye.get("violationsCount", 0)
        or dannye.get("vyavleno_narusheniy", 0),
        "summa_narusheniy": dannye.get("violationsAmount") or dannye.get("summa_narusheniy"),
        "rekomendacii": dannye.get("recommendations", []) or dannye.get("rekomendacii", []),
        "ispolnenie": dannye.get("execution", "") or dannye.get("ispolnenie", ""),
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }


def _razobrat_ispolnenie_byudzheta(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об исполнении бюджета."""
    return {
        "period": dannye.get("period", "") or dannye.get("year", ""),
        "dohody": dannye.get("revenue") or dannye.get("income") or dannye.get("dohody"),
        "raskhody": dannye.get("expenditure") or dannye.get("expenses") or dannye.get("raskhody"),
        "defitsit": dannye.get("deficit"),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _razobrat_narushenie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о нарушении."""
    return {
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "summa": dannye.get("amount") or dannye.get("summa"),
        "tip_narusheniya": dannye.get("type", "") or dannye.get("tip_narusheniya", ""),
        "organizaciya": dannye.get("organization", "") or dannye.get("organizaciya", ""),
        "norma_prava": dannye.get("legalNorm", "") or dannye.get("norma_prava", ""),
        "istochnik": "Счётная палата РФ (ach.gov.ru)",
    }
