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
    ZAKUPKI_API_BASE,
)
from .schemas import Kontrakt, PlanZakupki, Postavshchik, Zakazchik, Zakupka


def _poluchit_api_token() -> str:
    """Получение токена API Закупок из настроек."""
    return settings.ZAKUPKI_API_TOKEN


async def poisk_zakupok(
    zapros: str = "",
    zakon: str = "",
    region: str = "",
    status: str = "",
    ogranichenie: int = 20,
) -> list[Zakupka]:
    """Поиск закупок в ЕИС по параметрам.

    Аргументы:
        zapros: Поисковый запрос (название закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        region: Регион заказчика.
        status: Статус закупки.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список закупок.
    """
    params: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(ogranichenie, 50),
    }
    if zapros:
        params["searchString"] = zapros
    if zakon:
        if "44" in zakon:
            params["fz44"] = "on"
        elif "223" in zakon:
            params["fz223"] = "on"
    if region:
        params["regions"] = region
    if status:
        params["statuses"] = status

    token = _poluchit_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/search"
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_poisk_zakupok(data)
    except Exception:
        return []


def _razobrat_poisk_zakupok(data: Any) -> list[Zakupka]:
    """Разбор результатов поиска в список Zakupka."""
    if isinstance(data, dict):
        items = data.get("results", data.get("items", data.get("list", [])))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            Zakupka(
                identifikator=str(item.get("id", item.get("regNumber", ""))),
                nomer=item.get("regNumber", item.get("number", "")),
                nazvanie=item.get("name", item.get("title", item.get("objectInfo", ""))),
                zakon=_opredelit_zakon(item),
                sposob=item.get("purchaseMethod", item.get("method", "")),
                status=item.get("status", item.get("commonStatus", "")),
                nachalnaya_tsena=_bezopasnoe_veshchestvennoe(
                    item.get("price", item.get("maxPrice", 0))
                ),
                valyuta=item.get("currency", "RUB"),
                data_publikatsii=item.get("publishDate", item.get("docPublishDate", "")),
                srok_podachi=item.get("endDate", item.get("bidEndDate", "")),
                nazvanie_organizatora=item.get("customerName", item.get("organizerName", "")),
                organizator_inn=item.get("customerInn", item.get("organizerInn", "")),
            )
        )
    return results


def _opredelit_zakon(item: dict[str, Any]) -> str:
    """Определение применяемого закона (44-ФЗ или 223-ФЗ)."""
    fz = item.get("fz", item.get("law", ""))
    if isinstance(fz, (int, float)):
        fz = str(int(fz))
    if "44" in fz or "44" in str(item.get("purchaseCode", "")):
        return "44-ФЗ"
    if "223" in fz or "223" in str(item.get("purchaseCode", "")):
        return "223-ФЗ"
    return ""


def _bezopasnoe_veshchestvennoe(value: Any) -> float:
    """Безопасное преобразование значения в float."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


async def poluchit_zakupku(identifikator_zakupki: str) -> Zakupka | None:
    """Получить подробную информацию о конкретной закупке.

    Аргументы:
        identifikator_zakupki: Идентификатор закупки в ЕИС (реестровый номер).

    Возвращает:
        Данные закупки или None.
    """
    token = _poluchit_api_token()
    params: dict[str, str] = {}
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/card/{identifikator_zakupki}"
    try:
        data = await http_poluchit(url, params=params)
        if isinstance(data, dict):
            items = _razobrat_poisk_zakupok([data])
            return items[0] if items else None
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
    params: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(ogranichenie, 50),
    }
    if inn_podryadchika:
        params["supplierInn"] = inn_podryadchika
    if inn_zakazchika:
        params["customerInn"] = inn_zakazchika

    token = _poluchit_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/contracts"
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_kontrakty(data)
    except Exception:
        return []


def _razobrat_kontrakty(data: Any) -> list[Kontrakt]:
    """Разбор результатов поиска контрактов."""
    if isinstance(data, dict):
        items = data.get("results", data.get("items", data.get("list", [])))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            Kontrakt(
                identifikator=str(item.get("id", "")),
                nomer=item.get("regNum", item.get("contractNumber", "")),
                zakupka_nomer=item.get("purchaseNumber", ""),
                nazvanie_podryadchika=item.get("supplierName", item.get("contractorName", "")),
                podryadchik_inn=item.get("supplierInn", item.get("contractorInn", "")),
                tsena=_bezopasnoe_veshchestvennoe(item.get("price", item.get("contractPrice", 0))),
                valyuta=item.get("currency", "RUB"),
                data_podpisaniya=item.get("signDate", item.get("contractDate", "")),
                status=item.get("status", item.get("contractStatus", "")),
                srok_ispolneniya=item.get("executionDate", item.get("endDate", "")),
            )
        )
    return results


async def info_zakazchika(inn: str) -> Zakazchik | None:
    """Получить информацию о заказчике по ИНН.

    Использует данные ЕГРЮЛ с egrul.nalog.ru для получения базовой информации об организации.

    Аргументы:
        inn: ИНН заказчика.

    Возвращает:
        Данные заказчика или None.
    """
    try:
        from mcp_russia.data.fns.client import poluchit_organizaciyu

        org = await poluchit_organizaciyu(inn)
        if org:
            return Zakazchik(
                identifikator=org.inn,
                nazvanie=org.nazvanie,
                inn=org.inn,
                kpp="",
                region="",
                adres=org.yuridicheskiy_adres,
                zakupki_kolichestvo=0,
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
        from mcp_russia.data.fns.client import poluchit_ip, poluchit_organizaciyu

        if len(inn) == 10:
            org = await poluchit_organizaciyu(inn)
            if org:
                return Postavshchik(
                    identifikator=org.inn,
                    nazvanie=org.nazvanie,
                    inn=org.inn,
                    region="",
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
                    region="",
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
    params: dict[str, str | int] = {
        "year": god,
        "pageSize": 50,
    }
    if inn_organizatora:
        params["customerInn"] = inn_organizatora

    token = _poluchit_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/plans"
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_plany(data)
    except Exception:
        return []


def _razobrat_plany(data: Any) -> list[PlanZakupki]:
    """Разбор планов закупок."""
    if isinstance(data, dict):
        items = data.get("results", data.get("items", data.get("list", [])))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            PlanZakupki(
                identifikator=str(item.get("id", "")),
                god=item.get("year", 0),
                nazvanie_organizatora=item.get("customerName", ""),
                organizator_inn=item.get("customerInn", ""),
                kolichestvo_pozitsiy=item.get("positionsCount", 0),
                obshchiy_byudzhet=_bezopasnoe_veshchestvennoe(item.get("totalSum", 0)),
                data_sozdaniya=item.get("createDate", ""),
                data_obnovleniya=item.get("updateDate", ""),
            )
        )
    return results


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
