"""HTTP-клиент для модуля Роспотребнадзора.

Интеграция с реальными API:
    - Реестр проверок: proverki.rospotrebnadzor.ru
    - Открытые данные: rospotrebnadzor.ru/opendata
    - Защита прав потребителей: zpp.rospotrebnadzor.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import PROVERKI_API_BASE, ZPP_API_BASE

logger = logging.getLogger(__name__)


async def poisk_proverok(
    inn_tseli: str = "",
    nazvanie_tseli: str = "",
    region: str = "",
) -> list[dict[str, Any]]:
    """Поиск проверок в реестре proverki.rospotrebnadzor.ru.

    Аргументы:
        inn_tseli: ИНН проверяемого лица.
        nazvanie_tseli: Название проверяемого лица.
        region: Код региона.

    Возвращает:
        Список проверок.
    """
    try:
        url = f"{PROVERKI_API_BASE}/api/procedure"
        params: dict[str, Any] = {}
        if inn_tseli:
            params["targetInn"] = inn_tseli
        if nazvanie_tseli:
            params["targetName"] = nazvanie_tseli
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
        if isinstance(data, list):
            return [_razobrat_proverku(p) for p in data if isinstance(p, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске проверок")
        return []


async def info_proverki(nomer: str) -> dict[str, Any] | None:
    """Получить информацию о проверке по номеру.

    Аргументы:
        nomer: Номер проверки.

    Возвращает:
        Данные о проверке или None.
    """
    try:
        url = f"{PROVERKI_API_BASE}/api/procedure/{nomer}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _razobrat_proverku(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении проверки №%s", nomer)
        return None


async def plan_proverok(
    god: int = 0,
    region: str = "",
    organ: str = "rospotrebnadzor",
) -> list[dict[str, Any]]:
    """Получить план проверок Роспотребнадзора.

    Аргументы:
        god: Год плана проверок.
        region: Код региона.
        organ: Код контролирующего органа.

    Возвращает:
        Список запланированных проверок.
    """
    try:
        url = f"{PROVERKI_API_BASE}/api/plan"
        params: dict[str, Any] = {"organ": organ}
        if god:
            params["year"] = god
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_razobrat_proverku(p) for p in items if isinstance(p, dict)]
        if isinstance(data, list):
            return [_razobrat_proverku(p) for p in data if isinstance(p, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при получении плана проверок")
        return []


async def poisk_zhalob(
    organizaciya: str = "",
    inn: str = "",
) -> list[dict[str, Any]]:
    """Поиск жалоб потребителей через zpp.rospotrebnadzor.ru.

    Аргументы:
        organizaciya: Название организации.
        inn: ИНН организации.

    Возвращает:
        Список жалоб.
    """
    try:
        url = f"{ZPP_API_BASE}/api/complaints"
        params: dict[str, Any] = {}
        if organizaciya:
            params["organizationName"] = organizaciya
        if inn:
            params["inn"] = inn
        data = await http_get(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            items = data.get("data", data.get("items", []))
            if isinstance(items, list):
                return [_razobrat_zhalobu(z) for z in items if isinstance(z, dict)]
        if isinstance(data, list):
            return [_razobrat_zhalobu(z) for z in data if isinstance(z, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске жалоб потребителей")
        return []


def _razobrat_proverku(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о проверке из реестра."""
    return {
        "nomer": item.get("id", "") or item.get("number", ""),
        "tip_proverki": item.get("type", "") or item.get("kind", ""),
        "organ": item.get("controlOrgan", "") or item.get("organ", ""),
        "obekt": item.get("targetName", "") or item.get("target", ""),
        "inn": item.get("targetInn", ""),
        "data_nachala": item.get("startDate", "") or item.get("dateStart", ""),
        "data_okonchaniya": item.get("endDate", "") or item.get("dateEnd", ""),
        "status": item.get("status", ""),
        "vyavleno_narusheniy": item.get("violationsCount", 0),
        "rezultat": item.get("result", ""),
        "istochnik": "Реестр проверок (proverki.rospotrebnadzor.ru)",
    }


def _razobrat_zhalobu(item: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о жалобе потребителя."""
    return {
        "tema": item.get("subject", "") or item.get("topic", ""),
        "data_podachi": item.get("date", "") or item.get("created", ""),
        "status_rassmotreniya": item.get("status", ""),
        "rezultat": item.get("result", ""),
        "organizaciya": item.get("organizationName", ""),
        "inn": item.get("inn", ""),
        "istochnik": "ЗПП (zpp.rospotrebnadzor.ru)",
    }
