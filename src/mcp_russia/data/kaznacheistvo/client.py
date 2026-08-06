"""HTTP-клиент для модуля Федерального казначейства.

Интеграция с реальными API:
    - Федеральное казначейство: roskazna.gov.ru
    - Портал бюджетных данных: budget.gov.ru/api
    - Открытые данные: data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    BYUDZHET_GOV_RU_BAZA,
    KATEGORII_RASKHODOV,
    KAZNACHEISTVO_BAZA_API,
    PODRAZDELY_BYUDZHETNOY_KLASSIFIKATSII,
    RAZDELY_BYUDZHETNOY_KLASSIFIKATSII,
    ROSKAZNA_BAZA_OTKRYTYKH_DANNYKH,
    VIDY_BUDZHETOV,
)

logger = logging.getLogger(__name__)


async def poluchit_ispolnenie_byudzheta(
    god: int = 0,
    tip: str = "",
    razdel: str = "",
    podrazdel: str = "",
) -> dict[str, Any] | None:
    """Получить данные об исполнении федерального бюджета.

    Аргументы:
        god: Год.
        tip: Тип бюджета.
        razdel: Код раздела бюджетной классификации.
        podrazdel: Код подраздела бюджетной классификации.

    Возвращает:
        Данные об исполнении бюджета или None.
    """
    try:
        adres_url = f"{BYUDZHET_GOV_RU_BAZA}/v1/execution"
        parametry: dict[str, Any] = {}
        if god:
            parametry["year"] = god
        if tip:
            parametry["budgetType"] = tip
        if razdel:
            parametry["section"] = razdel
        if podrazdel:
            parametry["subsection"] = podrazdel
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_ispolnenie_byudzheta(dannye)
    except Exception:
        logger.debug("budget.gov.ru API недоступен")

    try:
        adres_url = f"{KAZNACHEISTVO_BAZA_API}/execution"
        parametry_kaznacheistvo: dict[str, Any] = {}
        if god:
            parametry_kaznacheistvo["year"] = god
        if tip:
            parametry_kaznacheistvo["budgetType"] = tip
        dannye = await http_poluchit(adres_url, parametry=parametry_kaznacheistvo, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_ispolnenie_byudzheta(dannye)
    except Exception:
        logger.debug("roskazna.gov.ru API недоступен")

    return None


async def poisk_uchastnikov_bp(
    inn: str = "",
    nazvanie: str = "",
) -> list[dict[str, Any]]:
    """Поиск участников бюджетного процесса.

    Аргументы:
        inn: ИНН организации.
        nazvanie: Название организации.

    Возвращает:
        Список участников бюджетного процесса.
    """
    try:
        adres_url = f"{ROSKAZNA_BAZA_OTKRYTYKH_DANNYKH}/participants"
        parametry: dict[str, str] = {}
        if inn:
            parametry["inn"] = inn
        if nazvanie:
            parametry["name"] = nazvanie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_uchastnik_bp(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("roskazna.gov.ru открытые данные недоступны")
        return []


async def poisk_uchrezhdeniy(
    inn: str = "",
    nazvanie: str = "",
    tip: str = "",
) -> list[dict[str, Any]]:
    """Поиск казённых учреждений.

    Аргументы:
        inn: ИНН учреждения.
        nazvanie: Название учреждения.
        tip: Тип учреждения.

    Возвращает:
        Список учреждений.
    """
    try:
        adres_url = f"{ROSKAZNA_BAZA_OTKRYTYKH_DANNYKH}/institutions"
        parametry: dict[str, str] = {}
        if inn:
            parametry["inn"] = inn
        if nazvanie:
            parametry["name"] = nazvanie
        if tip:
            parametry["type"] = tip
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_uchrezhdenie(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("roskazna.gov.ru открытые данные недоступны")
        return []


async def poluchit_mezhbyudzhetnye(
    god: int = 0,
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о межбюджетных трансфертах.

    Аргументы:
        god: Год.
        subiekt: Регион.

    Возвращает:
        Список межбюджетных трансфертов.
    """
    try:
        adres_url = f"{BYUDZHET_GOV_RU_BAZA}/v1/interbudget"
        parametry: dict[str, Any] = {}
        if god:
            parametry["year"] = god
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [
            _razobrat_mezhbyudzhetnyy_transfer(zapis)
            for zapis in elementy
            if isinstance(zapis, dict)
        ]
    except Exception:
        logger.debug("budget.gov.ru API недоступен для межбюджетных трансфертов")
        return []


