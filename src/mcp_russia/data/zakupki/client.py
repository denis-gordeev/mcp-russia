"""HTTP-клиент для API ЕИС Закупок.

Интеграция с реальными API:
    - ЕИС закупок: https://zakupki.gov.ru
    - Открытые данные: https://data.zakupki.gov.ru
    - Поиск закупок: https://zakupki.gov.ru/api/nsi/search

API ЕИС предоставляет публичный доступ к данным о закупках.
Полный доступ к API может требовать аутентификацию через ЕСИА.
"""

from __future__ import annotations

from typing import Any

from mcp_russia import settings
from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    OTRASLI,
    SPOSOBY_ZAKUPOK,
    STATUSY_ZAKUPOK,
    TIPLY_DANNYKH,
    ZAKUPKI_BAZA_API,
)
from .schemas import Kontrakt, PlanZakupki, Postavshchik, Zakazchik, Zakupka


def _poluchit_api_token() -> str:
    """Получение токена API Закупок из настроек."""
    return settings.KLYUCH_ZAKUPKI_API


async def poisk_zakupok(
    zapros: str = "",
    zakon: str = "",
    subiekt: str = "",
    sostoyanie: str = "",
    ogranichenie: int = 20,
) -> list[Zakupka]:
    """Поиск закупок в ЕИС по параметрам.

    Аргументы:
        zapros: Поисковый запрос (название закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        subiekt: Регион заказчика.
        sostoyanie: Статус закупки.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список закупок.
    """
    parametry: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(ogranichenie, 50),
    }
    if zapros:
        parametry["searchString"] = zapros
    if zakon:
        if "44" in zakon:
            parametry["fz44"] = "on"
        elif "223" in zakon:
            parametry["fz223"] = "on"
    if subiekt:
        parametry["regions"] = subiekt
    if sostoyanie:
        parametry["statuses"] = sostoyanie

    zheton = _poluchit_api_token()
    if zheton:
        parametry["token"] = zheton

    adres_url = f"{ZAKUPKI_BAZA_API}/api/nsi/search"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_poisk_zakupok(dannye)
    except Exception:
        return []


def _razobrat_poisk_zakupok(dannye: Any) -> list[Zakupka]:
    """Разбор результатов поиска в список Zakupka."""
    if isinstance(dannye, dict):
        elementy = dannye.get("results", dannye.get("items", dannye.get("list", [])))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Zakupka(
                identifikator=str(zapis.get("id", zapis.get("regNumber", ""))),
                nomer=zapis.get("regNumber", zapis.get("number", "")),
                nazvanie=zapis.get("name", zapis.get("title", zapis.get("objectInfo", ""))),
                zakon=_opredelit_zakon(zapis),
                sposob=zapis.get("purchaseMethod", zapis.get("method", "")),
                sostoyanie=zapis.get("status", zapis.get("commonStatus", "")),
                nachalnaya_tsena=_bezopasnoe_veshchestvennoe(
                    zapis.get("price", zapis.get("maxPrice", 0))
                ),
                valyuta=zapis.get("currency", "RUB"),
                data_publikatsii=zapis.get("publishDate", zapis.get("docPublishDate", "")),
                srok_podachi=zapis.get("endDate", zapis.get("bidEndDate", "")),
                nazvanie_organizatora=zapis.get("customerName", zapis.get("organizerName", "")),
                organizator_inn=zapis.get("customerInn", zapis.get("organizerInn", "")),
            )
        )
    return rezultaty


def _opredelit_zakon(zapis: dict[str, Any]) -> str:
    """Определение применяемого закона (44-ФЗ или 223-ФЗ)."""
    fz = zapis.get("fz", zapis.get("law", ""))
    if isinstance(fz, (int, float)):
        fz = str(int(fz))
    if "44" in fz or "44" in str(zapis.get("purchaseCode", "")):
        return "44-ФЗ"
    if "223" in fz or "223" in str(zapis.get("purchaseCode", "")):
        return "223-ФЗ"
    return ""


def _bezopasnoe_veshchestvennoe(znachenie: Any) -> float:
    """Безопасное преобразование значения в float."""
    if znachenie is None:
        return 0.0
    try:
        return float(znachenie)
    except (ValueError, TypeError):
        return 0.0


async def poluchit_zakupku(identifikator_zakupki: str) -> Zakupka | None:
    """Получить подробную информацию о конкретной закупке.

    Аргументы:
        identifikator_zakupki: Идентификатор закупки в ЕИС (реестровый номер).

    Возвращает:
        Данные закупки или None.
    """
    zheton = _poluchit_api_token()
    parametry: dict[str, str] = {}
    if zheton:
        parametry["token"] = zheton

    adres_url = f"{ZAKUPKI_BAZA_API}/api/nsi/card/{identifikator_zakupki}"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        if isinstance(dannye, dict):
            elementy = _razobrat_poisk_zakupok([dannye])
            return elementy[0] if elementy else None
    except Exception:
        pass
    return None


async def poisk_kontraktov(
    inn_podryadchika: str = "",
    inn_zakazchika: str = "",
    ogranichenie: int = 20,
) -> list[Kontrakt]:
    """Поиск контрактов в реестре.

    Аргументы:
        inn_podryadchika: ИНН поставщика.
        inn_zakazchika: ИНН заказчика.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список контрактов.
    """
    parametry: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(ogranichenie, 50),
    }
    if inn_podryadchika:
        parametry["supplierInn"] = inn_podryadchika
    if inn_zakazchika:
        parametry["customerInn"] = inn_zakazchika

    zheton = _poluchit_api_token()
    if zheton:
        parametry["token"] = zheton

    adres_url = f"{ZAKUPKI_BAZA_API}/api/nsi/contracts"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_kontrakty(dannye)
    except Exception:
        return []


