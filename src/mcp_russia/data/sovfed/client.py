"""HTTP-клиент для модуля Совета Федерации РФ.

Интеграция с реальными API:
    - Официальный сайт Совета Федерации: sovfed.ru
    - Открытые данные data.gov.ru: датасеты Совета Федерации
    - Сенаторы, комитеты, законопроекты через API sovfed.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    DANNYE_GOV_RU_SOVFED,
    KOMISSII_SOVFEDA,
    KOMITETY_SOVFEDA,
    SENATORY_SPRAVOCHNIK,
    SOVFED_BAZA_API,
)

logger = logging.getLogger(__name__)


async def poisk_senatorov(
    subiekt: str = "",
    komitet: str = "",
) -> list[dict[str, Any]]:
    """Поиск сенаторов Совета Федерации.

    Аргументы:
        subiekt: Регион представительства.
        komitet: Комитет.

    Возвращает:
        Список сенаторов.
    """
    try:
        adres_url = f"{SOVFED_BAZA_API}/senators"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if komitet:
            parametry["committee"] = komitet
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_senator(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен, пробуем data.gov.ru")

    try:
        adres_url = f"{DANNYE_GOV_RU_SOVFED}"
        parametry_dannye: dict[str, Any] = {"organization": "sovet_federatsii", "limit": 50}
        dannye = await http_poluchit(adres_url, parametry=parametry_dannye, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_senator(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("data.gov.ru API недоступен")

    if subiekt or komitet:
        return [
            senator
            for senator in SENATORY_SPRAVOCHNIK
            if (not subiekt or subiekt.lower() in senator.get("subiekt", "").lower())
            and (not komitet or komitet.lower() in senator.get("komitet", "").lower())
        ]

    return SENATORY_SPRAVOCHNIK


async def info_senatora(identifikator_senatora: str) -> dict[str, Any] | None:
    """Получить подробную информацию о сенаторе.

    Аргументы:
        identifikator_senatora: Идентификатор или фамилия сенатора.

    Возвращает:
        Данные сенатора или None.
    """
    try:
        adres_url = f"{SOVFED_BAZA_API}/senators/{identifikator_senatora}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_senator(dannye)
    except Exception:
        logger.debug("sovfed.ru API недоступен для сенатора %s", identifikator_senatora)

    for senator in SENATORY_SPRAVOCHNIK:
        if identifikator_senatora in (senator.get("familiya", ""), str(senator.get("nomer", ""))):
            return senator
    return None


async def spisok_komitetov() -> list[dict[str, Any]]:
    """Получить список комитетов Совета Федерации из API sovfed.ru."""
    try:
        adres_url = f"{SOVFED_BAZA_API}/committees"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_komitet(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для комитетов")

    return []


async def spisok_komissiy() -> list[dict[str, Any]]:
    """Получить список комиссий Совета Федерации из API sovfed.ru."""
    try:
        adres_url = f"{SOVFED_BAZA_API}/commissions"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_komitet(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для комиссий")

    return []


async def poisk_zakonoproektov(
    sostoyanie: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Поиск законопроектов Совета Федерации.

    Аргументы:
        sostoyanie: Статус законопроекта.
        god: Год рассмотрения.

    Возвращает:
        Список законопроектов.
    """
    try:
        adres_url = f"{SOVFED_BAZA_API}/bills"
        parametry: dict[str, Any] = {}
        if sostoyanie:
            parametry["status"] = sostoyanie
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_zakonoproekt(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для законопроектов")
        return []


async def spisok_zasedaniy(god: int = 0) -> list[dict[str, Any]]:
    """Получить список заседаний Совета Федерации.

    Аргументы:
        god: Год.

    Возвращает:
        Список заседаний.
    """
    try:
        adres_url = f"{SOVFED_BAZA_API}/sessions"
        parametry: dict[str, Any] = {}
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_zasedanie(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("sovfed.ru API недоступен для заседаний")
        return []


def poluchit_spisok_komitetov() -> list[dict[str, str]]:
    """Вернуть справочник комитетов Совета Федерации."""
    return KOMITETY_SOVFEDA


def poluchit_spisok_komissiy() -> list[dict[str, str]]:
    """Вернуть справочник комиссий Совета Федерации."""
    return KOMISSII_SOVFEDA


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


def _razobrat_senator(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных сенатора."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "familiya": dannye.get("lastName", "") or dannye.get("familiya", ""),
        "imya": dannye.get("firstName", "") or dannye.get("imya", ""),
        "otchestvo": dannye.get("middleName", "") or dannye.get("otchestvo", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "dolzhnost": dannye.get("position", "") or dannye.get("dolzhnost", ""),
        "komitet": dannye.get("committee", "") or dannye.get("komitet", ""),
        "fraktsiya": dannye.get("faction", "") or dannye.get("fraktsiya", ""),
        "data_naznacheniya": dannye.get("appointmentDate", "")
        or dannye.get("data_naznacheniya", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _razobrat_komitet(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных комитета/комиссии."""
    return {
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "predsedatel": dannye.get("chairman", "") or dannye.get("predsedatel", ""),
        "kolichestvo_chlenov": dannye.get("membersCount", 0)
        or dannye.get("kolichestvo_chlenov", 0),
        "napravlenie": dannye.get("direction", "") or dannye.get("napravlenie", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _razobrat_zasedanie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных заседания."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "data": dannye.get("date", "") or dannye.get("data", ""),
        "sostoyanie": dannye.get("status", ""),
        "povestka": dannye.get("agenda", "") or dannye.get("povestka", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }


def _razobrat_zakonoproekt(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных законопроекта."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "sostoyanie": dannye.get("status", ""),
        "data_rassmotreniya": dannye.get("reviewDate", "") or dannye.get("data_rassmotreniya", ""),
        "iniciator": dannye.get("initiator", "") or dannye.get("iniciator", ""),
        "istochnik": "Совет Федерации РФ (sovfed.ru)",
    }
