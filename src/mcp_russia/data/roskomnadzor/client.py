"""HTTP-клиент для модуля Роскомнадзора.

Интеграция с реальными API:
    - Реестр операторов ПД: rkn.gov.ru/pdn
    - Реестр ОРИ: rkn.gov.ru/registry-ori
    - Единый реестр запрещённых сайтов: eais.rkn.gov.ru
    - Открытые данные: rkn.gov.ru/it/opendata
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    EAIS_BAZA_API,
    RKN_BAZA_API,
)

logger = logging.getLogger(__name__)


async def poisk_operatora_pd(inn: str = "", nazvanie: str = "") -> list[dict[str, Any]]:
    """Поиск оператора персональных данных в реестре Роскомнадзора.

    Аргументы:
        inn: ИНН организации.
        nazvanie: Название организации.

    Возвращает:
        Список операторов ПД.
    """
    try:
        adres_url = f"{RKN_BAZA_API}/pdn/search"
        parametry: dict[str, Any] = {}
        if inn:
            parametry["inn"] = inn
        if nazvanie:
            parametry["name"] = nazvanie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [
                    _razobrat_operatora_pd(zapis) for zapis in elementy if isinstance(zapis, dict)
                ]
        if isinstance(dannye, list):
            return [_razobrat_operatora_pd(zapis) for zapis in dannye if isinstance(zapis, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске оператора ПД")
        return []


async def poisk_ori(nazvanie: str = "", inn: str = "") -> list[dict[str, Any]]:
    """Поиск организатора распространения информации в реестре ОРИ.

    Аргументы:
        nazvanie: Название организации.
        inn: ИНН организации.

    Возвращает:
        Список организаторов ОРИ.
    """
    try:
        adres_url = f"{RKN_BAZA_API}/registry-ori/search"
        parametry: dict[str, Any] = {}
        if nazvanie:
            parametry["name"] = nazvanie
        if inn:
            parametry["inn"] = inn
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_ori(zapis) for zapis in elementy if isinstance(zapis, dict)]
        if isinstance(dannye, list):
            return [_razobrat_ori(zapis) for zapis in dannye if isinstance(zapis, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске ОРИ")
        return []


async def proverka_blokirovki(domen: str = "") -> dict[str, Any]:
    """Проверка наличия сайта в реестре запрещённых сайтов.

    Аргументы:
        domen: Доменное имя для проверки.

    Возвращает:
        Информация о блокировке.
    """
    if not domen:
        return {"blokirovka": False, "osnovanie": ""}
    try:
        adres_url = f"{EAIS_BAZA_API}/api/check"
        parametry = {"domain": domen}
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_blokirovku(dannye, domen)
        return {"domen": domen, "blokirovka": False, "istochnik": "ЕАИС (eais.rkn.gov.ru)"}
    except Exception:
        logger.exception("Ошибка при проверке блокировки %s", domen)
        return {
            "domen": domen,
            "blokirovka": False,
            "osnovanie": "Не удалось проверить",
            "istochnik": "ЕАИС (eais.rkn.gov.ru)",
        }


async def poisk_licenziy(nomer: str = "", inn: str = "") -> list[dict[str, Any]]:
    """Поиск лицензий связи в реестре Роскомнадзора.

    Аргументы:
        nomer: Номер лицензии.
        inn: ИНН лицензиата.

    Возвращает:
        Список лицензий.
    """
    try:
        adres_url = f"{RKN_BAZA_API}/licenses/search"
        parametry: dict[str, Any] = {}
        if nomer:
            parametry["number"] = nomer
        if inn:
            parametry["inn"] = inn
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [
                    _razobrat_litsenziyu(zapis) for zapis in elementy if isinstance(zapis, dict)
                ]
        if isinstance(dannye, list):
            return [_razobrat_litsenziyu(zapis) for zapis in dannye if isinstance(zapis, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске лицензий")
        return []


async def poisk_smi(registracionnyy_nomer: str = "", nazvanie: str = "") -> list[dict[str, Any]]:
    """Поиск СМИ в реестре Роскомнадзора.

    Аргументы:
        registracionnyy_nomer: Регистрационный номер СМИ.
        nazvanie: Название СМИ.

    Возвращает:
        Список СМИ.
    """
    try:
        adres_url = f"{RKN_BAZA_API}/mass-media/search"
        parametry: dict[str, Any] = {}
        if registracionnyy_nomer:
            parametry["regNumber"] = registracionnyy_nomer
        if nazvanie:
            parametry["name"] = nazvanie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_smi(s) for s in elementy if isinstance(s, dict)]
        if isinstance(dannye, list):
            return [_razobrat_smi(s) for s in dannye if isinstance(s, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске СМИ")
        return []


def _razobrat_operatora_pd(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи оператора ПД."""
    return {
        "naimenovanie": zapis.get("name", "") or zapis.get("naimenovanie", ""),
        "inn": zapis.get("inn", ""),
        "kategoriya": zapis.get("category", ""),
        "tsel_obrabotki": zapis.get("processingPurpose", "") or zapis.get("tsel", ""),
        "sostoyanie": zapis.get("status", ""),
        "data_registracii": zapis.get("registrationDate", ""),
        "adres": zapis.get("address", ""),
        "istochnik": "Реестр ПД (rkn.gov.ru/pdn)",
    }


def _razobrat_ori(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи ОРИ."""
    return {
        "naimenovanie": zapis.get("name", "") or zapis.get("naimenovanie", ""),
        "inn": zapis.get("inn", ""),
        "tip": zapis.get("type", "") or zapis.get("tip_ori", ""),
        "sostoyanie": zapis.get("status", ""),
        "data_vklyucheniya": zapis.get("inclusionDate", ""),
        "osnovanie": zapis.get("ground", ""),
        "istochnik": "Реестр ОРИ (rkn.gov.ru/registry-ori)",
    }


def _razobrat_blokirovku(zapis: dict[str, Any], domen: str) -> dict[str, Any]:
    """Парсинг результата проверки блокировки."""
    return {
        "domen": domen,
        "blokirovka": bool(zapis.get("blocked", zapis.get("isBlocked", False))),
        "osnovanie": zapis.get("reason", "") or zapis.get("ground", ""),
        "data_vklyucheniya": zapis.get("inclusionDate", ""),
        "organy": zapis.get("decisionOrgans", ""),
        "istochnik": "ЕАИС (eais.rkn.gov.ru)",
    }


def _razobrat_litsenziyu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи лицензии связи."""
    return {
        "nomer": zapis.get("number", "") or zapis.get("nomer", ""),
        "organizaciya": zapis.get("licensee", "") or zapis.get("organizaciya", ""),
        "tip_licenzii": zapis.get("type", "") or zapis.get("tip", ""),
        "data_vydachi": zapis.get("issueDate", ""),
        "data_okonchaniya": zapis.get("expiryDate", ""),
        "sostoyanie": zapis.get("status", ""),
        "territoriya": zapis.get("territory", ""),
        "istochnik": "Реестр лицензий (rkn.gov.ru)",
    }


def _razobrat_smi(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи СМИ."""
    return {
        "registracionnyy_nomer": zapis.get("regNumber", "") or zapis.get("nomer", ""),
        "nazvanie": zapis.get("name", "") or zapis.get("nazvanie", ""),
        "tip_smi": zapis.get("type", "") or zapis.get("tip", ""),
        "uchreditel": zapis.get("founder", ""),
        "yazyk": zapis.get("language", ""),
        "adres": zapis.get("address", ""),
        "sostoyanie": zapis.get("status", ""),
        "istochnik": "Реестр СМИ (rkn.gov.ru)",
    }
