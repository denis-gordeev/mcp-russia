"""HTTP-клиент для модуля Минздрава РФ.

Интеграция с реальными API:
    - Открытые данные Минздрава: data.minzdrav.gov.ru
    - Росздравнадзор: roszdravnadzor.gov.ru
    - ФРМО (Федеральный реестр медицинских организаций)
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

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
    subiekt: str = "",
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
        adres_url = f"{FRMO_API_BASE}/organizations"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if tip:
            parametry["type"] = tip
            parametry["city"] = gorod
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_med_organizatsiyu(p) for p in elementy if isinstance(p, dict)]
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
        adres_url = f"{FRMO_API_BASE}/organizations/{identifikator_mo}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        if isinstance(dannye, dict):
            return _razobrat_med_organizatsiyu(dannye)
        return None
    except Exception:
        logger.exception("Ошибка при получении МО %s", identifikator_mo)
        return None


async def poisk_litsenziy(
    inn: str = "",
    vid: str = "",
    sostoyanie: str = "",
) -> list[dict[str, Any]]:
    """Поиск лицензий Росздравнадзора.

    Аргументы:
        inn: ИНН организации.
        vid: Вид лицензируемой деятельности.
        sostoyanie: Статус лицензии.

    Возвращает:
        Список лицензий.
    """
    try:
        adres_url = f"{ROSZDRAVNADZOR_API}/licenses"
        parametry: dict[str, Any] = {}
        if inn:
            parametry["inn"] = inn
        if vid:
            parametry["type"] = vid
        if sostoyanie:
            parametry["status"] = sostoyanie
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_litsenziyu(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при поиске лицензий")
        return []


async def pokazateli_zdorovya(
    subiekt: str = "",
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
        adres_url = f"{MINZDRAV_OPEN_DATA}/indicators"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        if kod_pokazatelya:
            parametry["code"] = kod_pokazatelya
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_pokazatel(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении показателей здоровья")
        return []


async def statistika_zabolevaniy(
    kod_mkb: str = "",
    subiekt: str = "",
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
        adres_url = f"{MINZDRAV_OPEN_DATA}/morbidity"
        parametry: dict[str, Any] = {}
        if kod_mkb:
            parametry["mkb"] = kod_mkb
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_zabolevanie(p) for p in elementy if isinstance(p, dict)]
    except Exception:
        logger.exception("Ошибка при получении статистики заболеваний")
        return []


def poluchit_tipy_mo() -> list[dict[str, str]]:
    """Вернуть справочник типов медицинских организаций."""
    return TIPLY_MO


def poluchit_spetsialnosti() -> list[dict[str, str]]:
    """Вернуть справочник врачебных специальностей."""
    return SPETSIALNOSTI_VRACHEY


def poluchit_klassy_mkb10() -> list[dict[str, str]]:
    """Вернуть справочник классов МКБ-10."""
    return MKB10_CLASSES


def poluchit_federalnyye_okruga() -> list[dict[str, str]]:
    """Вернуть справочник федеральных округов."""
    return FEDERALNYE_OKRUGA


def poluchit_spisok_pokazateley_zdorovya() -> list[dict[str, str]]:
    """Вернуть справочник показателей здоровья."""
    return POKAZATELI_ZDOROVYA


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


def _razobrat_med_organizatsiyu(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных медицинской организации."""
    return {
        "identifikator": element.get("id", "") or element.get("ogrn", ""),
        "nazvanie": element.get("name", "") or element.get("fullName", ""),
        "tip": element.get("type", "") or element.get("tip", ""),
        "subiekt": element.get("region", "") or element.get("subject", ""),
        "gorod": element.get("city", "") or element.get("settlement", ""),
        "adres": element.get("address", "") or element.get("adres", ""),
        "telefon": element.get("phone", "") or element.get("telefon", ""),
        "litsenzia": element.get("license", "") or element.get("litsenzia", ""),
        "krovatey": element.get("beds", 0) or element.get("krovatey", 0),
        "vrachey": element.get("doctors", 0) or element.get("vrachey", 0),
        "istochnik": "ФРМО (frrr.rosminzdrav.ru)",
    }


def _razobrat_litsenziyu(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных лицензии."""
    return {
        "nomer": element.get("number", "") or element.get("nomer", ""),
        "organizaciya": element.get("organizationName", "") or element.get("name", ""),
        "inn": element.get("inn", ""),
        "vid_deyatelnosti": element.get("activityType", "") or element.get("vid", ""),
        "data_vydachi": element.get("issueDate", "") or element.get("data_vydachi", ""),
        "data_okonchaniya": element.get("endDate", "") or element.get("data_okonchaniya", ""),
        "sostoyanie": element.get("status", ""),
        "adres": element.get("address", "") or element.get("adres", ""),
        "istochnik": "Росздравнадзор (roszdravnadzor.gov.ru)",
    }


def _razobrat_pokazatel(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных показателя здоровья."""
    return {
        "kod": element.get("code", "") or element.get("kod", ""),
        "nazvanie": element.get("name", ""),
        "znachenie": element.get("value") or element.get("znachenie", 0),
        "ed_izm": element.get("unit", "") or element.get("ed_izm", ""),
        "god": element.get("year") or element.get("god", 0),
        "subiekt": element.get("region", ""),
        "istochnik": element.get("source", "Открытые данные Минздрава"),
    }


def _razobrat_zabolevanie(element: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о заболевании."""
    return {
        "kod_mkb": element.get("mkbCode", "") or element.get("mkb_code", ""),
        "nazvanie": element.get("name", "") or element.get("diseaseName", ""),
        "chelovek_zabolelo": element.get("cases") or element.get("chelovek_zabolelo", 0),
        "chelovek_vylechilos": element.get("recovered") or element.get("chelovek_vylechilos", 0),
        "letalnykh_sluchaev": element.get("deaths") or element.get("letalnykh_sluchaev", 0),
        "god": element.get("year") or element.get("god", 0),
        "subiekt": element.get("region", ""),
    }
