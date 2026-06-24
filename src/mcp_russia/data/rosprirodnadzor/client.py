"""HTTP-клиент для модуля Росприроднадзора.

Интеграция с реальными API:
    - Росприроднадзор: rpn.gov.ru
    - Открытые данные Росприроднадзора: rpn.gov.ru/opendata
    - Реестр ОНВ: onv.register.rpn.gov.ru
    - Госуслуги ЭКО: gosuslugi.ru/api/eco
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    GOSUSLUGI_EKO_BASE,
    KATEGORII_OBNV,
    ONV_REGISTER_BASE,
    ROSPRIRODNADZOR_API_BASE,
    ROSPRIRODNADZOR_OPENDATA_BASE,
    VIDY_LITSENZIY_NEDRA,
    VIDY_NADZORA,
)

logger = logging.getLogger(__name__)


async def poisk_proverok(
    organizaciya: str = "",
    vid_nadzora: str = "",
    god: int = 0,
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск экологических проверок Росприроднадзора.

    Аргументы:
        organizaciya: Название организации.
        vid_nadzora: Код вида надзора.
        god: Год проверки.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список проверок.
    """
    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/inspections"
        params: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            params["organization"] = organizaciya
        if vid_nadzora:
            params["supervisionType"] = vid_nadzora
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен")

    try:
        url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/inspections"
        params: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            params["organization"] = organizaciya
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru/opendata недоступен")

    return []


async def info_proverki(nomer: str) -> dict[str, Any] | None:
    """Получить информацию о проверке Росприроднадзора по номеру.

    Аргументы:
        nomer: Номер проверки.

    Возвращает:
        Данные проверки или None.
    """
    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/inspections/{nomer}"
        data = await http_poluchit(url, timeout=15.0)
        if isinstance(data, dict):
            return _razobrat_proverku(data)
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для проверки №%s", nomer)
        return None


async def poisk_obektov_negativnogo(
    organizaciya: str = "",
    kategoriya: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск объектов негативного воздействия в реестре ОНВ.

    Аргументы:
        organizaciya: Название организации.
        kategoriya: Категория ОНВ.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список объектов ОНВ.
    """
    try:
        url = f"{ONV_REGISTER_BASE}/search"
        params: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            params["name"] = organizaciya
        if kategoriya:
            params["category"] = kategoriya
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_obekt_negativnogo(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("ONV реестр недоступен")

    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/onv"
        params: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            params["organization"] = organizaciya
        if kategoriya:
            params["category"] = kategoriya
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_obekt_negativnogo(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для ОНВ")

    return []


async def poisk_litsenziy_nedra(
    territoriya: str = "",
    vid_litsenzii: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск лицензий на недропользование.

    Аргументы:
        territoriya: Территория действия лицензии.
        vid_litsenzii: Вид лицензии.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список лицензий.
    """
    try:
        url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/licenses"
        params: dict[str, Any] = {"limit": ogranichenie}
        if territoriya:
            params["territory"] = territoriya
        if vid_litsenzii:
            params["licenseType"] = vid_litsenzii
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_razobrat_litsenziyu(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru/opendata недоступен для лицензий")

    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/licenses"
        params: dict[str, Any] = {"limit": ogranichenie}
        if territoriya:
            params["territory"] = territoriya
        if vid_litsenzii:
            params["licenseType"] = vid_litsenzii
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        return [_razobrat_litsenziyu(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для лицензий")
        return []


async def poluchit_ekologicheskie_platezhi(
    god: int = 0,
    tip_platezha: str = "",
) -> list[dict[str, Any]]:
    """Получить данные об экологических платежах.

    Аргументы:
        god: Год.
        tip_platezha: Тип платежа.

    Возвращает:
        Список экологических платежей.
    """
    try:
        url = f"{GOSUSLUGI_EKO_BASE}/payments"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        if tip_platezha:
            params["paymentType"] = tip_platezha
        data = await http_poluchit(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        return [_razobrat_ekologicheskiy_platezh(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("Госуслуги ЭКО API недоступен")
        return []


def poluchit_spisok_vidov_nadzora() -> list[dict[str, str]]:
    """Вернуть справочник видов надзора Росприроднадзора."""
    return VIDY_NADZORA


def poluchit_spisok_kategoriy_obnv() -> list[dict[str, str]]:
    """Вернуть справочник категорий ОНВ."""
    return KATEGORII_OBNV


def poluchit_spisok_vidov_litsenziy_nedra() -> list[dict[str, str]]:
    """Вернуть справочник видов лицензий на недропользование."""
    return VIDY_LITSENZIY_NEDRA


def _izvlech_spisok(data: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_proverku(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных проверки Росприроднадзора."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "organizaciya": data.get("organization", "") or data.get("organizaciya", ""),
        "vid_nadzora": data.get("supervisionType", "") or data.get("vid_nadzora", ""),
        "data_nachala": data.get("startDate", "") or data.get("data_nachala", ""),
        "data_okonchaniya": data.get("endDate", "") or data.get("data_okonchaniya", ""),
        "status": data.get("status", ""),
        "vyavleno_narusheniy": data.get("violationsCount", 0)
        or data.get("vyavleno_narusheniy", 0),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_obekt_negativnogo(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных объекта негативного воздействия."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "kategoriya": data.get("category", "") or data.get("kategoriya", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "vid_deyatelnosti": data.get("activityType", "") or data.get("vid_deyatelnosti", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_litsenziyu(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных лицензии на недропользование."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "vid_litsenzii": data.get("licenseType", "") or data.get("vid_litsenzii", ""),
        "territoriya": data.get("territory", "") or data.get("region", ""),
        "srok_deystviya": data.get("validityPeriod", "") or data.get("srok_deystviya", ""),
        "derzhatel": data.get("holder", "") or data.get("derzhatel", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_ekologicheskiy_platezh(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных экологического платежа."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "tip_platezha": data.get("paymentType", "") or data.get("tip_platezha", ""),
        "summa": data.get("amount") or data.get("summa"),
        "god": data.get("year", "") or data.get("god", ""),
        "platelshchik": data.get("payer", "") or data.get("platelshchik", ""),
        "istochnik": "Госуслуги ЭКО (gosuslugi.ru)",
    }
