"""HTTP-клиент для модуля Роспотребнадзора.

Интеграция с реальными API:
    - Реестр проверок: proverki.rospotrebnadzor.ru
    - Открытые данные: rospotrebnadzor.ru/opendata
    - Защита прав потребителей: zpp.rospotrebnadzor.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import PROVERKI_API_BASE, ZPP_API_BASE

logger = logging.getLogger(__name__)


async def poisk_proverok(
    inn_tseli: str = "",
    nazvanie_tseli: str = "",
    subiekt: str = "",
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
        if subiekt:
            params["region"] = subiekt
        data = await http_poluchit(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            elementy = data.get("data", data.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
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
        data = await http_poluchit(url, timeout=15.0)
        if isinstance(data, dict):
            return _razobrat_proverku(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении проверки №%s", nomer)
        return None


async def plan_proverok(
    god: int = 0,
    subiekt: str = "",
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
        if subiekt:
            params["region"] = subiekt
        data = await http_poluchit(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            elementy = data.get("data", data.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_proverku(p) for p in elementy if isinstance(p, dict)]
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
        data = await http_poluchit(url, params=params, timeout=15.0)
        if isinstance(data, dict):
            elementy = data.get("data", data.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_zhalobu(z) for z in elementy if isinstance(z, dict)]
        if isinstance(data, list):
            return [_razobrat_zhalobu(z) for z in data if isinstance(z, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске жалоб потребителей")
        return []


def _razobrat_proverku(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о проверке из реестра."""
    return {
        "nomer": element.get("id", "") or element.get("number", ""),
        "tip_proverki": element.get("type", "") or element.get("kind", ""),
        "organ": element.get("controlOrgan", "") or element.get("organ", ""),
        "obekt": element.get("targetName", "") or element.get("target", ""),
        "inn": element.get("targetInn", ""),
        "data_nachala": element.get("startDate", "") or element.get("dateStart", ""),
        "data_okonchaniya": element.get("endDate", "") or element.get("dateEnd", ""),
        "sostoyanie": element.get("status", ""),
        "vyavleno_narusheniy": element.get("violationsCount", 0),
        "rezultat": element.get("result", ""),
        "istochnik": "Реестр проверок (proverki.rospotrebnadzor.ru)",
    }


def _razobrat_zhalobu(element: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о жалобе потребителя."""
    return {
        "tema": element.get("subject", "") or element.get("topic", ""),
        "data_podachi": element.get("date", "") or element.get("created", ""),
        "status_rassmotreniya": element.get("status", ""),
        "rezultat": element.get("result", ""),
        "organizaciya": element.get("organizationName", ""),
        "inn": element.get("inn", ""),
        "istochnik": "ЗПП (zpp.rospotrebnadzor.ru)",
    }
