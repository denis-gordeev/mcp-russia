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
    adres_url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
    parametry: dict[str, str] = {}
    if tip:
        parametry["tip"] = tip
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_normativnyy_akt(dannye)
    except Exception:
        return None


async def poluchit_zakon_proekt(nomer: str) -> ZakonProekt | None:
    """Получение законопроекта по номеру из открытых данных pravo.gov.ru.

    Аргументы:
        nomer: Номер законопроекта.

    Возвращает:
        Данные законопроекта или None.
    """
    adres_url = f"{PRAVO_DOCUMENT_URL}/{nomer}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_zakon_proekt(dannye)
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
    adres_url = PRAVO_SEARCH_URL
    parametry: dict[str, str] = {}
    if tip:
        parametry["type"] = tip
    if otrysl:
        parametry["branch"] = otrysl
    if data_from:
        parametry["dateFrom"] = data_from
    if data_to:
        parametry["dateTo"] = data_to
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _razobrat_publikatsii(dannye)
    except Exception:
        return []


async def poluchit_izmeneniya_akta(akt_nomer: str) -> list[IzmenenieAkta]:
    """Получение поправок к нормативному акту из открытых данных pravo.gov.ru.

    Аргументы:
        akt_nomer: Номер/идентификатор акта.

    Возвращает:
        Список поправок.
    """
    adres_url = f"{PRAVO_DOCUMENT_URL}/{akt_nomer}/amendments"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_izmeneniya(dannye)
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
    adres_url = PRAVO_SEARCH_URL
    parametry: dict[str, str] = {"q": tekst}
    if tip:
        parametry["type"] = tip
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        return _rezultaty_poiska(dannye)
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


def _razobrat_normativnyy_akt(dannye: Any) -> NormativnyyAkt | None:
    """Разбор ответа открытых данных pravo.gov.ru в NormativnyyAkt."""
    if not isinstance(dannye, dict):
        return None
    tip_code = str(dannye.get("type", dannye.get("tip", "")) or "")
    tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
    return NormativnyyAkt(
        nomer=dannye.get("number", dannye.get("nomer", "")) or "",
        nazvanie=dannye.get("title", dannye.get("nazvanie", "")) or "",
        tip=tip_name,
        data_prinyatiya=dannye.get("date", dannye.get("data_prinyatiya", "")) or "",
        data_publikatsii=dannye.get("publishDate", dannye.get("data_publikatsii", "")) or "",
        istochnik=dannye.get("source", dannye.get("istochnik", "pravo.gov.ru")) or "",
        sostoyanie=dannye.get("status", "") or "",
        otrysl=dannye.get("branch", dannye.get("otrysl", "")) or "",
        kratkoe_opisanie=dannye.get("description", dannye.get("kratkoe_opisanie", "")) or "",
        tekst_ssylka=dannye.get("url", dannye.get("tekst_ssylka", "")) or "",
        izmeneniya=dannye.get("amendments", dannye.get("izmeneniya", [])) or [],
    )


def _razobrat_zakon_proekt(dannye: Any) -> ZakonProekt | None:
    """Разбор ответа открытых данных pravo.gov.ru в ZakonProekt."""
    if not isinstance(dannye, dict):
        return None
    return ZakonProekt(
        nomer=dannye.get("number", dannye.get("nomer", "")) or "",
        nazvanie=dannye.get("title", dannye.get("nazvanie", "")) or "",
        stadnya=dannye.get("stage", dannye.get("stadnya", "")) or "",
        data_vneseniya=dannye.get("introducedDate", dannye.get("data_vneseniya", "")) or "",
        vnesen_subiekt=dannye.get("introducedBy", dannye.get("vnesen_subiekt", "")) or "",
        otvetstvennyy_komitet=dannye.get("committee", dannye.get("otvetstvennyy_komitet", ""))
        or "",
        chteniya=dannye.get("readings", dannye.get("chteniya", [])) or [],
        tekst_ssylka=dannye.get("url", dannye.get("tekst_ssylka", "")) or "",
    )


def _razobrat_publikatsii(dannye: Any) -> list[OficialnayaPublikatsiya]:
    """Разбор поискового ответа открытых данных pravo.gov.ru в список OficialnayaPublikatsiya."""
    elementy = dannye
    if isinstance(dannye, dict):
        elementy = dannye.get("items", dannye.get("results", dannye.get("documents", [])))
    if not isinstance(elementy, list):
        return []
    rezultaty = []
    for element in elementy:
        tip_code = str(element.get("type", element.get("tip_dokumenta", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        rezultaty.append(
            OficialnayaPublikatsiya(
                nazvanie=element.get("title", element.get("nazvanie", "")),
                tip_dokumenta=tip_name,
                data_publikatsii=element.get("publishDate", element.get("data_publikatsii", "")),
                nomer_vypuska=element.get("issueNumber", element.get("nomer_vypuska", "")),
                istochnik=element.get("source", element.get("istochnik", "pravo.gov.ru")),
                rubrika=element.get("rubric", element.get("rubrika", "")),
                annotaciya=element.get("annotation", element.get("annotaciya", "")),
                tekst_ssylka=element.get("url", element.get("tekst_ssylka", "")),
            )
        )
    return rezultaty


def _razobrat_izmeneniya(dannye: Any) -> list[IzmenenieAkta]:
    """Разбор ответа поправок открытых данных pravo.gov.ru в список IzmenenieAkta."""
    elementy = dannye
    if isinstance(dannye, dict):
        elementy = dannye.get("items", dannye.get("results", dannye.get("amendments", [])))
    if not isinstance(elementy, list):
        return []
    rezultaty = []
    for element in elementy:
        rezultaty.append(
            IzmenenieAkta(
                akt_nomer=element.get("actNumber", element.get("akt_nomer", "")),
                akt_nazvanie=element.get("actTitle", element.get("akt_nazvanie", "")),
                izmenenie_nomer=element.get("amendmentNumber", element.get("izmenenie_nomer", "")),
                izmenenie_data=element.get("amendmentDate", element.get("izmenenie_data", "")),
                izmenenie_opisanie=element.get(
                    "amendmentDescription", element.get("izmenenie_opisanie", "")
                ),
                data_vstupleniya_v_silu=element.get(
                    "effectiveDate", element.get("data_vstupleniya_v_silu", "")
                ),
                tekst_ssylka=element.get("url", element.get("tekst_ssylka", "")),
            )
        )
    return rezultaty


def _rezultaty_poiska(dannye: Any) -> list[NormativnyyAkt]:
    """Разбор результатов поиска открытых данных pravo.gov.ru в список NormativnyyAkt."""
    elementy = dannye
    if isinstance(dannye, dict):
        elementy = dannye.get("items", dannye.get("results", dannye.get("documents", [])))
    if not isinstance(elementy, list):
        return []
    rezultaty = []
    for element in elementy:
        tip_code = str(element.get("type", element.get("tip", "")))
        tip_name = TIPY_DOKUMENTOV_PRAVO.get(tip_code, tip_code)
        rezultaty.append(
            NormativnyyAkt(
                nomer=element.get("number", element.get("nomer", "")),
                nazvanie=element.get("title", element.get("nazvanie", "")),
                tip=tip_name,
                data_prinyatiya=element.get("date", element.get("data_prinyatiya", "")),
                sostoyanie=element.get("status", ""),
                otrysl=element.get("branch", element.get("otrysl", "")),
                kratkoe_opisanie=element.get("description", element.get("kratkoe_opisanie", "")),
                tekst_ssylka=element.get("url", element.get("tekst_ssylka", "")),
            )
        )
    return rezultaty
