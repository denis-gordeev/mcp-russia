"""HTTP-клиент для модуля ГИБДД/МВД.

Интеграция с реальными API:
    - Проверка ТС: https://гибдд.рф/check/auto
    - Проверка ВУ: https://гибдд.рф/check/driver
    - Статистика ДТП: https://stat.gibdd.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import GIBDD_CHECK_BASE, GIBDD_STAT_BASE
from .schemas import (
    RegistracionnoeDeystvie,
    StatistikaDTP,
    VoditelskoeUdostoverenie,
)

logger = logging.getLogger(__name__)


async def proverka_istorii_ts(vin: str) -> list[RegistracionnoeDeystvie]:
    """Проверка истории регистрации ТС через API ГИБДД.

    Аргументы:
        vin: VIN-номер (17 символов).

    Возвращает:
        Список регистрационных действий.
    """
    adres_url = f"{GIBDD_CHECK_BASE}/auto/history/{vin}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_istoriyu(dannye, vin)
    except Exception:
        logger.exception("Ошибка при проверке истории ТС по VIN %s", vin)
        return []


async def proverka_dtp_ts(vin: str) -> list[dict[str, Any]]:
    """Проверка истории ДТП через API ГИБДД.

    Аргументы:
        vin: VIN-номер (17 символов).

    Возвращает:
        Список записей о ДТП.
    """
    adres_url = f"{GIBDD_CHECK_BASE}/auto/dtp/{vin}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_dtp(dannye)
    except Exception:
        logger.exception("Ошибка при проверке ДТП по VIN %s", vin)
        return []


async def proverka_rozysk_ts(vin: str) -> list[dict[str, Any]]:
    """Проверка нахождения ТС в розыске через API ГИБДД.

    Аргументы:
        vin: VIN-номер (17 символов).

    Возвращает:
        Список записей о розыске.
    """
    adres_url = f"{GIBDD_CHECK_BASE}/auto/wanted/{vin}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_rozysk(dannye)
    except Exception:
        logger.exception("Ошибка при проверке розыска ТС по VIN %s", vin)
        return []


async def proverka_ogranicheniy_ts(vin: str) -> list[dict[str, Any]]:
    """Проверка ограничений на регистрацию ТС через API ГИБДД.

    Аргументы:
        vin: VIN-номер (17 символов).

    Возвращает:
        Список записей об ограничениях.
    """
    adres_url = f"{GIBDD_CHECK_BASE}/auto/restrict/{vin}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_ogranichenie(dannye)
    except Exception:
        logger.exception("Ошибка при проверке ограничений ТС по VIN %s", vin)
        return []


async def proverka_vu(nomer_vu: str) -> VoditelskoeUdostoverenie | None:
    """Проверка действительности ВУ через API ГИБДД.

    Аргументы:
        nomer_vu: Номер водительского удостоверения (10 цифр, без пробелов).

    Возвращает:
        Данные ВУ или None.
    """
    adres_url = f"{GIBDD_CHECK_BASE}/driver/{nomer_vu}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_voditelya(dannye, nomer_vu)
    except Exception:
        logger.exception("Ошибка при проверке ВУ %s", nomer_vu)
        return None


async def statistika_dtp_region(subiekt: str, god: int) -> StatistikaDTP | None:
    """Получение статистики ДТП с stat.gibdd.ru.

    Аргументы:
        region: Название региона (субъект РФ).
        god: Год для статистики.

    Возвращает:
        Статистика ДТП или None.
    """
    adres_url = f"{GIBDD_STAT_BASE}/map/dtp"
    parametry = {"region": subiekt, "year": str(god)}
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_statistiku(dannye, subiekt, god)
    except Exception:
        logger.exception("Ошибка при получении статистики ДТП для %s, %d", subiekt, god)
        return None


def _izvlech_rezultat(dannye: Any, klyuch: str) -> dict[str, Any]:
    """Извлечение секции результата из ответа API проверки ГИБДД.

    Типичный формат: {"RequestResult": {"result": {<key>: {...}}}}
    """
    if not isinstance(dannye, dict):
        return {}
    request_result = dannye.get("RequestResult", {})
    if not isinstance(request_result, dict):
        return {}
    rezultat = request_result.get("result", {})
    if not isinstance(rezultat, dict):
        return {}
    return rezultat.get(klyuch, {})


def _razobrat_istoriyu(dannye: Any, vin: str) -> list[RegistracionnoeDeystvie]:
    """Разбор ответа истории регистрации ТС."""
    history = _izvlech_rezultat(dannye, "history")
    if not isinstance(history, dict):
        return []

    zapisi = []
    for element in history.get("records", []) or []:
        if not isinstance(element, dict):
            continue
        zapisi.append(
            RegistracionnoeDeystvie(
                vin=vin,
                gos_nomer=element.get("regNumber", ""),
                tip_deystviya=element.get("regAction", ""),
                data_deystviya=element.get("regDate", ""),
                subiekt=element.get("regRegion", ""),
            )
        )
    return zapisi


def _razobrat_dtp(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа истории ДТП."""
    dtp = _izvlech_rezultat(dannye, "dtp")
    if not isinstance(dtp, dict):
        return []

    zapisi = []
    for element in dtp.get("records", []) or []:
        if not isinstance(element, dict):
            continue
        zapisi.append(
            {
                "data_dtp": element.get("accidentDate", ""),
                "tip_dtp": element.get("accidentType", ""),
                "subiekt_dtp": element.get("regionName", ""),
                "model_ts": element.get("vehicleModel", ""),
                "god_vypuska": element.get("vehicleYear", ""),
                "status_ts": element.get("damageState", ""),
            }
        )
    return zapisi


