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
    GMVO_BAZA_API,
    KRUPNYE_VODOKHRANILISHCHA,
    TIPY_GIDRO_DANNYKH,
    TIPY_VODNYKH_OBIEKTOV,
    VODNYY_REESTR_BAZA,
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
        adres_url = f"{VODNYY_REESTR_BAZA}/api/objects"
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
        return [
            _razobrat_vodnyy_obekt(element) for element in elementy if isinstance(element, dict)
        ]
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
        adres_url = f"{VODNYY_REESTR_BAZA}/api/objects/{kod}"
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
        adres_url = f"{GMVO_BAZA_API}/api/data"
        parametry: dict[str, Any] = {"type": tip_dannykh}
        if identifikator_posta:
            parametry["post"] = identifikator_posta
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [
            _razobrat_gidro_zapis(element) for element in elementy if isinstance(element, dict)
        ]
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
        adres_url = f"{GMVO_BAZA_API}/api/reservoirs/{kod}"
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
        adres_url = f"{VODNYY_REESTR_BAZA}/api/water-use"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [
            _razobrat_vodopolzovanie_zapis(element)
            for element in elementy
            if isinstance(element, dict)
        ]
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
        {
            "kod": vodokhranilishche["kod"],
            "nazvanie": vodokhranilishche["nazvanie"],
            "subiekt": vodokhranilishche["subiekt"],
        }
        for vodokhranilishche in KRUPNYE_VODOKHRANILISHCHA
    ]


def poluchit_vodokhranilishche_podrobno() -> list[dict[str, Any]]:
    """Вернуть подробный справочник водохранилищ."""
    return KRUPNYE_VODOKHRANILISHCHA


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API (поддержка разных форматов)."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for klyuch in ("data", "items", "results", "records"):
            znachenie_spiska = dannye.get(klyuch)
            if isinstance(znachenie_spiska, list):
                return znachenie_spiska
    return []


def _razobrat_vodnyy_obekt(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водного объекта."""
    return {
        "kod": zapis.get("code", "") or zapis.get("id", ""),
        "nazvanie": zapis.get("name", "") or zapis.get("title", ""),
        "tip": zapis.get("type", "") or zapis.get("tip", ""),
        "basseyn": zapis.get("basin", "") or zapis.get("basseyn", ""),
        "dlinna_km": zapis.get("length") or zapis.get("dlinna_km"),
        "ploshchad_km2": zapis.get("area") or zapis.get("ploshchad_km2"),
        "subiekt": zapis.get("region", ""),
        "opisaniye": zapis.get("description", "") or zapis.get("opisaniye", ""),
        "istochnik": "Государственный водный реестр (text.water.ru)",
    }


def _razobrat_gidro_zapis(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи гидрологических данных."""
    return {
        "post": zapis.get("post", "") or zapis.get("postName", ""),
        "post_id": zapis.get("postId", "") or zapis.get("post_id", ""),
        "vodnyy_obekt": zapis.get("waterObject", "") or zapis.get("vodnyy_obekt", ""),
        "data_izmereniya": zapis.get("date", "") or zapis.get("data_izmereniya", ""),
        "uroven": zapis.get("level") or zapis.get("uroven"),
        "raskhod": zapis.get("discharge") or zapis.get("raskhod"),
        "temperatura": zapis.get("temperature") or zapis.get("temperatura"),
        "ledovaya_obstanovka": zapis.get("iceCondition", "")
        or zapis.get("ledovaya_obstanovka", ""),
        "preduprezhdenie": zapis.get("warning", "") or zapis.get("preduprezhdenie", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _razobrat_vodokhranilishche(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных водохранилища."""
    return {
        "kod": zapis.get("code", "") or zapis.get("id", ""),
        "nazvanie": zapis.get("name", "") or zapis.get("title", ""),
        "subiekt": zapis.get("region", ""),
        "obiem_km3": zapis.get("volume") or zapis.get("obiem_km3"),
        "ploshchad_km2": zapis.get("area") or zapis.get("ploshchad_km2"),
        "uroven_m": zapis.get("level") or zapis.get("uroven_m"),
        "priznak_napolneniya": zapis.get("fillStatus", "") or zapis.get("priznak_napolneniya", ""),
        "data_izmereniya": zapis.get("date", "") or zapis.get("data_izmereniya", ""),
        "istochnik": "ГМВО (gmvo.skniigkh.ru)",
    }


def _razobrat_vodopolzovanie_zapis(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор записи о водопользовании."""
    return {
        "subiekt": zapis.get("region", ""),
        "god": str(zapis.get("year", zapis.get("god", ""))),
        "zabrano_vody_km3": zapis.get("withdrawn") or zapis.get("zabrano_vody_km3"),
        "ispolzovano_vody_km3": zapis.get("used") or zapis.get("ispolzovano_vody_km3"),
        "sbrosheno_stokov_km3": zapis.get("discharged") or zapis.get("sbrosheno_stokov_km3"),
        "istochnik": zapis.get("source", "") or zapis.get("istochnik", ""),
        "naznachenie": zapis.get("purpose", "") or zapis.get("naznachenie", ""),
    }
