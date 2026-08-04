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

from .constants import GIBDD_BAZA_PROVEROK, GIBDD_BAZA_STATISTIKI
from .schemas import (
    RegistratsionnoeDeystvie,
    StatistikaDTP,
    VoditelskoeUdostoverenie,
)

logger = logging.getLogger(__name__)


async def proverka_istorii_ts(vin: str) -> list[RegistratsionnoeDeystvie]:
    """Проверка истории регистрации ТС через API ГИБДД.

    Аргументы:
        vin: VIN-номер (17 символов).

    Возвращает:
        Список регистрационных действий.
    """
    adres_url = f"{GIBDD_BAZA_PROVEROK}/auto/history/{vin}"
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
    adres_url = f"{GIBDD_BAZA_PROVEROK}/auto/dtp/{vin}"
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
    adres_url = f"{GIBDD_BAZA_PROVEROK}/auto/wanted/{vin}"
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
    adres_url = f"{GIBDD_BAZA_PROVEROK}/auto/restrict/{vin}"
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
    adres_url = f"{GIBDD_BAZA_PROVEROK}/driver/{nomer_vu}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_voditelya(dannye, nomer_vu)
    except Exception:
        logger.exception("Ошибка при проверке ВУ %s", nomer_vu)
        return None


async def statistika_dtp_region(subiekt: str, god: int) -> StatistikaDTP | None:
    """Получение статистики ДТП с stat.gibdd.ru.

    Аргументы:
        subiekt: Название региона (субъект РФ).
        god: Год для статистики.

    Возвращает:
        Статистика ДТП или None.
    """
    adres_url = f"{GIBDD_BAZA_STATISTIKI}/map/dtp"
    parametry = {"region": subiekt, "year": str(god)}
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_statistiku(dannye, subiekt, god)
    except Exception:
        logger.exception("Ошибка при получении статистики ДТП для %s, %d", subiekt, god)
        return None


def _izvlech_rezultat(dannye: Any, klyuch: str) -> Any:
    """Извлечение секции результата из ответа API проверки ГИБДД.

    Типичный формат: {"RequestResult": {"result": {<key>: {...}}}}
    """
    if not isinstance(dannye, dict):
        return {}
    rezultat_zaprosa = dannye.get("RequestResult", {})
    if not isinstance(rezultat_zaprosa, dict):
        return {}
    rezultat = rezultat_zaprosa.get("result", {})
    if not isinstance(rezultat, dict):
        return {}
    return rezultat.get(klyuch, {})


def _razobrat_istoriyu(dannye: Any, vin: str) -> list[RegistratsionnoeDeystvie]:
    """Разбор ответа истории регистрации ТС."""
    istoriya = _izvlech_rezultat(dannye, "history")
    if not isinstance(istoriya, dict):
        return []

    zapisi = []
    for zapis in istoriya.get("records", []) or []:
        if not isinstance(zapis, dict):
            continue
        zapisi.append(
            RegistratsionnoeDeystvie(
                vin=vin,
                gos_nomer=zapis.get("regNumber", ""),
                tip_deystviya=zapis.get("regAction", ""),
                data_deystviya=zapis.get("regDate", ""),
                subiekt=zapis.get("regRegion", ""),
            )
        )
    return zapisi


