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
from mcp_russia._shared.http_client import http_get

from .constants import (
    OTRASLI,
    SPOSOBY_ZAKUPOK,
    STATUSY_ZAKUPOK,
    TIPLY_DANNYKH,
    ZAKUPKI_API_BASE,
)
from .schemas import Kontrakt, PlanZakupki, Postavshchik, Zakazchik, Zakupka


def _get_api_token() -> str:
    """Get Zakupki API token from settings."""
    return settings.ZAKUPKI_API_TOKEN


async def poisk_zakupok(
    query: str = "",
    zakon: str = "",
    region: str = "",
    status: str = "",
    limit: int = 20,
) -> list[Zakupka]:
    """Поиск закупок в ЕИС по параметрам.

    Args:
        query: Поисковый запрос (название закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        region: Регион заказчика.
        status: Статус закупки.
        limit: Максимальное количество результатов.

    Returns:
        Список закупок.
    """
    params: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(limit, 50),
    }
    if query:
        params["searchString"] = query
    if zakon:
        if "44" in zakon:
            params["fz44"] = "on"
        elif "223" in zakon:
            params["fz223"] = "on"
    if region:
        params["regions"] = region
    if status:
        params["statuses"] = status

    token = _get_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/search"
    try:
        data = await http_get(url, params=params)
        return _parse_zakupki_search(data)
    except Exception:
        return []


def _parse_zakupki_search(data: Any) -> list[Zakupka]:
    """Parse search results into Zakupka list."""
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
                id=str(item.get("id", item.get("regNumber", ""))),
                number=item.get("regNumber", item.get("number", "")),
                title=item.get("name", item.get("title", item.get("objectInfo", ""))),
                zakon=_determine_zakon(item),
                sposob=item.get("purchaseMethod", item.get("method", "")),
                status=item.get("status", item.get("commonStatus", "")),
                initial_price=_safe_float(item.get("price", item.get("maxPrice", 0))),
                currency=item.get("currency", "RUB"),
                publish_date=item.get("publishDate", item.get("docPublishDate", "")),
                deadline=item.get("endDate", item.get("bidEndDate", "")),
                organizer_name=item.get("customerName", item.get("organizerName", "")),
                organizer_inn=item.get("customerInn", item.get("organizerInn", "")),
            )
        )
    return results


def _determine_zakon(item: dict[str, Any]) -> str:
    """Determine which law applies (44-ФЗ or 223-ФЗ)."""
    fz = item.get("fz", item.get("law", ""))
    if isinstance(fz, (int, float)):
        fz = str(int(fz))
    if "44" in fz or "44" in str(item.get("purchaseCode", "")):
        return "44-ФЗ"
    if "223" in fz or "223" in str(item.get("purchaseCode", "")):
        return "223-ФЗ"
    return ""