async def poluchit_byudzhetnuyu_smetu(nomer: str) -> dict[str, Any] | None:
    """Получить бюджетную смету по номеру.

    Аргументы:
        nomer: Номер сметы.

    Возвращает:
        Данные бюджетной сметы или None.
    """
    try:
        adres_url = f"{KAZNACHEISTVO_BAZA_API}/estimates/{nomer}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_byudzhetnuyu_smetu(dannye)
    except Exception:
        logger.debug("roskazna.gov.ru API недоступен для сметы №%s", nomer)
        return None

    return None


def poluchit_spisok_vidov_byudzhetov() -> list[dict[str, str]]:
    """Вернуть справочник видов бюджетов."""
    return VIDY_BUDZHETOV


def poluchit_spisok_kategoriy_raskhodov() -> list[dict[str, str]]:
    """Вернуть справочник категорий расходов."""
    return KATEGORII_RASKHODOV


def poluchit_spisok_razdelov_byudzheta() -> list[dict[str, str]]:
    """Вернуть справочник разделов бюджетной классификации."""
    return RAZDELY_BYUDZHETNOY_KLASSIFIKATSII


def poluchit_spisok_podrazdelov_byudzheta(razdel: str = "") -> list[dict[str, str]]:
    """Вернуть справочник подразделов бюджетной классификации.

    Аргументы:
        razdel: Код раздела для фильтрации (необязательно).
    """
    if not razdel:
        return PODRAZDELY_BYUDZHETNOY_KLASSIFIKATSII
    return [
        podrazdel
        for podrazdel in PODRAZDELY_BYUDZHETNOY_KLASSIFIKATSII
        if podrazdel["razdel"] == razdel
    ]


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


def _razobrat_ispolnenie_byudzheta(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об исполнении бюджета."""
    return {
        "period": dannye.get("period", "") or dannye.get("year", ""),
        "tip": dannye.get("budgetType", "") or dannye.get("tip", ""),
        "dohody": dannye.get("revenue") or dannye.get("income") or dannye.get("dohody"),
        "raskhody": dannye.get("expenditure") or dannye.get("expenses") or dannye.get("raskhody"),
        "defitsit": dannye.get("deficit"),
        "sostoyanie": dannye.get("status", ""),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _razobrat_uchastnik_bp(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных участника бюджетного процесса."""
    return {
        "inn": dannye.get("inn", "") or dannye.get("id", ""),
        "nazvanie": dannye.get("name", "") or dannye.get("nazvanie", ""),
        "tip_uchastnika": dannye.get("participantType", "") or dannye.get("tip_uchastnika", ""),
        "byudzhet": dannye.get("budget", "") or dannye.get("byudzhet", ""),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }


def _razobrat_uchrezhdenie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных казённого учреждения."""
    return {
        "inn": dannye.get("inn", "") or dannye.get("id", ""),
        "nazvanie": dannye.get("name", "") or dannye.get("nazvanie", ""),
        "tip": dannye.get("type", "") or dannye.get("tip", ""),
        "osnovnoy_vid_deyatelnosti": dannye.get("mainActivity", "")
        or dannye.get("osnovnoy_vid_deyatelnosti", ""),
        "osnovanie": dannye.get("basis", "") or dannye.get("osnovanie", ""),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }


def _razobrat_mezhbyudzhetnyy_transfer(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных межбюджетного трансферта."""
    return {
        "vid": dannye.get("type", "") or dannye.get("vid", ""),
        "otpravitel": dannye.get("sender", "") or dannye.get("otpravitel", ""),
        "poluchatel": dannye.get("receiver", "") or dannye.get("poluchatel", ""),
        "summa": dannye.get("amount") or dannye.get("summa"),
        "god": str(dannye.get("year", "")) or dannye.get("god", ""),
        "istochnik": "Портал бюджетных данных (budget.gov.ru)",
    }


def _razobrat_byudzhetnuyu_smetu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных бюджетной сметы."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "tip": dannye.get("type", "") or dannye.get("tip", ""),
        "god": str(dannye.get("year", "")) or dannye.get("god", ""),
        "dohody": dannye.get("revenue") or dannye.get("income") or dannye.get("dohody"),
        "raskhody": dannye.get("expenditure") or dannye.get("expenses") or dannye.get("raskhody"),
        "defitsit": dannye.get("deficit"),
        "istochnik": "Федеральное казначейство (roskazna.gov.ru)",
    }