def _razobrat_dtp(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа истории ДТП."""
    dtp_dannye = _izvlech_rezultat(dannye, "dtp")
    if not isinstance(dtp_dannye, dict):
        return []

    zapisi = []
    for zapis in dtp_dannye.get("records", []) or []:
        if not isinstance(zapis, dict):
            continue
        zapisi.append(
            {
                "data_dtp": zapis.get("accidentDate", ""),
                "tip_dtp": zapis.get("accidentType", ""),
                "subiekt_dtp": zapis.get("regionName", ""),
                "model_ts": zapis.get("vehicleModel", ""),
                "god_vypuska": zapis.get("vehicleYear", ""),
                "sostoyanie_ts": zapis.get("damageState", ""),
            }
        )
    return zapisi


def _razobrat_rozysk(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа о розыске ТС."""
    razyskivaemye = _izvlech_rezultat(dannye, "wanted")
    if not isinstance(razyskivaemye, dict):
        return []

    zapisi = []
    for zapis in razyskivaemye.get("records", []) or []:
        if not isinstance(zapis, dict):
            continue
        zapisi.append(
            {
                "data_rozyska": zapis.get("wantedDate", ""),
                "subiekt": zapis.get("wantedRegion", ""),
                "initsiator": zapis.get("wantedInitiator", ""),
                "model_ts": zapis.get("vehicleModel", ""),
                "god_vypuska": zapis.get("vehicleYear", ""),
                "nomer_dela": zapis.get("wantedNumpkio", ""),
            }
        )
    return zapisi


def _razobrat_ogranichenie(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа об ограничениях транспортного средства."""
    ogranicheniya_dannye = _izvlech_rezultat(dannye, "restrict")
    if not isinstance(ogranicheniya_dannye, dict):
        return []

    zapisi = []
    for zapis in ogranicheniya_dannye.get("records", []) or []:
        if not isinstance(zapis, dict):
            continue
        zapisi.append(
            {
                "data_ogranicheniya": zapis.get("dateadd", ""),
                "subiekt": zapis.get("regname", ""),
                "tip_ogranicheniya": zapis.get("restrictType", ""),
                "osnovanie": zapis.get("restrictBasis", ""),
                "initsiator": zapis.get("restrictInitiator", ""),
                "nomer_dela": zapis.get("restrictNumber", ""),
            }
        )
    return zapisi


def _razobrat_voditelya(dannye: Any, nomer_vu: str) -> VoditelskoeUdostoverenie | None:
    """Разбор ответа проверки водительского удостоверения."""
    voditel_dannye = _izvlech_rezultat(dannye, "driver")
    if not isinstance(voditel_dannye, dict):
        return None

    chasti_fio = []
    if voditel_dannye.get("lastName"):
        chasti_fio.append(voditel_dannye["lastName"])
    if voditel_dannye.get("firstName"):
        chasti_fio.append(voditel_dannye["firstName"])
    if voditel_dannye.get("middleName"):
        chasti_fio.append(voditel_dannye["middleName"])

    kategorii_vu = []
    for kategoriya in voditel_dannye.get("categories", []) or []:
        if isinstance(kategoriya, dict):
            kategorii_vu.append(kategoriya.get("category", ""))

    return VoditelskoeUdostoverenie(
        nomer_vu=nomer_vu,
        kategoriya=", ".join(kategorii_vu),
        data_vydachi=voditel_dannye.get("dateIssue", ""),
        srok_deystviya=voditel_dannye.get("dateExpiry", ""),
        fio=" ".join(chasti_fio),
        mesto_rozhdeniya=voditel_dannye.get("birthPlace", ""),
        ograniceniya=voditel_dannye.get("restriction", ""),
        osoboie_otmetki=voditel_dannye.get("specialNote", ""),
        sostoyanie=voditel_dannye.get("status", ""),
    )


def _razobrat_statistiku(dannye: Any, subiekt: str, god: int) -> StatistikaDTP | None:
    """Разбор ответа статистики ДТП."""
    if not isinstance(dannye, dict):
        return None

    statistika = dannye.get("data", dannye)
    if not isinstance(statistika, dict):
        return None

    return StatistikaDTP(
        subiekt=subiekt,
        god=god,
        kolichestvo_dtp=int(statistika.get("dtpCount", 0) or 0),
        pogibshie=int(statistika.get("deadCount", 0) or 0),
        ranennye=int(statistika.get("injuredCount", 0) or 0),
        dtp_s_peshchodami=int(statistika.get("pedestrianDtpCount", 0) or 0),
        dtp_s_detmi=int(statistika.get("childDtpCount", 0) or 0),
        alco_gibdd=int(statistika.get("drunkDtpCount", 0) or 0),
    )