def _razobrat_kontrakty(dannye: Any) -> list[Kontrakt]:
    """Разбор результатов поиска контрактов."""
    if isinstance(dannye, dict):
        elementy = dannye.get("results", dannye.get("items", dannye.get("list", [])))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Kontrakt(
                identifikator=str(zapis.get("id", "")),
                nomer=zapis.get("regNum", zapis.get("contractNumber", "")),
                zakupka_nomer=zapis.get("purchaseNumber", ""),
                nazvanie_podryadchika=zapis.get("supplierName", zapis.get("contractorName", "")),
                podryadchik_inn=zapis.get("supplierInn", zapis.get("contractorInn", "")),
                tsena=_bezopasnoe_veshchestvennoe(
                    zapis.get("price", zapis.get("contractPrice", 0))
                ),
                valyuta=zapis.get("currency", "RUB"),
                data_podpisaniya=zapis.get("signDate", zapis.get("contractDate", "")),
                sostoyanie=zapis.get("status", zapis.get("contractStatus", "")),
                srok_ispolneniya=zapis.get("executionDate", zapis.get("endDate", "")),
            )
        )
    return rezultaty


async def info_zakazchika(inn: str) -> Zakazchik | None:
    """Получить информацию о заказчике по ИНН.

    Использует данные ЕГРЮЛ с egrul.nalog.ru для получения базовой информации об организации.

    Аргументы:
        inn: ИНН заказчика.

    Возвращает:
        Данные заказчика или None.
    """
    try:
        from mcp_russia.data.fns.client import poluchit_organizatsiyu

        organizatsiya = await poluchit_organizatsiyu(inn)
        if organizatsiya:
            return Zakazchik(
                identifikator=organizatsiya.inn,
                nazvanie=organizatsiya.nazvanie,
                inn=organizatsiya.inn,
                kpp="",
                subiekt="",
                adres=organizatsiya.yuridicheskiy_adres,
                obshchie_raskhody=0.0,
            )
    except Exception:
        pass
    return None


async def info_postavshchika(inn: str) -> Postavshchik | None:
    """Получить информацию о поставщике по ИНН.

    Использует данные ЕГРЮЛ/ЕГРИП с egrul.nalog.ru для получения базовой информации.

    Аргументы:
        inn: ИНН поставщика.

    Возвращает:
        Данные поставщика или None.
    """
    try:
        from mcp_russia.data.fns.client import poluchit_ip, poluchit_organizatsiyu

        if len(inn) == 10:
            organizatsiya = await poluchit_organizatsiyu(inn)
            if organizatsiya:
                return Postavshchik(
                    identifikator=organizatsiya.inn,
                    nazvanie=organizatsiya.nazvanie,
                    inn=organizatsiya.inn,
                    subiekt="",
                    kontraktov_vyigrano=0,
                    kontraktov_ispolneno=0,
                    obshchiy_dokhod=0.0,
                    is_dobrosovestny=True,
                )
        elif len(inn) == 12:
            ip = await poluchit_ip(inn)
            if ip:
                return Postavshchik(
                    identifikator=ip.inn,
                    nazvanie=ip.fio,
                    inn=ip.inn,
                    subiekt="",
                    kontraktov_vyigrano=0,
                    kontraktov_ispolneno=0,
                    obshchiy_dokhod=0.0,
                    is_dobrosovestny=True,
                )
    except Exception:
        pass
    return None


async def plany_zakupok(god: int = 2026, inn_organizatora: str = "") -> list[PlanZakupki]:
    """Получить планы-графики закупок.

    Аргументы:
        god: Год плана.
        inn_organizatora: ИНН организатора (опционально).

    Возвращает:
        Список планов-графиков.
    """
    parametry: dict[str, str | int] = {
        "year": god,
        "pageSize": 50,
    }
    if inn_organizatora:
        parametry["customerInn"] = inn_organizatora

    zheton = _poluchit_api_token()
    if zheton:
        parametry["token"] = zheton

    adres_url = f"{ZAKUPKI_BAZA_API}/api/nsi/plans"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_plany(dannye)
    except Exception:
        return []


def _razobrat_plany(dannye: Any) -> list[PlanZakupki]:
    """Разбор планов закупок."""
    if isinstance(dannye, dict):
        elementy = dannye.get("results", dannye.get("items", dannye.get("list", [])))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            PlanZakupki(
                identifikator=str(zapis.get("id", "")),
                god=zapis.get("year", 0),
                nazvanie_organizatora=zapis.get("customerName", ""),
                organizator_inn=zapis.get("customerInn", ""),
                kolichestvo_pozitsiy=zapis.get("positionsCount", 0),
                obshchiy_byudzhet=_bezopasnoe_veshchestvennoe(zapis.get("totalSum", 0)),
                data_sozdaniya=zapis.get("createDate", ""),
                data_obnovleniya=zapis.get("updateDate", ""),
            )
        )
    return rezultaty


def poluchit_tipy_dannykh() -> list[dict[str, str]]:
    """Получить список типов данных ЕИС."""
    return TIPLY_DANNYKH


def poluchit_sposoby_zakupok() -> list[dict[str, str]]:
    """Получить список способов определения поставщиков."""
    return SPOSOBY_ZAKUPOK


def poluchit_otrasli() -> list[dict[str, str]]:
    """Получить список основных отраслей."""
    return OTRASLI


def poluchit_statusy_zakupok() -> list[dict[str, str]]:
    """Получить список статусов закупок."""
    return STATUSY_ZAKUPOK
