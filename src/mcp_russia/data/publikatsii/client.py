"""HTTP-клиент для модуля Официальные публикации РФ.

Официальные российские правовые публикации с открытого API pravo.gov.ru,
КонсультантПлюс (платный) и Российская газета (rg.ru).
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    ISTOCHNIKI_PUBLIKATSIY,
    OTRASLI_ZAKONODATELSTVA,
    PRAVO_DOCUMENT_URL,
    PRAVO_SEARCH_URL,
    STATUSY_DOKUMENTOV,
    TIPY_DOKUMENTOV_PRAVO,
    TIPY_NORMATIVNYKH_AKTOV,
)
from .schemas import (
    IzmenenieAkta,
    NormativnyyAkt,
    OficialnayaPublikatsiya,
    ZakonProekt,
)


async def poluchit_normativnyy_akt(nomer: str, tip: str = "") -> NormativnyyAkt | None:
    """Получение нормативного правового акта по номеру из открытых данных pravo.gov.ru.

    Аргументы:
        nomer: Номер/идентификатор акта (напр. «ФЗ-123», «УП-234»).
        tip: Код типа акта (fz, ukaz, postanovlenie_pr и т.д.).

    Возвращает:
        Данные акта или None.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
    params: dict[str, str] = {}
    if tip:
        params["tip"] = tip
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_normativnyy_akt(data)
    except Exception:
        return None


async def poluchit_zakon_proekt(nomer: str) -> ZakonProekt | None:
    """Получение законопроекта по номеру из открытых данных pravo.gov.ru.

    Аргументы:
        nomer: Номер законопроекта.

    Возвращает:
        Данные законопроекта или None.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
    try:
        data = await http_poluchit(url)
        return _razobrat_zakon_proekt(data)
    except Exception:
        return None


async def poluchit_publikatsii(
    tip: str = "",
    otrysl: str = "",
    data_from: str = "",
    data_to: str = "",
) -> list[OficialnayaPublikatsiya]:
    """Поиск официальных публикаций через открытые данные pravo.gov.ru.

    Аргументы:
        tip: Фильтр по типу документа (код типа pravo.gov.ru).
        otrysl: Фильтр по отрасли права.
        data_from: Фильтр по начальной дате (ГГГГ-ММ-ДД).
        data_to: Фильтр по конечной дате (ГГГГ-ММ-ДД).

    Возвращает:
        Список публикаций.
    """
    url = PRAVO_SEARCH_URL
    params: dict[str, str] = {}
    if tip:
        params["type"] = tip
    if otrysl:
        params["branch"] = otrysl
    if data_from:
        params["dateFrom"] = data_from
    if data_to:
        params["dateTo"] = data_to
    try:
        data = await http_poluchit(url, params=params)
        return _razobrat_publikatsii(data)
    except Exception:
        return []


async def poluchit_izmeneniya_akta(akt_nomer: str) -> list[IzmenenieAkta]:
    """Получение поправок к нормативному акту из открытых данных pravo.gov.ru.

    Аргументы:
        akt_nomer: Номер/идентификатор акта.

    Возвращает:
        Список поправок.
    """
    url = f"{PRAVO_DOCUMENT_URL}/{akt_nomer}/amendments"
    try:
        data = await http_poluchit(url)
        return _razobrat_izmeneniya(data)
    except Exception:
        return []


async def poluchit_poisku(tekst: str, tip: str = "") -> list[NormativnyyAkt]:
    """Поиск правовых актов по тексту через открытые данные pravo.gov.ru.

    Аргументы:
        tekst: Поисковый текст.
        tip: Фильтр по типу документа (код типа pravo.gov.ru).

    Возвращает:
        Список найденных актов.
    """
    url = PRAVO_SEARCH_URL
    params: dict[str, str] = {"q": tekst}
    if tip:
        params["type"] = tip
    try:
        data = await http_poluchit(url, params=params)
        return _rezultaty_poiska(data)
    except Exception:
        return []


def poluchit_spisok_tipov_aktov() -> list[dict[str, str]]:
    """Возвращает список типов нормативных актов."""
    return TIPY_NORMATIVNYKH_AKTOV


def poluchit_spisok_otrasley() -> list[dict[str, str]]:
    """Возвращает список отраслей права."""
    return OTRASLI_ZAKONODATELSTVA


def poluchit_spisok_istochnikov() -> list[dict[str, str]]:
    """Возвращает список источников публикаций."""
    return ISTOCHNIKI_PUBLIKATSIY


def poluchit_spisok_statusov() -> list[dict[str, str]]:
    """Возвращает список статусов документов."""
    return STATUSY_DOKUMENTOV


# --- Разборщики ответов ---


def _razobrat_normativnyy_akt(data: Any) -> NormativnyyAkt | None:
    """Разбор ответа открытых данных pravo.gov.ru в NormativnyyAkt."""
    if not isinstance(data, dict):
        return None
    tip_code = str(data.get("type", data.get("tip", "")) or "")
    tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
    return NormativnyyAkt(
        nomer=data.get("number", data.get("nomer", "")) or "",
        nazvanie=data.get("title", data.get("nazvanie", "")) or "",
        tip=tip_name,
        data_prinyatiya=data.get("date", data.get("data_prinyatiya", "")) or "",
        data_publikatsii=data.get("publishDate", data.get("data_publikatsii", "")) or "",
        istochnik=data.get("source", data.get("istochnik", "pravo.gov.ru")) or "",
        sostoyanie=data.get("status", "") or "",
        otrysl=data.get("branch", data.get("otrysl", "")) or "",
        kratkoe_opisanie=data.get("description", data.get("kratkoe_opisanie", "")) or "",
        tekst_ssylka=data.get("url", data.get("tekst_ssylka", "")) or "",
        izmeneniya=data.get("amendments", data.get("izmeneniya", [])) or [],
    )


def _razobrat_zakon_proekt(data: Any) -> ZakonProekt | None:
    """Разбор ответа открытых данных pravo.gov.ru в ZakonProekt."""
    if not isinstance(data, dict):
        return None
    return ZakonProekt(
        nomer=data.get("number", data.get("nomer", "")) or "",
        nazvanie=data.get("title", data.get("nazvanie", "")) or "",
        stadnya=data.get("stage", data.get("stadnya", "")) or "",
        data_vneseniya=data.get("introducedDate", data.get("data_vneseniya", "")) or "",
        vnesen_subiekt=data.get("introducedBy", data.get("vnesen_subiekt", "")) or "",
        otvetstvennyy_komitet=data.get("committee", data.get("otvetstvennyy_komitet", "")) or "",
        chteniya=data.get("readings", data.get("chteniya", [])) or [],
        tekst_ssylka=data.get("url", data.get("tekst_ssylka", "")) or "",
    )


def _razobrat_publikatsii(data: Any) -> list[OficialnayaPublikatsiya]:
    """Разбор поискового ответа открытых данных pravo.gov.ru в список OficialnayaPublikatsiya."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("documents", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        tip_code = str(item.get("type", item.get("tip_dokumenta", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        results.append(
            OficialnayaPublikatsiya(
                nazvanie=item.get("title", item.get("nazvanie", "")),
                tip_dokumenta=tip_name,
                data_publikatsii=item.get("publishDate", item.get("data_publikatsii", "")),
                nomer_vypuska=item.get("issueNumber", item.get("nomer_vypuska", "")),
                istochnik=item.get("source", item.get("istochnik", "pravo.gov.ru")),
                rubrika=item.get("rubric", item.get("rubrika", "")),
                annotaciya=item.get("annotation", item.get("annotaciya", "")),
                tekst_ssylka=item.get("url", item.get("tekst_ssylka", "")),
            )
        )
    return results


