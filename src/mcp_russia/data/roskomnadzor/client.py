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
    EAIS_API_BASE,
    RKN_API_BASE,
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
        adres_url = f"{RKN_API_BASE}/pdn/search"
        parametry: dict[str, Any] = {}
        if inn:
            parametry["inn"] = inn
        if nazvanie:
            parametry["name"] = nazvanie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_operatora_pd(o) for o in elementy if isinstance(o, dict)]
        if isinstance(dannye, list):
            return [_razobrat_operatora_pd(o) for o in dannye if isinstance(o, dict)]
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
        adres_url = f"{RKN_API_BASE}/registry-ori/search"
        parametry: dict[str, Any] = {}
        if nazvanie:
            parametry["name"] = nazvanie
        if inn:
            parametry["inn"] = inn
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_ori(o) for o in elementy if isinstance(o, dict)]
        if isinstance(dannye, list):
            return [_razobrat_ori(o) for o in dannye if isinstance(o, dict)]
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
        adres_url = f"{EAIS_API_BASE}/api/check"
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
        adres_url = f"{RKN_API_BASE}/licenses/search"
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
                    _razobrat_litsenziyu(element)
                    for element in elementy
                    if isinstance(element, dict)
                ]
        if isinstance(dannye, list):
            return [
                _razobrat_litsenziyu(element) for element in dannye if isinstance(element, dict)
            ]
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
        adres_url = f"{RKN_API_BASE}/mass-media/search"
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


def _razobrat_operatora_pd(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи оператора ПД."""
    return {
        "naimenovanie": element.get("name", "") or element.get("naimenovanie", ""),
        "inn": element.get("inn", ""),
        "kategoriya": element.get("category", ""),
        "tsel_obrabotki": element.get("processingPurpose", "") or element.get("tsel", ""),
        "sostoyanie": element.get("status", ""),
        "data_registracii": element.get("registrationDate", ""),
        "adres": element.get("address", ""),
        "istochnik": "Реестр ПД (rkn.gov.ru/pdn)",
    }


def _razobrat_ori(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи ОРИ."""
    return {
        "naimenovanie": element.get("name", "") or element.get("naimenovanie", ""),
        "inn": element.get("inn", ""),
        "tip": element.get("type", "") or element.get("tip_ori", ""),
        "sostoyanie": element.get("status", ""),
        "data_vklyucheniya": element.get("inclusionDate", ""),
        "osnovanie": element.get("ground", ""),
        "istochnik": "Реестр ОРИ (rkn.gov.ru/registry-ori)",
    }


def _razobrat_blokirovku(element: dict[str, Any], domen: str) -> dict[str, Any]:
    """Парсинг результата проверки блокировки."""
    return {
        "domen": domen,
        "blokirovka": bool(element.get("blocked", element.get("isBlocked", False))),
        "osnovanie": element.get("reason", "") or element.get("ground", ""),
        "data_vklyucheniya": element.get("inclusionDate", ""),
        "organy": element.get("decisionOrgans", ""),
        "istochnik": "ЕАИС (eais.rkn.gov.ru)",
    }


def _razobrat_litsenziyu(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи лицензии связи."""
    return {
        "nomer": element.get("number", "") or element.get("nomer", ""),
        "organizaciya": element.get("licensee", "") or element.get("organizaciya", ""),
        "tip_licenzii": element.get("type", "") or element.get("tip", ""),
        "data_vydachi": element.get("issueDate", ""),
        "data_okonchaniya": element.get("expiryDate", ""),
        "sostoyanie": element.get("status", ""),
        "territoriya": element.get("territory", ""),
        "istochnik": "Реестр лицензий (rkn.gov.ru)",
    }


def _razobrat_smi(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи СМИ."""
    return {
        "registracionnyy_nomer": element.get("regNumber", "") or element.get("nomer", ""),
        "nazvanie": element.get("name", "") or element.get("nazvanie", ""),
        "tip_smi": element.get("type", "") or element.get("tip", ""),
        "uchreditel": element.get("founder", ""),
        "yazyk": element.get("language", ""),
        "adres": element.get("address", ""),
        "sostoyanie": element.get("status", ""),
        "istochnik": "Реестр СМИ (rkn.gov.ru)",
    }
