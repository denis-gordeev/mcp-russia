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
    PRAVO_ADRES_DOKUMENTA,
    PRAVO_ADRES_POISKA,
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
    adres_url = f"{PRAVO_ADRES_DOKUMENTA}/{nomer}"
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
    adres_url = f"{PRAVO_ADRES_DOKUMENTA}/{nomer}"
    try:
        dannye = await http_poluchit(adres_url)
        return _razobrat_zakon_proekt(dannye)
    except Exception:
        return None


async def poluchit_publikatsii(
    tip: str = "",
    otrasl: str = "",
    data_s: str = "",
    data_po: str = "",
) -> list[OficialnayaPublikatsiya]:
    """Поиск официальных публикаций через открытые данные pravo.gov.ru.

    Аргументы:
        tip: Фильтр по типу документа (код типа pravo.gov.ru).
        otrasl: Фильтр по отрасли права.
        data_s: Фильтр по начальной дате (ГГГГ-ММ-ДД).
        data_po: Фильтр по конечной дате (ГГГГ-ММ-ДД).

    Возвращает:
        Список публикаций.
    """
    adres_url = PRAVO_ADRES_POISKA
    parametry: dict[str, str] = {}
    if tip:
        parametry["type"] = tip
    if otrasl:
        parametry["branch"] = otrasl
    if data_s:
        parametry["dateFrom"] = data_s
    if data_po:
        parametry["dateTo"] = data_po
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
    adres_url = f"{PRAVO_ADRES_DOKUMENTA}/{akt_nomer}/amendments"
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
    adres_url = PRAVO_ADRES_POISKA
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
    kod_tipa = str(dannye.get("type", dannye.get("tip", "")) or "")
    nazvanie_tipa = TIPY_DOKUMENTOV_PRAVO.get(kod_tipa, kod_tipa)
    return NormativnyyAkt(
        nomer=dannye.get("number", dannye.get("nomer", "")) or "",
        nazvanie=dannye.get("title", dannye.get("nazvanie", "")) or "",
        tip=nazvanie_tipa,
        data_prinyatiya=dannye.get("date", dannye.get("data_prinyatiya", "")) or "",
        data_publikatsii=dannye.get("publishDate", dannye.get("data_publikatsii", "")) or "",
        istochnik=dannye.get("source", dannye.get("istochnik", "pravo.gov.ru")) or "",
        sostoyanie=dannye.get("status", "") or "",
        otrasl=dannye.get("branch", dannye.get("otrasl", "")) or "",
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
    for zapis in elementy:
        kod_tipa = str(zapis.get("type", zapis.get("tip_dokumenta", "")))
        nazvanie_tipa = TIPY_DOKUMENTOV_PRAVO.get(kod_tipa, kod_tipa)
        rezultaty.append(
            OficialnayaPublikatsiya(
                nazvanie=zapis.get("title", zapis.get("nazvanie", "")),
                tip_dokumenta=nazvanie_tipa,
                data_publikatsii=zapis.get("publishDate", zapis.get("data_publikatsii", "")),
                nomer_vypuska=zapis.get("issueNumber", zapis.get("nomer_vypuska", "")),
                istochnik=zapis.get("source", zapis.get("istochnik", "pravo.gov.ru")),
                rubrika=zapis.get("rubric", zapis.get("rubrika", "")),
                annotaciya=zapis.get("annotation", zapis.get("annotaciya", "")),
                tekst_ssylka=zapis.get("url", zapis.get("tekst_ssylka", "")),
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
    for zapis in elementy:
        rezultaty.append(
            IzmenenieAkta(
                akt_nomer=zapis.get("actNumber", zapis.get("akt_nomer", "")),
                akt_nazvanie=zapis.get("actTitle", zapis.get("akt_nazvanie", "")),
                izmenenie_nomer=zapis.get("amendmentNumber", zapis.get("izmenenie_nomer", "")),
                izmenenie_data=zapis.get("amendmentDate", zapis.get("izmenenie_data", "")),
                izmenenie_opisanie=zapis.get(
                    "amendmentDescription", zapis.get("izmenenie_opisanie", "")
                ),
                data_vstupleniya_v_silu=zapis.get(
                    "effectiveDate", zapis.get("data_vstupleniya_v_silu", "")
                ),
                tekst_ssylka=zapis.get("url", zapis.get("tekst_ssylka", "")),
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
    for zapis in elementy:
        kod_tipa = str(zapis.get("type", zapis.get("tip", "")))
        nazvanie_tipa = TIPY_DOKUMENTOV_PRAVO.get(kod_tipa, kod_tipa)
        rezultaty.append(
            NormativnyyAkt(
                nomer=zapis.get("number", zapis.get("nomer", "")),
                nazvanie=zapis.get("title", zapis.get("nazvanie", "")),
                tip=nazvanie_tipa,
                data_prinyatiya=zapis.get("date", zapis.get("data_prinyatiya", "")),
                sostoyanie=zapis.get("status", ""),
                otrasl=zapis.get("branch", zapis.get("otrasl", "")),
                kratkoe_opisanie=zapis.get("description", zapis.get("kratkoe_opisanie", "")),
                tekst_ssylka=zapis.get("url", zapis.get("tekst_ssylka", "")),
            )
        )
    return rezultaty
