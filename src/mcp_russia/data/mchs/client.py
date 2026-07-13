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

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    FEDERALNYE_OKRUGA_MCHS,
    KLASSY_CHS,
    MCHS_BAZA_API,
    MCHS_BAZA_OTKRYTYKH_DANNYKH,
    POZHARY_BAZA_STATISTIKI,
    STATISTIKA_POZHAROV_2023,
    TIPY_OPASNOSTI,
    VIDY_CHS,
    VIDY_POZHAROV,
)

logger = logging.getLogger(__name__)


async def statistika_pojarov(
    subiekt: str = "",
    god: int = 0,
    vid_pozhara: str = "",
) -> list[dict[str, Any]]:
    """Получить статистику пожаров.

    Аргументы:
        subiekt: Субъект РФ или федеральный округ.
        god: Год статистики.
        vid_pozhara: Вид пожара.

    Возвращает:
        Список данных о пожарах.
    """
    try:
        adres_url = f"{POZHARY_BAZA_STATISTIKI}/statistics"
        parametry: dict[str, Any] = {"limit": 50}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        if vid_pozhara:
            parametry["fireType"] = vid_pozhara
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_pozhar(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("fires.ru API недоступен")

    try:
        adres_url = f"{MCHS_BAZA_API}/fires/statistics"
        parametry = {"limit": 50}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_pozhar(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен")

    return []


async def poisk_chs(
    subiekt: str = "",
    vid_chs: str = "",
    klass_chs: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск чрезвычайных ситуаций.

    Аргументы:
        subiekt: Регион.
        vid_chs: Вид ЧС.
        klass_chs: Класс ЧС.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список чрезвычайных ситуаций.
    """
    try:
        adres_url = f"{MCHS_BAZA_API}/emergencies"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if vid_chs:
            parametry["type"] = vid_chs
        if klass_chs:
            parametry["class"] = klass_chs
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_chs(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для ЧС")

    try:
        adres_url = f"{MCHS_BAZA_OTKRYTYKH_DANNYKH}/emergencies"
        parametry = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if vid_chs:
            parametry["type"] = vid_chs
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_chs(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("data.mchs.gov.ru недоступен")

    return []


async def radiatsionnyy_monitoring(
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Получить данные радиационного мониторинга.

    Аргументы:
        subiekt: Регион мониторинга.

    Возвращает:
        Список данных радиационного мониторинга.
    """
    try:
        adres_url = f"{MCHS_BAZA_API}/radiation"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_radiatsiyu(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для радиационного мониторинга")

    return []


async def gidrologicheskaya_obstanovka(
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Получить данные гидрологической обстановки.

    Аргументы:
        subiekt: Регион наблюдения.

    Возвращает:
        Список данных гидрологической обстановки.
    """
    try:
        adres_url = f"{MCHS_BAZA_API}/hydrology"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_gidrologiyu(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для гидрологии")

    return []


async def preduprezhdeniya_chs(
    subiekt: str = "",
    tip_opasnosti: str = "",
) -> list[dict[str, Any]]:
    """Получить предупреждения о чрезвычайных ситуациях.

    Аргументы:
        subiekt: Регион.
        tip_opasnosti: Тип опасности.

    Возвращает:
        Список предупреждений.
    """
    try:
        adres_url = f"{MCHS_BAZA_API}/warnings"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if tip_opasnosti:
            parametry["dangerType"] = tip_opasnosti
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_preduprezhdenie(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.debug("mchs.gov.ru API недоступен для предупреждений")

    return []


def poluchit_spisok_vidov_chs() -> list[dict[str, str]]:
    """Вернуть справочник видов ЧС."""
    return VIDY_CHS


def poluchit_spisok_klassov_chs() -> list[dict[str, str]]:
    """Вернуть справочник классов ЧС."""
    return KLASSY_CHS


def poluchit_spisok_vidov_pozharov() -> list[dict[str, str]]:
    """Вернуть справочник видов пожаров."""
    return VIDY_POZHAROV


def poluchit_spisok_tipov_opasnosti() -> list[dict[str, str]]:
    """Вернуть справочник типов опасностей."""
    return TIPY_OPASNOSTI


def poluchit_spisok_federalnykh_okrugov() -> list[dict[str, Any]]:
    """Вернуть справочник федеральных округов МЧС."""
    return FEDERALNYE_OKRUGA_MCHS


def poluchit_statistiku_pozharov_staticheskie() -> dict[str, Any]:
    """Вернуть статическую статистику пожаров (2023)."""
    return STATISTIKA_POZHAROV_2023


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for klyuch in ("data", "items", "results", "records"):
            znachenie_spiska = dannye.get(klyuch)
            if isinstance(znachenie_spiska, list):
                return znachenie_spiska
    return []


def _razobrat_pozhar(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о пожаре."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "data": dannye.get("date", "") or dannye.get("data", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "vid_pozhara": dannye.get("fireType", "") or dannye.get("vid_pozhara", ""),
        "pogibshikh": dannye.get("deaths", 0) or dannye.get("pogibshikh", 0),
        "postradavshikh": dannye.get("injured", 0) or dannye.get("postradavshikh", 0),
        "ushcherb": dannye.get("damage") or dannye.get("ushcherb"),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _razobrat_chs(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о чрезвычайной ситуации."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", "") or dannye.get("nomer", ""),
        "vid_chs": dannye.get("type", "") or dannye.get("vid_chs", ""),
        "klass_chs": dannye.get("class", "") or dannye.get("klass_chs", ""),
        "data_vozniknoveniya": dannye.get("date", "") or dannye.get("data_vozniknoveniya", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "sostoyanie": dannye.get("status", ""),
        "pogibshikh": dannye.get("deaths", 0) or dannye.get("pogibshikh", 0),
        "postradavshikh": dannye.get("injured", 0) or dannye.get("postradavshikh", 0),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _razobrat_radiatsiyu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных радиационного мониторинга."""
    return {
        "stantsiya": dannye.get("station", "") or dannye.get("stantsiya", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "uroven_radiatsii": dannye.get("level", 0.0) or dannye.get("uroven_radiatsii", 0.0),
        "edinitsa": dannye.get("unit", "мкЗв/ч"),
        "data_izmereniya": dannye.get("date", "") or dannye.get("data_izmereniya", ""),
        "norma": dannye.get("norm", 0.30) or dannye.get("norma", 0.30),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _razobrat_gidrologiyu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных гидрологической обстановки."""
    return {
        "reka": dannye.get("river", "") or dannye.get("reka", ""),
        "punkt_nablyudeniya": dannye.get("point", "") or dannye.get("punkt_nablyudeniya", ""),
        "uroven_vody": dannye.get("level", 0.0) or dannye.get("uroven_vody", 0.0),
        "opasnyy_uroven": dannye.get("dangerLevel") or dannye.get("opasnyy_uroven"),
        "tendentsiya": dannye.get("trend", "") or dannye.get("tendentsiya", ""),
        "data_izmereniya": dannye.get("date", "") or dannye.get("data_izmereniya", ""),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }


def _razobrat_preduprezhdenie(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных предупреждения о ЧС."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("nomer", ""),
        "tip_opasnosti": dannye.get("dangerType", "") or dannye.get("tip_opasnosti", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "data_nachala": dannye.get("startDate", "") or dannye.get("data_nachala", ""),
        "data_okonchaniya": dannye.get("endDate", "") or dannye.get("data_okonchaniya", ""),
        "istochnik": "МЧС России (mchs.gov.ru)",
    }
