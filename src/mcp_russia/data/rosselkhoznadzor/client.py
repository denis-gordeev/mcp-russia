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
        url = f"{FSVPS_API_BASE}/inspections"
        params: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            params["region"] = subiekt
        if vid_nadzora:
            params["supervisionType"] = vid_nadzora
        if tip_proverki:
            params["inspectionType"] = tip_proverki
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("fsvps.gov.ru API недоступен для проверок")

    try:
        url = f"{FSVPS_OPENDATA_BASE}/inspections"
        params = {"limit": ogranichenie}
        if subiekt:
            params["region"] = subiekt
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
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
        url = f"{FSVPS_API_BASE}/quarantine"
        params: dict[str, Any] = {}
        if subiekt:
            params["region"] = subiekt
        if tip:
            params["type"] = tip
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_karantin(p) for p in items if isinstance(p, dict)]
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
        url = f"{FSVPS_API_BASE}/registrations"
        params: dict[str, Any] = {"limit": ogranichenie}
        if tip_produktsii:
            params["productType"] = tip_produktsii
        if proizvoditel:
            params["manufacturer"] = proizvoditel
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_registratsiyu(p) for p in items if isinstance(p, dict)]
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
        url = f"{FSVPS_API_BASE}/certificates"
        params: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            params["region"] = subiekt
        if tip_produktsii:
            params["productType"] = tip_produktsii
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_sertifikat(p) for p in items if isinstance(p, dict)]
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
        url = f"{FSVPS_API_BASE}/warnings"
        params: dict[str, Any] = {}
        if subiekt:
            params["region"] = subiekt
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_preduprezhdenie(p) for p in items if isinstance(p, dict)]
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


def _izvlech_spisok(data: Any) -> list[Any]:
    """Извлечь список из ответа API."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_proverku(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о проверке."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "vid_nadzora": data.get("supervisionType", "") or data.get("vid_nadzora", ""),
        "tip_proverki": data.get("inspectionType", "") or data.get("tip_proverki", ""),
        "data_provedeniya": data.get("date", "") or data.get("data_provedeniya", ""),
        "subiekt": data.get("region", "") or data.get("subject", ""),
        "status": data.get("status", ""),
        "narusheniya": data.get("violations", 0) or data.get("narusheniya", 0),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_karantin(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о карантинном объекте."""
    return {
        "nazvanie": data.get("name", "") or data.get("nazvanie", ""),
        "tip": data.get("type", "") or data.get("tip", ""),
        "subiekt": data.get("region", "") or data.get("subject", ""),
        "status_karantina": data.get("quarantineStatus", "") or data.get("status_karantina", ""),
        "data_vvedeniya": data.get("startDate", "") or data.get("data_vvedeniya", ""),
        "opisanie": data.get("description", "") or data.get("opisanie", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_registratsiyu(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о регистрации продукции."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "naimenovanie": data.get("name", "") or data.get("naimenovanie", ""),
        "proizvoditel": data.get("manufacturer", "") or data.get("proizvoditel", ""),
        "tip_produktsii": data.get("productType", "") or data.get("tip_produktsii", ""),
        "data_registratsii": data.get("registrationDate", "") or data.get("data_registratsii", ""),
        "srok_deystviya": data.get("validUntil", "") or data.get("srok_deystviya", ""),
        "sostoyanie": data.get("status", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_sertifikat(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о ветеринарном сертификате."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "tip_produktsii": data.get("productType", "") or data.get("tip_produktsii", ""),
        "otpravitel": data.get("sender", "") or data.get("otpravitel", ""),
        "poluchatel": data.get("receiver", "") or data.get("poluchatel", ""),
        "data_oformleniya": data.get("date", "") or data.get("data_oformleniya", ""),
        "region_otpravki": data.get("senderRegion", "") or data.get("region_otpravki", ""),
        "sostoyanie": data.get("status", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }


def _razobrat_preduprezhdenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных предупреждения о карантине."""
    return {
        "nomer": data.get("id", "") or data.get("nomer", ""),
        "subiekt": data.get("region", "") or data.get("subject", ""),
        "opisanie": data.get("description", "") or data.get("opisanie", ""),
        "tip_karantina": data.get("quarantineType", "") or data.get("tip_karantina", ""),
        "data_nachala": data.get("startDate", "") or data.get("data_nachala", ""),
        "data_okonchaniya": data.get("endDate", "") or data.get("data_okonchaniya", ""),
        "istochnik": "Россельхознадзор (fsvps.gov.ru)",
    }
