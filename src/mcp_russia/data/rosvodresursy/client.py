"""HTTP-клиент для модуля Росводресурсов.

Интеграция с реальными API:
    - Государственный водный реестр: text.water.ru
    - ГМВО (гидромониторинг): gmvo.skniigkh.ru
    - Открытые данные data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    BASSEYNOVYE_OKRUGA,
    GMVO_API_BASE,
    KRUPNYE_VODOKHRANILISHCHA,
    TIPY_GIDRO_DANNYKH,
    TIPY_VODNYKH_OBIEKTOV,
    VODNYY_REESTR_BASE,
)

logger = logging.getLogger(__name__)


async def poisk_vodnykh_obektov(
    zapros: str = "",
    tip: str = "",
    basseyn: str = "",
    region: str = "",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Поиск водных объектов в Государственном водном реестре.

    Args:
        zapros: Поисковый запрос (название водного объекта).
        tip: Тип водного объекта (reka, ozero и т.д.).
        basseyn: Код бассейнового округа.
        region: Регион.
        limit: Максимум результатов.

    Returns:
        Список водных объектов.
    """
    try:
        url = f"{VODNYY_REESTR_BASE}/api/objects"
        params: dict[str, Any] = {}
        if zapros:
            params["query"] = zapros
        if tip:
            params["type"] = tip
        if basseyn:
            params["basin"] = basseyn
        if region:
            params["region"] = region
        params["limit"] = limit
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_vodnyy_obekt(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске водных объектов")
        return []


async def info_vodnogo_obekta(code: str) -> dict[str, Any] | None:
    """Получить информацию о водном объекте из Государственного водного реестра.

    Args:
        code: Код водного объекта.

    Returns:
        Данные о водном объекте или None.
    """
    try:
        url = f"{VODNYY_REESTR_BASE}/api/objects/{code}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_vodnyy_obekt(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении водного объекта %s", code)
        return None


async def poluchit_gidro_dannye(
    post_id: str = "",
    region: str = "",
    tip_dannykh: str = "uroven",
) -> list[dict[str, Any]]:
    """Получить гидрологические данные с мониторинговых постов ГМВО.

    Args:
        post_id: Идентификатор гидрологического поста.
        region: Регион.
        tip_dannykh: Тип данных (uroven, raskhod, temperatura, led, navodnenie).

    Returns:
        Список гидрологических данных.
    """
    try:
        url = f"{GMVO_API_BASE}/api/data"
        params: dict[str, Any] = {"type": tip_dannykh}
        if post_id:
            params["post"] = post_id
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_gidro_zapis(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении гидрологических данных")
        return []


async def poluchit_dannye_vodokhranilishcha(code: str) -> dict[str, Any] | None:
    """Получить актуальные данные о водохранилище.

    Args:
        code: Код водохранилища.

    Returns:
        Данные о водохранилище или None.
    """
    try:
        url = f"{GMVO_API_BASE}/api/reservoirs/{code}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_vodokhranilishche(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении данных водохранилища %s", code)
        return None


async def poluchit_vodopolzovanie(
    region: str = "",
    god: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о водопользовании из открытых данных.

    Args:
        region: Регион.
        god: Год.

    Returns:
        Список данных о водопользовании.
    """
    try:
        url = f"{VODNYY_REESTR_BASE}/api/water-use"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_vodopolzovanie_zapis(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении данных о водопользовании")
        return []


def get_basseynovye_okruga_list() -> list[dict[str, str]]:
    """Вернуть справочник бассейновых округов."""
    return BASSEYNOVYE_OKRUGA


def get_tipy_vodnykh_obektov_list() -> list[dict[str, str]]:
    """Вернуть справочник типов водных объектов."""
    return TIPY_VODNYKH_OBIEKTOV


def get_tipy_gidro_list() -> list[dict[str, str]]:
    """Вернуть справочник типов гидрологических данных."""
    return TIPY_GIDRO_DANNYKH


def get_vodokhranilishcha_list() -> list[dict[str, str]]:
    """Вернуть справочник водохранилищ (краткий)."""
    return [
        {"code": v["code"], "name": v["name"], "region": v["region"]}
        for v in KRUPNYE_VODOKHRANILISHCHA
    ]


def get_vodokhranilishcha_detailed() -> list[dict[str, Any]]:
    """Вернуть подробный справочник водохранилищ."""
    return KRUPNYE_VODOKHRANILISHCHA


def _extract_list(data: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _parse_vodnyy_obekt(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водного объекта."""
    return {
        "code": item.get("code", "") or item.get("id", ""),
        "name": item.get("name", "") or item.get("title", ""),
        "tip": item.get("type", "") or item.get("tip", ""),
        "basseyn": item.get("basin", "") or item.get("basseyn", ""),
        "dlinna_km": item.get("length") or item.get("dlinna_km"),
        "ploshchad_km2": item.get("area") or item.get("ploshchad_km2"),
        "region": item.get("region", ""),
        "opisaniye": item.get("description", "") or item.get("opisaniye", ""),
        "istochnik": "Государственный водный реестр (text.water.ru)",
    }


def _parse_gidro_zapis(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи гидрологических данных."""
    return {
        "post": item.get("post", "") or item.get("postName", ""),
        "post_id": item.get("postId", "") or item.get("post_id", ""),
        "vodnyy_obekt": item.get("waterObject", "") or item.get("vodnyy_obekt", ""),
        "data_izmereniya": item.get("date", "") or item.get("data_izmereniya", ""),
        "uroven": item.get("level") or item.get("uroven"),
        "raskhod": item.get("discharge") or item.get("raskhod"),
        "temperatura": item.get("temperature") or item.get("temperatura"),
        "ledovaya_obstanovka": item.get("iceCondition", "") or item.get("ledovaya_obstanovka", ""),
        "preduprezhdenie": item.get("warning", "") or item.get("preduprezhdenie", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _parse_vodokhranilishche(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водохранилища."""
    return {
        "code": item.get("code", "") or item.get("id", ""),
        "name": item.get("name", "") or item.get("title", ""),
        "region": item.get("region", ""),
        "obiem_km3": item.get("volume") or item.get("obiem_km3"),
        "ploshchad_km2": item.get("area") or item.get("ploshchad_km2"),
        "uroven_m": item.get("level") or item.get("uroven_m"),
        "priznak_napolneniya": item.get("fillStatus", "") or item.get("priznak_napolneniya", ""),
        "data_izmereniya": item.get("date", "") or item.get("data_izmereniya", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _parse_vodopolzovanie_zapis(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи о водопользовании."""
    return {
        "region": item.get("region", ""),
        "god": str(item.get("year", item.get("god", ""))),
        "zabrano_vody_km3": item.get("withdrawn") or item.get("zabrano_vody_km3"),
        "ispolzovano_vody_km3": item.get("used") or item.get("ispolzovano_vody_km3"),
        "sbrosheno_stokov_km3": item.get("discharged") or item.get("sbrosheno_stokov_km3"),
        "istochnik": item.get("source", "") or item.get("istochnik", ""),
        "naznachenie": item.get("purpose", "") or item.get("naznachenie", ""),
    }
