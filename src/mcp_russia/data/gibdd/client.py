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
    url = f"{GIBDD_CHECK_BASE}/auto/history/{vin}"
    try:
        data = await http_poluchit(url)
        return _razobrat_istoriyu(data, vin)
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
    url = f"{GIBDD_CHECK_BASE}/auto/dtp/{vin}"
    try:
        data = await http_poluchit(url)
        return _razobrat_dtp(data)
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
    url = f"{GIBDD_CHECK_BASE}/auto/wanted/{vin}"
    try:
        data = await http_poluchit(url)
        return _razobrat_rozysk(data)
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
    url = f"{GIBDD_CHECK_BASE}/auto/restrict/{vin}"
    try:
        data = await http_poluchit(url)
        return _razobrat_ogranichenie(data)
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
    url = f"{GIBDD_CHECK_BASE}/driver/{nomer_vu}"
    try:
        data = await http_poluchit(url)
        return _razobrat_voditelya(data, nomer_vu)
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
    url = f"{GIBDD_STAT_BASE}/map/dtp"
    params = {"region": subiekt, "year": str(god)}
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_statistiku(data, subiekt, god)
    except Exception:
        logger.exception("Ошибка при получении статистики ДТП для %s, %d", subiekt, god)
        return None


def _izvlech_rezultat(data: Any, klyuch: str) -> dict[str, Any]:
    """Извлечение секции результата из ответа API проверки ГИБДД.

    Типичный формат: {"RequestResult": {"result": {<key>: {...}}}}
    """
    if not isinstance(data, dict):
        return {}
    request_result = data.get("RequestResult", {})
    if not isinstance(request_result, dict):
        return {}
    result = request_result.get("result", {})
    if not isinstance(result, dict):
        return {}
    return result.get(klyuch, {})


def _razobrat_istoriyu(data: Any, vin: str) -> list[RegistracionnoeDeystvie]:
    """Разбор ответа истории регистрации ТС."""
    history = _izvlech_rezultat(data, "history")
    if not isinstance(history, dict):
        return []

    records = []
    for item in history.get("records", []) or []:
        if not isinstance(item, dict):
            continue
        records.append(
            RegistracionnoeDeystvie(
                vin=vin,
                gos_nomer=item.get("regNumber", ""),
                tip_deystviya=item.get("regAction", ""),
                data_deystviya=item.get("regDate", ""),
                subiekt=item.get("regRegion", ""),
            )
        )
    return records


def _razobrat_dtp(data: Any) -> list[dict[str, Any]]:
    """Разбор ответа истории ДТП."""
    dtp = _izvlech_rezultat(data, "dtp")
    if not isinstance(dtp, dict):
        return []

    records = []
    for item in dtp.get("records", []) or []:
        if not isinstance(item, dict):
            continue
        records.append(
            {
                "data_dtp": item.get("accidentDate", ""),
                "tip_dtp": item.get("accidentType", ""),
                "subiekt_dtp": item.get("regionName", ""),
                "model_ts": item.get("vehicleModel", ""),
                "god_vypuska": item.get("vehicleYear", ""),
                "status_ts": item.get("damageState", ""),
            }
        )
    return records


def _razobrat_rozysk(data: Any) -> list[dict[str, Any]]:
    """Разбор ответа о розыске ТС."""
    wanted = _izvlech_rezultat(data, "wanted")
    if not isinstance(wanted, dict):
        return []

    records = []
    for item in wanted.get("records", []) or []:
        if not isinstance(item, dict):
            continue
        records.append(
            {
                "data_rozyska": item.get("wantedDate", ""),
                "subiekt": item.get("wantedRegion", ""),
                "initsiator": item.get("wantedInitiator", ""),
                "model_ts": item.get("vehicleModel", ""),
                "god_vypuska": item.get("vehicleYear", ""),
                "nomer_dela": item.get("wantedNumpkio", ""),
            }
        )
    return records


def _razobrat_ogranichenie(data: Any) -> list[dict[str, Any]]:
    """Разбор ответа об ограничениях транспортного средства."""
    restrict = _izvlech_rezultat(data, "restrict")
    if not isinstance(restrict, dict):
        return []

    records = []
    for item in restrict.get("records", []) or []:
        if not isinstance(item, dict):
            continue
        records.append(
            {
                "data_ogranicheniya": item.get("dateadd", ""),
                "subiekt": item.get("regname", ""),
                "tip_ogranicheniya": item.get("restrictType", ""),
                "osnovanie": item.get("restrictBasis", ""),
                "initsiator": item.get("restrictInitiator", ""),
                "nomer_dela": item.get("restrictNumber", ""),
            }
        )
    return records


def _razobrat_voditelya(data: Any, nomer_vu: str) -> VoditelskoeUdostoverenie | None:
    """Разбор ответа проверки водительского удостоверения."""
    driver = _izvlech_rezultat(data, "driver")
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


def _razobrat_statistiku(data: Any, subiekt: str, god: int) -> StatistikaDTP | None:
    """Разбор ответа статистики ДТП."""
    if not isinstance(data, dict):
        return None

    stats = data.get("data", data)
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
