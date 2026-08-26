"""HTTP-клиент для API ЕИС Закупок.

Интеграция с реальными API:
    - ЕИС закупок: https://zakupki.gov.ru
    - Открытые данные: https://data.zakupki.gov.ru
    - Поиск закупок: https://zakupki.gov.ru/api/nsi/search

API ЕИС предоставляет публичный доступ к данным о закупках.
Полный доступ к API может требовать аутентификацию через ЕСИА.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia import settings
from mcp_russia._shared.http_client import http_poluchit
from mcp_russia._shared.normalizatsiya import (
    bezopasnaya_stroka,
    bezopasnoe_chislo,
    bezopasnoe_tseloe,
    izvlech_spisok,
    pervoe_znachenie,
)

from .constants import (
    OTRASLI,
    SPOSOBY_ZAKUPOK,
    STATUSY_ZAKUPOK,
    TIPLY_DANNYKH,
    ZAKUPKI_BAZA_API,
)
from .schemas import Kontrakt, PlanZakupki, Postavshchik, Zakazchik, Zakupka, ZapisRNP

logger = logging.getLogger(__name__)


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
        logger.exception("Ошибка при поиске закупок")
        return []


def _razobrat_poisk_zakupok(dannye: Any) -> list[Zakupka]:
    """Разбор результатов поиска в список Zakupka."""
    elementy = izvlech_spisok(dannye, "results", "items", "list")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Zakupka(
                identifikator=bezopasnaya_stroka(pervoe_znachenie(zapis, "id", "regNumber")),
                nomer=bezopasnaya_stroka(pervoe_znachenie(zapis, "regNumber", "number")),
                nazvanie=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "name", "title", "objectInfo")
                ),
                zakon=_opredelit_zakon(zapis),
                sposob=bezopasnaya_stroka(pervoe_znachenie(zapis, "purchaseMethod", "method")),
                sostoyanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "status", "commonStatus")),
                nachalnaya_tsena=bezopasnoe_chislo(
                    pervoe_znachenie(zapis, "price", "maxPrice"), po_umolchaniyu=0.0
                )
                or 0.0,
                valyuta=bezopasnaya_stroka(zapis.get("currency")) or "RUB",
                data_publikatsii=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "publishDate", "docPublishDate")
                ),
                srok_podachi=bezopasnaya_stroka(pervoe_znachenie(zapis, "endDate", "bidEndDate")),
                nazvanie_organizatora=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "customerName", "organizerName")
                ),
                organizator_inn=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "customerInn", "organizerInn")
                ),
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
        logger.exception("Ошибка при получении закупки %s", identifikator_zakupki)
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
        logger.exception("Ошибка при поиске контрактов")
        return []


def _razobrat_kontrakty(dannye: Any) -> list[Kontrakt]:
    """Разбор результатов поиска контрактов."""
    elementy = izvlech_spisok(dannye, "results", "items", "list")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Kontrakt(
                identifikator=bezopasnaya_stroka(zapis.get("id")),
                nomer=bezopasnaya_stroka(pervoe_znachenie(zapis, "regNum", "contractNumber")),
                zakupka_nomer=bezopasnaya_stroka(zapis.get("purchaseNumber")),
                nazvanie_podryadchika=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "supplierName", "contractorName")
                ),
                podryadchik_inn=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "supplierInn", "contractorInn")
                ),
                tsena=bezopasnoe_chislo(
                    pervoe_znachenie(zapis, "price", "contractPrice"), po_umolchaniyu=0.0
                )
                or 0.0,
                valyuta=bezopasnaya_stroka(zapis.get("currency")) or "RUB",
                data_podpisaniya=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "signDate", "contractDate")
                ),
                sostoyanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "status", "contractStatus")),
                srok_ispolneniya=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "executionDate", "endDate")
                ),
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
        logger.exception("Ошибка при получении информации о заказчике %s", inn)
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
                    dobrosovestny=True,
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
                    dobrosovestny=True,
                )
    except Exception:
        logger.exception("Ошибка при получении информации о поставщике %s", inn)
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
        logger.exception("Ошибка при получении планов закупок")
        return []


def _razobrat_plany(dannye: Any) -> list[PlanZakupki]:
    """Разбор планов закупок."""
    elementy = izvlech_spisok(dannye, "results", "items", "list")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            PlanZakupki(
                identifikator=bezopasnaya_stroka(zapis.get("id")),
                god=bezopasnoe_tseloe(zapis.get("year")),
                nazvanie_organizatora=bezopasnaya_stroka(zapis.get("customerName")),
                organizator_inn=bezopasnaya_stroka(zapis.get("customerInn")),
                kolichestvo_pozitsiy=bezopasnoe_tseloe(zapis.get("positionsCount")),
                obshchiy_byudzhet=bezopasnoe_chislo(zapis.get("totalSum"), po_umolchaniyu=0.0)
                or 0.0,
                data_sozdaniya=bezopasnaya_stroka(zapis.get("createDate")),
                data_obnovleniya=bezopasnaya_stroka(zapis.get("updateDate")),
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


async def poisk_rnp(
    inn: str = "",
    nazvanie: str = "",
    god: int = 0,
    ogranichenie: int = 20,
) -> list[ZapisRNP]:
    """Поиск в реестре недобросовестных поставщиков (РНП).

    Аргументы:
        inn: ИНН поставщика.
        nazvanie: Название организации.
        god: Год включения в РНП.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список записей РНП.
    """
    parametry: dict[str, str | int] = {
        "pageNumber": 1,
        "pageSize": min(ogranichenie, 50),
    }
    if inn:
        parametry["inn"] = inn
    if nazvanie:
        parametry["name"] = nazvanie
    if god:
        parametry["year"] = god

    zheton = _poluchit_api_token()
    if zheton:
        parametry["token"] = zheton

    adres_url = f"{ZAKUPKI_BAZA_API}/api/nsi/rnp"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_rnp(dannye)
    except Exception:
        logger.exception("Ошибка при поиске в РНП")
        return []


def _razobrat_rnp(dannye: Any) -> list[ZapisRNP]:
    """Разбор результатов поиска РНП."""
    elementy = izvlech_spisok(dannye, "results", "items", "list")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            ZapisRNP(
                identifikator=bezopasnaya_stroka(zapis.get("id")),
                inn=bezopasnaya_stroka(pervoe_znachenie(zapis, "inn", "supplierInn")),
                nazvanie=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "name", "supplierName", "fullName")
                ),
                data_vklyucheniya=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "includeDate", "dateInclusion")
                ),
                osnovanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "reason", "basis")),
                organ_zakazchik=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "customerName", "organizerName")
                ),
                nomer_zakupki=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "purchaseNumber", "tenderNumber")
                ),
                sostoyanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "status", "rnpStatus")),
            )
        )
    return rezultaty
