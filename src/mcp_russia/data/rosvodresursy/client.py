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
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск водных объектов в Государственном водном реестре.

    Аргументы:
        zapros: Поисковый запрос (название водного объекта).
        tip: Тип водного объекта (reka, ozero и т.д.).
        basseyn: Код бассейнового округа.
        region: Регион.
        ogranichenie: Максимум результатов.

    Возвращает:
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
        params["limit"] = ogranichenie
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        return [_razobrat_vodnyy_obekt(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске водных объектов")
        return []


async def info_vodnogo_obekta(kod: str) -> dict[str, Any] | None:
    """Получить информацию о водном объекте из Государственного водного реестра.

    Аргументы:
        kod: Код водного объекта.

    Возвращает:
        Данные о водном объекте или None.
    """
    try:
        url = f"{VODNYY_REESTR_BASE}/api/objects/{kod}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _razobrat_vodnyy_obekt(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении водного объекта %s", kod)
        return None


async def poluchit_gidro_dannye(
    identifikator_posta: str = "",
    region: str = "",
    tip_dannykh: str = "uroven",
) -> list[dict[str, Any]]:
    """Получить гидрологические данные с мониторинговых постов ГМВО.

    Аргументы:
        identifikator_posta: Идентификатор гидрологического поста.
        region: Регион.
        tip_dannykh: Тип данных (uroven, raskhod, temperatura, led, navodnenie).

    Возвращает:
        Список гидрологических данных.
    """
    try:
        url = f"{GMVO_API_BASE}/api/data"
        params: dict[str, Any] = {"type": tip_dannykh}
        if identifikator_posta:
            params["post"] = identifikator_posta
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        return [_razobrat_gidro_zapis(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении гидрологических данных")
        return []


async def poluchit_dannye_vodokhranilishcha(kod: str) -> dict[str, Any] | None:
    """Получить актуальные данные о водохранилище.

    Аргументы:
        kod: Код водохранилища.

    Возвращает:
        Данные о водохранилище или None.
    """
    try:
        url = f"{GMVO_API_BASE}/api/reservoirs/{kod}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _razobrat_vodokhranilishche(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении данных водохранилища %s", kod)
        return None


async def poluchit_vodopolzovanie(
    region: str = "",
    god: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о водопользовании из открытых данных.

    Аргументы:
        region: Регион.
        god: Год.

    Возвращает:
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
        items = _izvlech_spisok(data)
        return [_razobrat_vodopolzovanie_zapis(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении данных о водопользовании")
        return []


def poluchit_spisok_basseynovykh_okrugov() -> list[dict[str, str]]:
    """Вернуть справочник бассейновых округов."""
    return BASSEYNOVYE_OKRUGA


def poluchit_spisok_tipov_vodnykh_obektov() -> list[dict[str, str]]:
    """Вернуть справочник типов водных объектов."""
    return TIPY_VODNYKH_OBIEKTOV


def poluchit_spisok_tipov_gidro() -> list[dict[str, str]]:
    """Вернуть справочник типов гидрологических данных."""
    return TIPY_GIDRO_DANNYKH


def poluchit_spisok_vodokhranilishch() -> list[dict[str, str]]:
    """Вернуть справочник водохранилищ (краткий)."""
    return [
        {"kod": v["kod"], "nazvanie": v["nazvanie"], "region": v["region"]}
        for v in KRUPNYE_VODOKHRANILISHCHA
    ]


def poluchit_vodokhranilishche_podrobno() -> list[dict[str, Any]]:
    """Вернуть подробный справочник водохранилищ."""
    return KRUPNYE_VODOKHRANILISHCHA


def _izvlech_spisok(data: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_vodnyy_obekt(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водного объекта."""
    return {
        "kod": item.get("code", "") or item.get("id", ""),
        "nazvanie": item.get("name", "") or item.get("title", ""),
        "tip": item.get("type", "") or item.get("tip", ""),
        "basseyn": item.get("basin", "") or item.get("basseyn", ""),
        "dlinna_km": item.get("length") or item.get("dlinna_km"),
        "ploshchad_km2": item.get("area") or item.get("ploshchad_km2"),
        "region": item.get("region", ""),
        "opisaniye": item.get("description", "") or item.get("opisaniye", ""),
        "istochnik": "Государственный водный реестр (text.water.ru)",
    }


def _razobrat_gidro_zapis(item: dict[str, Any]) -> dict[str, Any]:
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


def _razobrat_vodokhranilishche(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водохранилища."""
    return {
        "kod": item.get("code", "") or item.get("id", ""),
        "nazvanie": item.get("name", "") or item.get("title", ""),
        "region": item.get("region", ""),
        "obiem_km3": item.get("volume") or item.get("obiem_km3"),
        "ploshchad_km2": item.get("area") or item.get("ploshchad_km2"),
        "uroven_m": item.get("level") or item.get("uroven_m"),
        "priznak_napolneniya": item.get("fillStatus", "") or item.get("priznak_napolneniya", ""),
        "data_izmereniya": item.get("date", "") or item.get("data_izmereniya", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _razobrat_vodopolzovanie_zapis(item: dict[str, Any]) -> dict[str, Any]:
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