def _safe_float(value: Any) -> float:
    """Safely convert a value to float."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


async def poluchit_zakupku(id_zakupki: str) -> Zakupka | None:
    """Получить подробную информацию о конкретной закупке.

    Args:
        id_zakupki: Идентификатор закупки в ЕИС (реестровый номер).

    Returns:
        Данные закупки или None.
    """
    token = _get_api_token()
    params: dict[str, str] = {}
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/card/{id_zakupki}"
    try:
        data = await http_get(url, params=params)
        if isinstance(data, dict):
            items = _parse_zakupki_search([data])
            return items[0] if items else None
    except Exception:
        pass
    return None


async def poisk_kontraktov(
    contractor_inn: str = "",
    zakazchik_inn: str = "",
    limit: int = 20,
) -> list[Kontrakt]:
    """Поиск контрактов в реестре.

    Args:
        contractor_inn: ИНН поставщика.
        zakazchik_inn: ИНН заказчика.
        limit: Максимальное количество результатов.

    Returns:
        Список контрактов.
    """
    params: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(limit, 50),
    }
    if contractor_inn:
        params["supplierInn"] = contractor_inn
    if zakazchik_inn:
        params["customerInn"] = zakazchik_inn

    token = _get_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/contracts"
    try:
        data = await http_get(url, params=params)
        return _parse_kontrakty(data)
    except Exception:
        return []


def _parse_kontrakty(data: Any) -> list[Kontrakt]:
    """Parse contract search results."""
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
                id=str(item.get("id", "")),
                number=item.get("regNum", item.get("contractNumber", "")),
                zakupka_number=item.get("purchaseNumber", ""),
                contractor_name=item.get("supplierName", item.get("contractorName", "")),
                contractor_inn=item.get("supplierInn", item.get("contractorInn", "")),
                price=_safe_float(item.get("price", item.get("contractPrice", 0))),
                currency=item.get("currency", "RUB"),
                sign_date=item.get("signDate", item.get("contractDate", "")),
                status=item.get("status", item.get("contractStatus", "")),
                execution_deadline=item.get("executionDate", item.get("endDate", "")),
            )
        )
    return results


async def info_zakazchika(inn: str) -> Zakazchik | None:
    """Получить информацию о заказчике по ИНН.

    Uses the ЕГРЮЛ data from egrul.nalog.ru to get basic organization info.

    Args:
        inn: ИНН заказчика.

    Returns:
        Данные заказчика или None.
    """
    try:
        from mcp_russia.data.fns.client import poluchit_organizaciyu

        org = await poluchit_organizaciyu(inn)
        if org:
            return Zakazchik(
                id=org.inn,
                name=org.nazvanie,
                inn=org.inn,
                kpp="",
                region="",
                adres=org.yuridicheskiy_adres,
                zakupki_count=0,
                total_spent=0.0,
            )
    except Exception:
        pass
    return None


async def info_postavshchika(inn: str) -> Postavshchik | None:
    """Получить информацию о поставщике по ИНН.

    Uses the ЕГРЮЛ/ЕГРИП data from egrul.nalog.ru to get basic info.

    Args:
        inn: ИНН поставщика.

    Returns:
        Данные поставщика или None.
    """
    try:
        from mcp_russia.data.fns.client import poluchit_ip, poluchit_organizaciyu

        if len(inn) == 10:
            org = await poluchit_organizaciyu(inn)
            if org:
                return Postavshchik(
                    id=org.inn,
                    name=org.nazvanie,
                    inn=org.inn,
                    region="",
                    contracts_won=0,
                    contracts_executed=0,
                    total_revenue=0.0,
                    is_dobrosovestny=True,
                )
        elif len(inn) == 12:
            ip = await poluchit_ip(inn)
            if ip:
                return Postavshchik(
                    id=ip.inn,
                    name=ip.fio,
                    inn=ip.inn,
                    region="",
                    contracts_won=0,
                    contracts_executed=0,
                    total_revenue=0.0,
                    is_dobrosovestny=True,
                )
    except Exception:
        pass
    return None


async def plany_zakupok(year: int = 2026, organizer_inn: str = "") -> list[PlanZakupki]:
    """Получить планы-графики закупок.

    Args:
        year: Год плана.
        organizer_inn: ИНН организатора (опционально).

    Returns:
        Список планов-графиков.
    """
    params: dict[str, str | int] = {
        "year": year,
        "pageSize": 50,
    }
    if organizer_inn:
        params["customerInn"] = organizer_inn

    token = _get_api_token()
    if token:
        params["token"] = token

    url = f"{ZAKUPKI_API_BASE}/api/nsi/plans"
    try:
        data = await http_get(url, params=params)
        return _parse_plany(data)
    except Exception:
        return []


def _parse_plany(data: Any) -> list[PlanZakupki]:
    """Parse procurement plans."""
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
                id=str(item.get("id", "")),
                year=item.get("year", 0),
                organizer_name=item.get("customerName", ""),
                organizer_inn=item.get("customerInn", ""),
                items_count=item.get("positionsCount", 0),
                total_budget=_safe_float(item.get("totalSum", 0)),
                created_date=item.get("createDate", ""),
                updated_date=item.get("updateDate", ""),
            )
        )
    return results


def get_tipy_dannykh() -> list[dict[str, str]]:
    """Получить список типов данных ЕИС."""
    return TIPLY_DANNYKH


def get_sposoby_zakupok() -> list[dict[str, str]]:
    """Получить список способов определения поставщиков."""
    return SPOSOBY_ZAKUPOK


def get_otrasli() -> list[dict[str, str]]:
    """Получить список основных отраслей."""
    return OTRASLI


def get_statusy_zakupok() -> list[dict[str, str]]:
    """Получить список статусов закупок."""
    return STATUSY_ZAKUPOK