def _razobrat_rozysk(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа о розыске ТС."""
    razyskivaemye = _izvlech_rezultat(dannye, "wanted")
    if not isinstance(razyskivaemye, dict):
        return []

    zapisi = []
    for element in razyskivaemye.get("records", []) or []:
        if not isinstance(element, dict):
            continue
        zapisi.append(
            {
                "data_rozyska": element.get("wantedDate", ""),
                "subiekt": element.get("wantedRegion", ""),
                "initsiator": element.get("wantedInitiator", ""),
                "model_ts": element.get("vehicleModel", ""),
                "god_vypuska": element.get("vehicleYear", ""),
                "nomer_dela": element.get("wantedNumpkio", ""),
            }
        )
    return zapisi


def _razobrat_ogranichenie(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа об ограничениях транспортного средства."""
    restrict = _izvlech_rezultat(dannye, "restrict")
    if not isinstance(restrict, dict):
        return []

    zapisi = []
    for element in restrict.get("records", []) or []:
        if not isinstance(element, dict):
            continue
        zapisi.append(
            {
                "data_ogranicheniya": element.get("dateadd", ""),
                "subiekt": element.get("regname", ""),
                "tip_ogranicheniya": element.get("restrictType", ""),
                "osnovanie": element.get("restrictBasis", ""),
                "initsiator": element.get("restrictInitiator", ""),
                "nomer_dela": element.get("restrictNumber", ""),
            }
        )
    return zapisi


def _razobrat_voditelya(dannye: Any, nomer_vu: str) -> VoditelskoeUdostoverenie | None:
    """Разбор ответа проверки водительского удостоверения."""
    driver = _izvlech_rezultat(dannye, "driver")
    if not isinstance(driver, dict):
        return None

    fio_parts = []
    if driver.get("lastName"):
        fio_parts.append(driver["lastName"])
    if driver.get("firstName"):
        fio_parts.append(driver["firstName"])
    if driver.get("middleName"):
        fio_parts.append(driver["middleName"])

    categories = []
    for cat in driver.get("categories", []) or []:
        if isinstance(cat, dict):
            categories.append(cat.get("category", ""))

    return VoditelskoeUdostoverenie(
        nomer_vu=nomer_vu,
        kategoriya=", ".join(categories),
        data_vydachi=driver.get("dateIssue", ""),
        srok_deystviya=driver.get("dateExpiry", ""),
        fio=" ".join(fio_parts),
        mesto_rozhdeniya=driver.get("birthPlace", ""),
        ograniceniya=driver.get("restriction", ""),
        osoboie_otmetki=driver.get("specialNote", ""),
        sostoyanie=driver.get("status", ""),
    )


def _razobrat_statistiku(dannye: Any, subiekt: str, god: int) -> StatistikaDTP | None:
    """Разбор ответа статистики ДТП."""
    if not isinstance(dannye, dict):
        return None

    stats = dannye.get("data", dannye)
    if not isinstance(stats, dict):
        return None

    return StatistikaDTP(
        subiekt=subiekt,
        god=god,
        kolichestvo_dtp=int(stats.get("dtpCount", 0) or 0),
        pogibshie=int(stats.get("deadCount", 0) or 0),
        ranennye=int(stats.get("injuredCount", 0) or 0),
        dtp_s_peshchodami=int(stats.get("pedestrianDtpCount", 0) or 0),
        dtp_s_detmi=int(stats.get("childDtpCount", 0) or 0),
        alco_gibdd=int(stats.get("drunkDtpCount", 0) or 0),
    )
