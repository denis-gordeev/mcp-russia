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

from .constants import PROVERKI_API_BAZA, ZPP_API_BAZA

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
        subiekt: Код региона.

    Возвращает:
        Список проверок.
    """
    try:
        adres_url = f"{PROVERKI_API_BAZA}/api/procedure"
        parametry: dict[str, Any] = {}
        if inn_tseli:
            parametry["targetInn"] = inn_tseli
        if nazvanie_tseli:
            parametry["targetName"] = nazvanie_tseli
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [
                    _razobrat_proverku(zapis)
                    for zapis in elementy
                    if isinstance(zapis, dict)
                ]
        if isinstance(dannye, list):
            return [_razobrat_proverku(zapis) for zapis in dannye if isinstance(zapis, dict)]
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
        adres_url = f"{PROVERKI_API_BAZA}/api/procedure/{nomer}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_proverku(dannye)
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
        subiekt: Код региона.
        organ: Код контролирующего органа.

    Возвращает:
        Список запланированных проверок.
    """
    try:
        adres_url = f"{PROVERKI_API_BAZA}/api/plan"
        parametry: dict[str, Any] = {"organ": organ}
        if god:
            parametry["year"] = god
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [
                    _razobrat_proverku(zapis)
                    for zapis in elementy
                    if isinstance(zapis, dict)
                ]
        if isinstance(dannye, list):
            return [_razobrat_proverku(zapis) for zapis in dannye if isinstance(zapis, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при получении плана проверок")
        return []


async def poisk_zhalob(
    organizatsiya: str = "",
    inn: str = "",
) -> list[dict[str, Any]]:
    """Поиск жалоб потребителей через zpp.rospotrebnadzor.ru.

    Аргументы:
        organizatsiya: Название организации.
        inn: ИНН организации.

    Возвращает:
        Список жалоб.
    """
    try:
        adres_url = f"{ZPP_API_BAZA}/api/complaints"
        parametry: dict[str, Any] = {}
        if organizatsiya:
            parametry["organizationName"] = organizatsiya
        if inn:
            parametry["inn"] = inn
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", dannye.get("items", []))
            if isinstance(elementy, list):
                return [_razobrat_zhalobu(zapis) for zapis in elementy if isinstance(zapis, dict)]
        if isinstance(dannye, list):
            return [_razobrat_zhalobu(zapis) for zapis in dannye if isinstance(zapis, dict)]
        return []
    except Exception:
        logger.exception("Ошибка при поиске жалоб потребителей")
        return []


def _razobrat_proverku(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о проверке из реестра."""
    return {
        "nomer": zapis.get("id", "") or zapis.get("number", ""),
        "tip_proverki": zapis.get("type", "") or zapis.get("kind", ""),
        "organ": zapis.get("controlOrgan", "") or zapis.get("organ", ""),
        "obekt": zapis.get("targetName", "") or zapis.get("target", ""),
        "inn": zapis.get("targetInn", ""),
        "data_nachala": zapis.get("startDate", "") or zapis.get("dateStart", ""),
        "data_okonchaniya": zapis.get("endDate", "") or zapis.get("dateEnd", ""),
        "sostoyanie": zapis.get("status", ""),
        "vyavleno_narusheniy": zapis.get("violationsCount", 0),
        "rezultat": zapis.get("result", ""),
        "istochnik": "Реестр проверок (proverki.rospotrebnadzor.ru)",
    }


def _razobrat_zhalobu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Парсинг записи о жалобе потребителя."""
    return {
        "tema": zapis.get("subject", "") or zapis.get("topic", ""),
        "data_podachi": zapis.get("date", "") or zapis.get("created", ""),
        "sostoyanie_rassmotreniya": zapis.get("status", ""),
        "rezultat": zapis.get("result", ""),
        "organizatsiya": zapis.get("organizationName", ""),
        "inn": zapis.get("inn", ""),
        "istochnik": "ЗПП (zpp.rospotrebnadzor.ru)",
    }
