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

from mcp_russia._shared.http_client import http_get

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
        url = f"{RKN_API_BASE}/pdn/search"
        params: dict[str, Any] = {}
        if inn:
            params["inn"] = inn
        if nazvanie:
            params["name"] = nazvanie
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_parse_operator_pd(o) for o in items if isinstance(o, dict)]
        if isinstance(data, list):
            return [_parse_operator_pd(o) for o in data if isinstance(o, dict)]
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
        url = f"{RKN_API_BASE}/registry-ori/search"
        params: dict[str, Any] = {}
        if nazvanie:
            params["name"] = nazvanie
        if inn:
            params["inn"] = inn
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_parse_ori(o) for o in items if isinstance(o, dict)]
        if isinstance(data, list):
            return [_parse_ori(o) for o in data if isinstance(o, dict)]
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
        url = f"{EAIS_API_BASE}/api/check"
        params = {"domain": domen}
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            return _parse_blokirovka(data, domen)
        return {"domain": domen, "blokirovka": False, "istochnik": "ЕАИС (eais.rkn.gov.ru)"}
    except Exception:
        logger.exception("Ошибка при проверке блокировки %s", domen)
        return {
            "domain": domen,
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
        url = f"{RKN_API_BASE}/licenses/search"
        params: dict[str, Any] = {}
        if nomer:
            params["number"] = nomer
        if inn:
            params["inn"] = inn
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_parse_licenziya(item) for item in items if isinstance(item, dict)]
        if isinstance(data, list):
            return [_parse_licenziya(item) for item in data if isinstance(item, dict)]
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
        url = f"{RKN_API_BASE}/mass-media/search"
        params: dict[str, Any] = {}
        if registracionnyy_nomer:
            params["regNumber"] = registracionnyy_nomer
        if nazvanie:
            params["name"] = nazvanie
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_parse_smi(s) for s in items if isinstance(s, dict)]
        if isinstance(data, list):
            return [_parse_smi(s) for s in data if isinstance(s, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске СМИ")
        return []


def _parse_operator_pd(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи оператора ПД."""
    return {
        "naimenovanie": item.get("name", "") or item.get("naimenovanie", ""),
        "inn": item.get("inn", ""),
        "kategoriya": item.get("category", ""),
        "tsel_obrabotki": item.get("processingPurpose", "") or item.get("tsel", ""),
        "status": item.get("status", ""),
        "data_registracii": item.get("registrationDate", ""),
        "adres": item.get("address", ""),
        "istochnik": "Реестр ПД (rkn.gov.ru/pdn)",
    }


def _parse_ori(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи ОРИ."""
    return {
        "naimenovanie": item.get("name", "") or item.get("naimenovanie", ""),
        "inn": item.get("inn", ""),
        "tip": item.get("type", "") or item.get("tip_ori", ""),
        "status": item.get("status", ""),
        "data_vklyucheniya": item.get("inclusionDate", ""),
        "osnovanie": item.get("ground", ""),
        "istochnik": "Реестр ОРИ (rkn.gov.ru/registry-ori)",
    }


def _parse_blokirovka(item: dict[str, Any], domain: str) -> dict[str, Any]:
    """Парсинг результата проверки блокировки."""
    return {
        "domain": domain,
        "blokirovka": bool(item.get("blocked", item.get("isBlocked", False))),
        "osnovanie": item.get("reason", "") or item.get("ground", ""),
        "data_vklyucheniya": item.get("inclusionDate", ""),
        "organy": item.get("decisionOrgans", ""),
        "istochnik": "ЕАИС (eais.rkn.gov.ru)",
    }


def _parse_licenziya(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи лицензии связи."""
    return {
        "nomer": item.get("number", "") or item.get("nomer", ""),
        "organizaciya": item.get("licensee", "") or item.get("organizaciya", ""),
        "tip_licenzii": item.get("type", "") or item.get("tip", ""),
        "data_vydachi": item.get("issueDate", ""),
        "data_okonchaniya": item.get("expiryDate", ""),
        "status": item.get("status", ""),
        "territoriya": item.get("territory", ""),
        "istochnik": "Реестр лицензий (rkn.gov.ru)",
    }


def _parse_smi(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи СМИ."""
    return {
        "registracionnyy_nomer": item.get("regNumber", "") or item.get("nomer", ""),
        "nazvanie": item.get("name", "") or item.get("nazvanie", ""),
        "tip_smi": item.get("type", "") or item.get("tip", ""),
        "uchreditel": item.get("founder", ""),
        "yazyk": item.get("language", ""),
        "adres": item.get("address", ""),
        "status": item.get("status", ""),
        "istochnik": "Реестр СМИ (rkn.gov.ru)",
    }