def _razobrat_izmeneniya(data: Any) -> list[IzmenenieAkta]:
    """Разбор ответа поправок открытых данных pravo.gov.ru в список IzmenenieAkta."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("amendments", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        results.append(
            IzmenenieAkta(
                akt_nomer=item.get("actNumber", item.get("akt_nomer", "")),
                akt_nazvanie=item.get("actTitle", item.get("akt_nazvanie", "")),
                izmenenie_nomer=item.get("amendmentNumber", item.get("izmenenie_nomer", "")),
                izmenenie_data=item.get("amendmentDate", item.get("izmenenie_data", "")),
                izmenenie_opisanie=item.get(
                    "amendmentDescription", item.get("izmenenie_opisanie", "")
                ),
                data_vstupleniya_v_silu=item.get(
                    "effectiveDate", item.get("data_vstupleniya_v_silu", "")
                ),
                tekst_ssylka=item.get("url", item.get("tekst_ssylka", "")),
            )
        )
    return results


def _rezultaty_poiska(data: Any) -> list[NormativnyyAkt]:
    """Разбор результатов поиска открытых данных pravo.gov.ru в список NormativnyyAkt."""
    items = data
    if isinstance(data, dict):
        items = data.get("items", data.get("results", data.get("documents", [])))
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        tip_code = str(item.get("type", item.get("tip", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        results.append(
            NormativnyyAkt(
                nomer=item.get("number", item.get("nomer", "")),
                nazvanie=item.get("title", item.get("nazvanie", "")),
                tip=tip_name,
                data_prinyatiya=item.get("date", item.get("data_prinyatiya", "")),
                sostoyanie=item.get("status", ""),
                otrysl=item.get("branch", item.get("otrysl", "")),
                kratkoe_opisanie=item.get("description", item.get("kratkoe_opisanie", "")),
                tekst_ssylka=item.get("url", item.get("tekst_ssylka", "")),
            )
        )
    return results
