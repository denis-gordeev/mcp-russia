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
    FRMO_API_BAZA,
    MINZDRAV_OTKRYTYE_DANNYE,
    MKB10_KLASSY,
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
        subiekt: Субъект РФ.
        tip: Тип организации (больница, поликлиника и т.д.).
        gorod: Город.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список медицинских организаций.
    """
    try:
        adres_url = f"{FRMO_API_BAZA}/organizations"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if tip:
            parametry["type"] = tip
            parametry["city"] = gorod
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [
            _razobrat_med_organizatsiyu(zapis) for zapis in elementy if isinstance(zapis, dict)
        ]
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
        adres_url = f"{FRMO_API_BAZA}/organizations/{identifikator_mo}"
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
        return [_razobrat_litsenziyu(zapis) for zapis in elementy if isinstance(zapis, dict)]
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
        subiekt: Субъект РФ (пусто = вся Россия).
        god: Год данных.
        kod_pokazatelya: Код показателя (опционально).

    Возвращает:
        Список показателей здоровья.
    """
    try:
        adres_url = f"{MINZDRAV_OTKRYTYE_DANNYE}/indicators"
        parametry: dict[str, Any] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        if kod_pokazatelya:
            parametry["code"] = kod_pokazatelya
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_pokazatel(zapis) for zapis in elementy if isinstance(zapis, dict)]
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
        subiekt: Субъект РФ.
        god: Год данных.

    Возвращает:
        Статистика заболеваний.
    """
    try:
        adres_url = f"{MINZDRAV_OTKRYTYE_DANNYE}/morbidity"
        parametry: dict[str, Any] = {}
        if kod_mkb:
            parametry["mkb"] = kod_mkb
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        return [_razobrat_zabolevanie(zapis) for zapis in elementy if isinstance(zapis, dict)]
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
    return MKB10_KLASSY


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
        for klyuch in ("data", "items", "results", "records"):
            znachenie_spiska = dannye.get(klyuch)
            if isinstance(znachenie_spiska, list):
                return znachenie_spiska
    return []


def _razobrat_med_organizatsiyu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных медицинской организации."""
    return {
        "identifikator": zapis.get("id", "") or zapis.get("ogrn", ""),
        "nazvanie": zapis.get("name", "") or zapis.get("fullName", ""),
        "tip": zapis.get("type", "") or zapis.get("tip", ""),
        "subiekt": zapis.get("region", "") or zapis.get("subject", ""),
        "gorod": zapis.get("city", "") or zapis.get("settlement", ""),
        "adres": zapis.get("address", "") or zapis.get("adres", ""),
        "telefon": zapis.get("phone", "") or zapis.get("telefon", ""),
        "litsenzia": zapis.get("license", "") or zapis.get("litsenzia", ""),
        "krovatey": zapis.get("beds", 0) or zapis.get("krovatey", 0),
        "vrachey": zapis.get("doctors", 0) or zapis.get("vrachey", 0),
        "istochnik": "ФРМО (frrr.rosminzdrav.ru)",
    }


def _razobrat_litsenziyu(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных лицензии."""
    return {
        "nomer": zapis.get("number", "") or zapis.get("nomer", ""),
        "organizatsiya": zapis.get("organizationName", "") or zapis.get("name", ""),
        "inn": zapis.get("inn", ""),
        "vid_deyatelnosti": zapis.get("activityType", "") or zapis.get("vid", ""),
        "data_vydachi": zapis.get("issueDate", "") or zapis.get("data_vydachi", ""),
        "data_okonchaniya": zapis.get("endDate", "") or zapis.get("data_okonchaniya", ""),
        "sostoyanie": zapis.get("status", ""),
        "adres": zapis.get("address", "") or zapis.get("adres", ""),
        "istochnik": "Росздравнадзор (roszdravnadzor.gov.ru)",
    }


def _razobrat_pokazatel(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных показателя здоровья."""
    return {
        "kod": zapis.get("code", "") or zapis.get("kod", ""),
        "nazvanie": zapis.get("name", ""),
        "znachenie": zapis.get("value") or zapis.get("znachenie", 0),
        "ed_izm": zapis.get("unit", "") or zapis.get("ed_izm", ""),
        "god": zapis.get("year") or zapis.get("god", 0),
        "subiekt": zapis.get("region", ""),
        "istochnik": zapis.get("source", "Открытые данные Минздрава"),
    }


def _razobrat_zabolevanie(zapis: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о заболевании."""
    return {
        "kod_mkb": zapis.get("mkbCode", "") or zapis.get("mkb_code", ""),
        "nazvanie": zapis.get("name", "") or zapis.get("diseaseName", ""),
        "chelovek_zabolelo": zapis.get("cases") or zapis.get("chelovek_zabolelo", 0),
        "chelovek_vylechilos": zapis.get("recovered") or zapis.get("chelovek_vylechilos", 0),
        "letalnykh_sluchaev": zapis.get("deaths") or zapis.get("letalnykh_sluchaev", 0),
        "god": zapis.get("year") or zapis.get("god", 0),
        "subiekt": zapis.get("region", ""),
    }
