"""HTTP-клиент для модуля Минздрава РФ.

Интеграция с реальными API:
    - Открытые данные Минздрава: data.minzdrav.gov.ru
    - Росздравнадзор: roszdravnadzor.gov.ru
    - ФРМО (Федеральный реестр медицинских организаций)
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    FEDERALNYE_OKRUGA,
    FRMO_API_BASE,
    MINZDRAV_OPEN_DATA,
    MKB10_CLASSES,
    POKAZATELI_ZDOROVYA,
    ROSZDRAVNADZOR_API,
    SPETSIALNOSTI_VRACHEY,
    TIPLY_MO,
)

logger = logging.getLogger(__name__)


async def poisk_med_organizatsiy(
    region: str = "",
    tip: str = "",
    gorod: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск медицинских организаций через ФРМО.

    Аргументы:
        region: Субъект РФ.
        tip: Тип организации (больница, поликлиника и т.д.).
        gorod: Город.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список медицинских организаций.
    """
    try:
        url = f"{FRMO_API_BASE}/organizations"
        params: dict[str, Any] = {"limit": ogranichenie}
        if region:
            params["region"] = region
        if tip:
            params["type"] = tip
        if gorod:
            params["city"] = gorod
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_med_organizatsia(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске медицинских организаций")
        return []


async def info_med_organizatsii(identifikator_mo: str) -> dict[str, Any] | None:
    """Получить подробную информацию о медицинской организации.

    Аргументы:
        identifikator_mo: Идентификатор медицинской организации (ОГРН/ИНН).

    Возвращает:
        Данные организации или None.
    """
    try:
        url = f"{FRMO_API_BASE}/organizations/{identifikator_mo}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_med_organizatsia(data)
        return None
    except Exception:
        logger.exception("Ошибка при получении МО %s", identifikator_mo)
        return None


async def poisk_litsenziy(
    inn: str = "",
    vid: str = "",
    status: str = "",
) -> list[dict[str, Any]]:
    """Поиск лицензий Росздравнадзора.

    Аргументы:
        inn: ИНН организации.
        vid: Вид лицензируемой деятельности.
        status: Статус лицензии.

    Возвращает:
        Список лицензий.
    """
    try:
        url = f"{ROSZDRAVNADZOR_API}/licenses"
        params: dict[str, Any] = {}
        if inn:
            params["inn"] = inn
        if vid:
            params["type"] = vid
        if status:
            params["status"] = status
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_litsenziya(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске лицензий")
        return []


async def pokazateli_zdorovya(
    region: str = "",
    god: int = 0,
    kod_pokazatelya: str = "",
) -> list[dict[str, Any]]:
    """Получить показатели здоровья населения из открытых данных Минздрава.

    Аргументы:
        region: Субъект РФ (пусто = вся Россия).
        god: Год данных.
        kod_pokazatelya: Код показателя (опционально).

    Возвращает:
        Список показателей здоровья.
    """
    try:
        url = f"{MINZDRAV_OPEN_DATA}/indicators"
        params: dict[str, Any] = {}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        if kod_pokazatelya:
            params["code"] = kod_pokazatelya
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_pokazatel(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении показателей здоровья")
        return []


async def statistika_zabolevaniy(
    kod_mkb: str = "",
    region: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Получить статистику заболеваний из открытых данных Минздрава.

    Аргументы:
        kod_mkb: Код МКБ-10.
        region: Субъект РФ.
        god: Год данных.

    Возвращает:
        Статистика заболеваний.
    """
    try:
        url = f"{MINZDRAV_OPEN_DATA}/morbidity"
        params: dict[str, Any] = {}
        if kod_mkb:
            params["mkb"] = kod_mkb
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_zabolevanie(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении статистики заболеваний")
        return []


def get_tipy_mo() -> list[dict[str, str]]:
    """Вернуть справочник типов медицинских организаций."""
    return TIPLY_MO


def get_spetsialnosti() -> list[dict[str, str]]:
    """Вернуть справочник врачебных специальностей."""
    return SPETSIALNOSTI_VRACHEY


def get_mkb10_classes() -> list[dict[str, str]]:
    """Вернуть справочник классов МКБ-10."""
    return MKB10_CLASSES


def get_federalnyye_okruga() -> list[dict[str, str]]:
    """Вернуть справочник федеральных округов."""
    return FEDERALNYE_OKRUGA


def get_pokazateli_zdorovya_list() -> list[dict[str, str]]:
    """Вернуть справочник показателей здоровья."""
    return POKAZATELI_ZDOROVYA


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


def _parse_med_organizatsia(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных медицинской организации."""
    return {
        "identifikator": item.get("id", "") or item.get("ogrn", ""),
        "nazvanie": item.get("name", "") or item.get("fullName", ""),
        "tip": item.get("type", "") or item.get("tip", ""),
        "region": item.get("region", "") or item.get("subject", ""),
        "gorod": item.get("city", "") or item.get("settlement", ""),
        "adres": item.get("address", "") or item.get("adres", ""),
        "telefon": item.get("phone", "") or item.get("telefon", ""),
        "litsenzia": item.get("license", "") or item.get("litsenzia", ""),
        "krovatey": item.get("beds", 0) or item.get("krovatey", 0),
        "vrachey": item.get("doctors", 0) or item.get("vrachey", 0),
        "istochnik": "ФРМО (frrr.rosminzdrav.ru)",
    }


def _parse_litsenziya(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных лицензии."""
    return {
        "nomer": item.get("number", "") or item.get("nomer", ""),
        "organizaciya": item.get("organizationName", "") or item.get("name", ""),
        "inn": item.get("inn", ""),
        "vid_deyatelnosti": item.get("activityType", "") or item.get("vid", ""),
        "data_vydachi": item.get("issueDate", "") or item.get("data_vydachi", ""),
        "data_okonchaniya": item.get("endDate", "") or item.get("data_okonchaniya", ""),
        "status": item.get("status", ""),
        "adres": item.get("address", "") or item.get("adres", ""),
        "istochnik": "Росздравнадзор (roszdravnadzor.gov.ru)",
    }


def _parse_pokazatel(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных показателя здоровья."""
    return {
        "kod": item.get("code", "") or item.get("kod", ""),
        "nazvanie": item.get("name", ""),
        "znachenie": item.get("value") or item.get("znachenie", 0),
        "ed_izm": item.get("unit", "") or item.get("ed_izm", ""),
        "god": item.get("year") or item.get("god", 0),
        "region": item.get("region", ""),
        "istochnik": item.get("source", "Открытые данные Минздрава"),
    }


def _parse_zabolevanie(item: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о заболевании."""
    return {
        "kod_mkb": item.get("mkbCode", "") or item.get("mkb_code", ""),
        "nazvanie": item.get("name", "") or item.get("diseaseName", ""),
        "chelovek_zabolelo": item.get("cases") or item.get("chelovek_zabolelo", 0),
        "chelovek_vylechilos": item.get("recovered") or item.get("chelovek_vylechilos", 0),
        "letalnykh_sluchaev": item.get("deaths") or item.get("letalnykh_sluchaev", 0),
        "god": item.get("year") or item.get("god", 0),
        "region": item.get("region", ""),
    }
