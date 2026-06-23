"""HTTP-клиент для модуля МЧС России.

Интеграция с реальными API:
    - МЧС России: mchs.gov.ru
    - Открытые данные МЧС: data.mchs.gov.ru
    - Статистика пожаров: fires.ru
    - Портал открытых данных: data.gov.ru
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    FEDERALNYE_OKRUGA_MCHS,
    FIRES_STAT_BASE,
    KLASSY_CHS,
    MCHS_API_BASE,
    MCHS_OPENDATA_BASE,
    STATISTIKA_POZHAROV_2023,
    TIPY_OPASNOSTI,
    VIDY_CHS,
    VIDY_POZHAROV,
)

logger = logging.getLogger(__name__)


async def statistika_pojarov(
    region: str = "",
    god: int = 0,
    vid_pozhara: str = "",
) -> list[dict[str, Any]]:
    """Получить статистику пожаров.

    Аргументы:
        region: Субъект РФ или федеральный округ.
        god: Год статистики.
        vid_pozhara: Вид пожара.

    Возвращает:
        Список данных о пожарах.
    """
    try:
        url = f"{FIRES_STAT_BASE}/statistics"
        params: dict[str, Any] = {"limit": 50}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        if vid_pozhara:
            params["fireType"] = vid_pozhara
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_pozhar(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("fires.ru API недоступен")

    try:
        url = f"{MCHS_API_BASE}/fires/statistics"
        params = {"limit": 50}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_pozhar(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен")

    return []


async def poisk_chs(
    region: str = "",
    vid_chs: str = "",
    klass_chs: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск чрезвычайных ситуаций.

    Аргументы:
        region: Регион.
        vid_chs: Вид ЧС.
        klass_chs: Класс ЧС.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список чрезвычайных ситуаций.
    """
    try:
        url = f"{MCHS_API_BASE}/emergencies"
        params: dict[str, Any] = {"limit": ogranichenie}
        if region:
            params["region"] = region
        if vid_chs:
            params["type"] = vid_chs
        if klass_chs:
            params["class"] = klass_chs
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_chs(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для ЧС")

    try:
        url = f"{MCHS_OPENDATA_BASE}/emergencies"
        params = {"limit": ogranichenie}
        if region:
            params["region"] = region
        if vid_chs:
            params["type"] = vid_chs
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_chs(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("data.mchs.gov.ru недоступен")

    return []


async def radiatsionnyy_monitoring(
    region: str = "",
) -> list[dict[str, Any]]:
    """Получить данные радиационного мониторинга.

    Аргументы:
        region: Регион мониторинга.

    Возвращает:
        Список данных радиационного мониторинга.
    """
    try:
        url = f"{MCHS_API_BASE}/radiation"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_radiatsiya(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для радиационного мониторинга")

    return []


async def gidrologicheskaya_obstanovka(
    region: str = "",
) -> list[dict[str, Any]]:
    """Получить данные гидрологической обстановки.

    Аргументы:
        region: Регион наблюдения.

    Возвращает:
        Список данных гидрологической обстановки.
    """
    try:
        url = f"{MCHS_API_BASE}/hydrology"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_gidrologiya(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для гидрологии")

    return []


async def preduprezhdeniya_chs(
    region: str = "",
    tip_opasnosti: str = "",
) -> list[dict[str, Any]]:
    """Получить предупреждения о чрезвычайных ситуациях.

    Аргументы:
        region: Регион.
        tip_opasnosti: Тип опасности.

    Возвращает:
        Список предупреждений.
    """
    try:
        url = f"{MCHS_API_BASE}/warnings"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        if tip_opasnosti:
            params["dangerType"] = tip_opasnosti
        data = await http_get(url, params=params, timeout=15.0)
        items = _izvlech_spisok(data)
        if items:
            return [_parse_preduprezhdenie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для предупреждений")

    return []


def get_vidy_chs_list() -> list[dict[str, str]]:
    """Вернуть справочник видов ЧС."""
    return VIDY_CHS


def get_klassy_chs_list() -> list[dict[str, str]]:
    """Вернуть справочник классов ЧС."""
    return KLASSY_CHS


def get_vidy_pojarov_list() -> list[dict[str, str]]:
    """Вернуть справочник видов пожаров."""
    return VIDY_POZHAROV


def get_tipy_opasnosti_list() -> list[dict[str, str]]:
    """Вернуть справочник типов опасностей."""
    return TIPY_OPASNOSTI


def get_federalnye_okruga_list() -> list[dict[str, Any]]:
    """Вернуть справочник федеральных округов МЧС."""
    return FEDERALNYE_OKRUGA_MCHS


def get_statistika_pojarov_static() -> dict[str, Any]:
    """Вернуть статическую статистику пожаров (2023)."""
    return STATISTIKA_POZHAROV_2023


def _izvlech_spisok(data: Any) -> list[Any]:
    """Извлечь список из ответа API."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _parse_pozhar(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о пожаре."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "data": data.get("date", "") or data.get("data", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "vid_pozhara": data.get("fireType", "") or data.get("vid_pozhara", ""),
        "pogibshikh": data.get("deaths", 0) or data.get("pogibshikh", 0),
        "postradavshikh": data.get("injured", 0) or data.get("postradavshikh", 0),
        "ushcherb": data.get("damage") or data.get("ushcherb"),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _parse_chs(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о чрезвычайной ситуации."""
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "vid_chs": data.get("type", "") or data.get("vid_chs", ""),
        "klass_chs": data.get("class", "") or data.get("klass_chs", ""),
        "data_vozniknoveniya": data.get("date", "") or data.get("data_vozniknoveniya", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "opisanie": data.get("description", "") or data.get("opisanie", ""),
        "status": data.get("status", ""),
        "pogibshikh": data.get("deaths", 0) or data.get("pogibshikh", 0),
        "postradavshikh": data.get("injured", 0) or data.get("postradavshikh", 0),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _parse_radiatsiya(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных радиационного мониторинга."""
    return {
        "stantsiya": data.get("station", "") or data.get("stantsiya", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "uroven_radiatsii": data.get("level", 0.0) or data.get("uroven_radiatsii", 0.0),
        "edinitsa": data.get("unit", "мкЗв/ч"),
        "data_izmereniya": data.get("date", "") or data.get("data_izmereniya", ""),
        "norma": data.get("norm", 0.30) or data.get("norma", 0.30),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _parse_gidrologiya(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных гидрологической обстановки."""
    return {
        "reka": data.get("river", "") or data.get("reka", ""),
        "punkt_nablyudeniya": data.get("point", "") or data.get("punkt_nablyudeniya", ""),
        "uroven_vody": data.get("level", 0.0) or data.get("uroven_vody", 0.0),
        "opasnyy_uroven": data.get("dangerLevel") or data.get("opasnyy_uroven"),
        "tendentsiya": data.get("trend", "") or data.get("tendentsiya", ""),
        "data_izmereniya": data.get("date", "") or data.get("data_izmereniya", ""),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _parse_preduprezhdenie(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных предупреждения о ЧС."""
    return {
        "nomer": data.get("id", "") or data.get("nomer", ""),
        "tip_opasnosti": data.get("dangerType", "") or data.get("tip_opasnosti", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "opisanie": data.get("description", "") or data.get("opisanie", ""),
        "data_nachala": data.get("startDate", "") or data.get("data_nachala", ""),
        "data_okonchaniya": data.get("endDate", "") or data.get("data_okonchaniya", ""),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }
