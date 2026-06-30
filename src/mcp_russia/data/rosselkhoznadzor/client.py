"""HTTP-клиент для модуля Россельхознадзор.

Интеграция с реальными API:
    - Россельхознадзор: fsvps.gov.ru
    - Открытые данные: data.fsvps.gov.ru
    - Портал открытых данных: data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    FEDERALNYE_OKRUGA_RSKHN,
    FSVPS_API_BASE,
    FSVPS_OPENDATA_BASE,
    KARANTINNYE_OBYEKTY,
    KATEGORII_PROVEROK,
    STATISTIKA_RSKHN_2023,
    TIPY_PRODUKTSII,
    VIDY_NADZORA,
    VIDY_NARUSHENIY_RSKHN,
)

logger = logging.getLogger(__name__)


async def poisk_proverok(
    subiekt: str = "",
    vid_nadzora: str = "",
    tip_proverki: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск проверок Россельхознадзора.

    Аргументы:
        region: Регион.
        vid_nadzora: Вид надзора.
        tip_proverki: Тип проверки.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список проверок.
    """
    try:
        adres_url = f"{FSVPS_API_BASE}/inspections"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if vid_nadzora:
            parametry["supervisionType"] = vid_nadzora
        if tip_proverki:
            parametry["inspectionType"] = tip_proverki
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для проверок")

    try:
        adres_url = f"{FSVPS_OPENDATA_BASE}/inspections"
        parametry = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("data.fsvps.gov.ru недоступен")

    return []


async def poisk_karantinnykh_obektov(
    subiekt: str = "",
    tip: str = "",
) -> list[dict[str, Any]]:
    """Поиск карантинных объектов.

    Аргументы:
        region: Регион.
        tip: Тип карантинного объекта.

    Возвращает:
        Список карантинных объектов.
    """
    try:
        adres_url = f"{FSVPS_API_BASE}/quarantine"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if tip:
            parametry["type"] = tip
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_karantin(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для карантинных объектов")

    return []


async def poisk_registratsiy_produktsii(
    tip_produktsii: str = "",
    proizvoditel: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск зарегистрированной продукции.

    Аргументы:
        tip_produktsii: Тип продукции.
        proizvoditel: Производитель.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список зарегистрированной продукции.
    """
    try:
        adres_url = f"{FSVPS_API_BASE}/registrations"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if tip_produktsii:
            parametry["productType"] = tip_produktsii
        if proizvoditel:
            parametry["manufacturer"] = proizvoditel
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_registratsiyu(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для регистрации продукции")

    return []


async def veterinarsnye_sertifikaty(
    subiekt: str = "",
    tip_produktsii: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск ветеринарных сертификатов.

    Аргументы:
        region: Регион отправки.
        tip_produktsii: Тип продукции.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список ветеринарных сертификатов.
    """
    try:
        adres_url = f"{FSVPS_API_BASE}/certificates"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if tip_produktsii:
            parametry["productType"] = tip_produktsii
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_sertifikat(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для ветеринарных сертификатов")

    return []


async def preduprezhdeniya_karantina(
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Получить предупреждения о карантинных ограничениях.

    Аргументы:
        region: Регион.

    Возвращает:
        Список предупреждений.
    """
    try:
        adres_url = f"{FSVPS_API_BASE}/warnings"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_preduprezhdenie(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для предупреждений")

    return []


def poluchit_spisok_vidov_nadzora() -> list[dict[str, str]]:
    """Вернуть справочник видов надзора."""
    return VIDY_NADZORA


def poluchit_spisok_kategoriy_proverok() -> list[dict[str, str]]:
    """Вернуть справочник категорий проверок."""
    return KATEGORII_PROVEROK


def poluchit_spisok_vidov_narusheniy() -> list[dict[str, str]]:
    """Вернуть справочник видов нарушений."""
    return VIDY_NARUSHENIY_RSKHN


def poluchit_spisok_tipov_produktsii() -> list[dict[str, str]]:
    """Вернуть справочник типов продукции."""
    return TIPY_PRODUKTSII


def poluchit_spisok_karantinnykh_obektov() -> list[dict[str, str]]:
    """Вернуть справочник карантинных объектов."""
    return KARANTINNYE_OBYEKTY


def poluchit_spisok_federalnykh_okrugov() -> list[dict[str, Any]]:
    """Вернуть справочник федеральных округов Россельхознадзора."""
    return FEDERALNYE_OKRUGA_RSKHN


def poluchit_statistiku_rskhn_staticheskie() -> dict[str, Any]:
    """Вернуть статическую статистику Россельхознадзора (2023)."""
    return STATISTIKA_RSKHN_2023


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for key in ("data", "items", "results", "records"):
            val = dannye.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_proverku(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о проверке."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "vid_nadzora": dannye.get("supervisionType", "") or dannye.get("vid_nadzora", ""),
        "tip_proverki": dannye.get("inspectionType", "") or dannye.get("tip_proverki", ""),
        "data_provedeniya": dannye.get("date", "") or dannye.get("data_provedeniya", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "sostoyanie": dannye.get("status", ""),
        "narusheniya": dannye.get("violations", 0) or dannye.get("narusheniya", 0),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_karantin(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о карантинном объекте."""
    return {
        "nazvanie": dannye.get("name", "") or dannye.get("nazvanie", ""),
        "tip": dannye.get("type", "") or dannye.get("tip", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "status_karantina": dannye.get("quarantineStatus", "")
        or dannye.get("status_karantina", ""),
        "data_vvedeniya": dannye.get("startDate", "") or dannye.get("data_vvedeniya", ""),
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_registratsiyu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о регистрации продукции."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "naimenovanie": dannye.get("name", "") or dannye.get("naimenovanie", ""),
        "proizvoditel": dannye.get("manufacturer", "") or dannye.get("proizvoditel", ""),
        "tip_produktsii": dannye.get("productType", "") or dannye.get("tip_produktsii", ""),
        "data_registratsii": dannye.get("registrationDate", "")
        or dannye.get("data_registratsii", ""),
        "srok_deystviya": dannye.get("validUntil", "") or dannye.get("srok_deystviya", ""),
        "sostoyanie": dannye.get("status", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_sertifikat(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о ветеринарном сертификате."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "tip_produktsii": dannye.get("productType", "") or dannye.get("tip_produktsii", ""),
        "otpravitel": dannye.get("sender", "") or dannye.get("otpravitel", ""),
        "poluchatel": dannye.get("receiver", "") or dannye.get("poluchatel", ""),
        "data_oformleniya": dannye.get("date", "") or dannye.get("data_oformleniya", ""),
        "region_otpravki": dannye.get("senderRegion", "") or dannye.get("region_otpravki", ""),
        "sostoyanie": dannye.get("status", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_preduprezhdenie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных предупреждения о карантине."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("nomer", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "tip_karantina": dannye.get("quarantineType", "") or dannye.get("tip_karantina", ""),
        "data_nachala": dannye.get("startDate", "") or dannye.get("data_nachala", ""),
        "data_okonchaniya": dannye.get("endDate", "") or dannye.get("data_okonchaniya", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }
