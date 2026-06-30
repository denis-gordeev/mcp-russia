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
        adres_url = f"{ROSPRIRODNADZOR_API_BASE}/inspections"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            parametry["organization"] = organizaciya
        if vid_nadzora:
            parametry["supervisionType"] = vid_nadzora
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен")

    try:
        adres_url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/inspections"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            parametry["organization"] = organizaciya
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{ROSPRIRODNADZOR_API_BASE}/inspections/{nomer}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_proverku(dannye)
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
        adres_url = f"{ONV_REGISTER_BASE}/search"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            parametry["name"] = organizaciya
        if kategoriya:
            parametry["category"] = kategoriya
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_obekt_negativnogo(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("ONV реестр недоступен")

    try:
        adres_url = f"{ROSPRIRODNADZOR_API_BASE}/onv"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if organizaciya:
            parametry["organization"] = organizaciya
        if kategoriya:
            parametry["category"] = kategoriya
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_obekt_negativnogo(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/licenses"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if territoriya:
            parametry["territory"] = territoriya
        if vid_litsenzii:
            parametry["licenseType"] = vid_litsenzii
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_litsenziyu(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru/opendata недоступен для лицензий")

    try:
        adres_url = f"{ROSPRIRODNADZOR_API_BASE}/licenses"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if territoriya:
            parametry["territory"] = territoriya
        if vid_litsenzii:
            parametry["licenseType"] = vid_litsenzii
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_litsenziyu(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{GOSUSLUGI_EKO_BASE}/payments"
        parametry: dict[str, Any] = {}
        if god:
            parametry["year"] = god
        if tip_platezha:
            parametry["paymentType"] = tip_platezha
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_ekologicheskiy_platezh(p) for p in elementy if isinstance(p, dict)]
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


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for key in ("data", "items", "results", "records"):
            val = dannye.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_proverku(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных проверки Росприроднадзора."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "organizaciya": dannye.get("organization", "") or dannye.get("organizaciya", ""),
        "vid_nadzora": dannye.get("supervisionType", "") or dannye.get("vid_nadzora", ""),
        "data_nachala": dannye.get("startDate", "") or dannye.get("data_nachala", ""),
        "data_okonchaniya": dannye.get("endDate", "") or dannye.get("data_okonchaniya", ""),
        "sostoyanie": dannye.get("status", ""),
        "vyavleno_narusheniy": dannye.get("violationsCount", 0)
        or dannye.get("vyavleno_narusheniy", 0),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_obekt_negativnogo(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных объекта негативного воздействия."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "nazvanie": dannye.get("title", "")
        or dannye.get("name", "")
        or dannye.get("nazvanie", ""),
        "kategoriya": dannye.get("category", "") or dannye.get("kategoriya", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "vid_deyatelnosti": dannye.get("activityType", "") or dannye.get("vid_deyatelnosti", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_litsenziyu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных лицензии на недропользование."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "vid_litsenzii": dannye.get("licenseType", "") or dannye.get("vid_litsenzii", ""),
        "territoriya": dannye.get("territory", "") or dannye.get("region", ""),
        "srok_deystviya": dannye.get("validityPeriod", "") or dannye.get("srok_deystviya", ""),
        "derzhatel": dannye.get("holder", "") or dannye.get("derzhatel", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _razobrat_ekologicheskiy_platezh(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных экологического платежа."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "tip_platezha": dannye.get("paymentType", "") or dannye.get("tip_platezha", ""),
        "summa": dannye.get("amount") or dannye.get("summa"),
        "god": dannye.get("year", "") or dannye.get("god", ""),
        "platelshchik": dannye.get("payer", "") or dannye.get("platelshchik", ""),
        "istochnik": "Госуслуги ЭКО (gosuslugi.ru)",
    }
