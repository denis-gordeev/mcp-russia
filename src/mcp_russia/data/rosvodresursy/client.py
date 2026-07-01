"""HTTP-клиент для модуля Росводресурсов.

Интеграция с реальными API:
    - Государственный водный реестр: text.water.ru
    - ГМВО (гидромониторинг): gmvo.skniigkh.ru
    - Открытые данные data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

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
    subiekt: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск водных объектов в Государственном водном реестре.

    Аргументы:
        zapros: Поисковый запрос (название водного объекта).
        tip: Тип водного объекта (reka, ozero и т.д.).
        basseyn: Код бассейнового округа.
        subiekt: Регион.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список водных объектов.
    """
    try:
        adres_url = f"{VODNYY_REESTR_BASE}/api/objects"
        parametry: dict[str, Any] = {}
        if zapros:
            parametry["query"] = zapros
        if tip:
            parametry["type"] = tip
        if basseyn:
            parametry["basin"] = basseyn
        if subiekt:
            parametry["region"] = subiekt
        parametry["limit"] = ogranichenie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_vodnyy_obekt(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{VODNYY_REESTR_BASE}/api/objects/{kod}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_vodnyy_obekt(dannye)
        return None
    except Exception:
        logger.exception("Ошибка при получении водного объекта %s", kod)
        return None


async def poluchit_gidro_dannye(
    identifikator_posta: str = "",
    subiekt: str = "",
    tip_dannykh: str = "uroven",
) -> list[dict[str, Any]]:
    """Получить гидрологические данные с мониторинговых постов ГМВО.

    Аргументы:
        identifikator_posta: Идентификатор гидрологического поста.
        subiekt: Регион.
        tip_dannykh: Тип данных (uroven, raskhod, temperatura, led, navodnenie).

    Возвращает:
        Список гидрологических данных.
    """
    try:
        adres_url = f"{GMVO_API_BASE}/api/data"
        parametry: dict[str, Any] = {"type": tip_dannykh}
        if identifikator_posta:
            parametry["post"] = identifikator_posta
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_gidro_zapis(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{GMVO_API_BASE}/api/reservoirs/{kod}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_vodokhranilishche(dannye)
        return None
    except Exception:
        logger.exception("Ошибка при получении данных водохранилища %s", kod)
        return None


async def poluchit_vodopolzovanie(
    subiekt: str = "",
    god: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о водопользовании из открытых данных.

    Аргументы:
        subiekt: Регион.
        god: Год.

    Возвращает:
        Список данных о водопользовании.
    """
    try:
        adres_url = f"{VODNYY_REESTR_BASE}/api/water-use"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_vodopolzovanie_zapis(p) for p in elementy if isinstance(p, dict)]
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
        {"kod": v["kod"], "nazvanie": v["nazvanie"], "subiekt": v["subiekt"]}
        for v in KRUPNYE_VODOKHRANILISHCHA
    ]


def poluchit_vodokhranilishche_podrobno() -> list[dict[str, Any]]:
    """Вернуть подробный справочник водохранилищ."""
    return KRUPNYE_VODOKHRANILISHCHA


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for key in ("data", "items", "results", "records"):
            val = dannye.get(key)
            if isinstance(val, list):
                return val
    return []


def _razobrat_vodnyy_obekt(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водного объекта."""
    return {
        "kod": element.get("code", "") or element.get("id", ""),
        "nazvanie": element.get("name", "") or element.get("title", ""),
        "tip": element.get("type", "") or element.get("tip", ""),
        "basseyn": element.get("basin", "") or element.get("basseyn", ""),
        "dlinna_km": element.get("length") or element.get("dlinna_km"),
        "ploshchad_km2": element.get("area") or element.get("ploshchad_km2"),
        "subiekt": element.get("region", ""),
        "opisaniye": element.get("description", "") or element.get("opisaniye", ""),
        "istochnik": "Государственный водный реестр (text.water.ru)",
    }


def _razobrat_gidro_zapis(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи гидрологических данных."""
    return {
        "post": element.get("post", "") or element.get("postName", ""),
        "post_id": element.get("postId", "") or element.get("post_id", ""),
        "vodnyy_obekt": element.get("waterObject", "") or element.get("vodnyy_obekt", ""),
        "data_izmereniya": element.get("date", "") or element.get("data_izmereniya", ""),
        "uroven": element.get("level") or element.get("uroven"),
        "raskhod": element.get("discharge") or element.get("raskhod"),
        "temperatura": element.get("temperature") or element.get("temperatura"),
        "ledovaya_obstanovka": element.get("iceCondition", "")
        or element.get("ledovaya_obstanovka", ""),
        "preduprezhdenie": element.get("warning", "") or element.get("preduprezhdenie", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _razobrat_vodokhranilishche(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водохранилища."""
    return {
        "kod": element.get("code", "") or element.get("id", ""),
        "nazvanie": element.get("name", "") or element.get("title", ""),
        "subiekt": element.get("region", ""),
        "obiem_km3": element.get("volume") or element.get("obiem_km3"),
        "ploshchad_km2": element.get("area") or element.get("ploshchad_km2"),
        "uroven_m": element.get("level") or element.get("uroven_m"),
        "priznak_napolneniya": element.get("fillStatus", "")
        or element.get("priznak_napolneniya", ""),
        "data_izmereniya": element.get("date", "") or element.get("data_izmereniya", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _razobrat_vodopolzovanie_zapis(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи о водопользовании."""
    return {
        "subiekt": element.get("region", ""),
        "god": str(element.get("year", element.get("god", ""))),
        "zabrano_vody_km3": element.get("withdrawn") or element.get("zabrano_vody_km3"),
        "ispolzovano_vody_km3": element.get("used") or element.get("ispolzovano_vody_km3"),
        "sbrosheno_stokov_km3": element.get("discharged") or element.get("sbrosheno_stokov_km3"),
        "istochnik": element.get("source", "") or element.get("istochnik", ""),
        "naznachenie": element.get("purpose", "") or element.get("naznachenie", ""),
    }
