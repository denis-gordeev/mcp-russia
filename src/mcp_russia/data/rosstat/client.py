"""HTTP-клиент для модуля Росстата / ЕМИСС.

Интеграция с реальными API:
    - ЕМИСС (fedstat.ru) для статистических показателей
    - Росстат (rosstat.gov.ru) для опубликованных данных
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit
from mcp_russia._shared.normalizatsiya import (
    bezopasnaya_stroka,
    bezopasnoe_chislo,
)

from .constants import (
    EMISS_BAZA_API,
    EMISS_KODY_POKAZATELEY,
    FEDERALNYE_OKRUGA,
    KLYUCHEVYE_INDIKATORY,
    OTRASLEVAYA_STRUKTURA_VRP,
    REGIONALNYE_POKAZATELI,
    SUBIEKTY_RF,
    VIDY_DEYATELNOSTI_INVESTITSII,
)
from .schemas import (
    DannyeRegiona,
    DannyeZarplaty,
    IndikatorDannye,
    InvestitsiiPoVidam,
    OtraslevayaStrukturaVRP,
    PokazatelRosstata,
    VRPDannye,
)

logger = logging.getLogger(__name__)


async def poluchit_indikator(kod: str, diapazon_dat: str = "") -> list[PokazatelRosstata]:
    """Получение статистического показателя из ЕМИСС/Росстата.

    Аргументы:
        kod: Код показателя (напр. 'ipcz', 'naselenie').
        diapazon_dat: Фильтр по диапазону дат (необязательно).

    Возвращает:
        Список значений показателя.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get(kod, kod)
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if diapazon_dat:
            parametry["date"] = diapazon_dat
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        return _razobrat_otvet_indikatora(dannye, kod)
    except Exception:
        logger.exception("Ошибка при получении индикатора %s", kod)
        return []


async def poluchit_dannye_regiona(kod: str) -> DannyeRegiona | None:
    """Получение данных о субъекте РФ.

    Аргументы:
        kod: Код региона (ОКАТО/ОКТМО).

    Возвращает:
        Данные региона или None.
    """
    info_o_regionye = next(
        (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == kod), None
    )
    if not info_o_regionye:
        return None
    try:
        adres_url = f"{EMISS_BAZA_API}/region/{kod}"
        dannye = await http_poluchit(adres_url, taimaut=20.0)
        if isinstance(dannye, dict):
            return DannyeRegiona(
                kod=kod,
                nazvanie=info_o_regionye["nazvanie"],
                federalny_okrug=info_o_regionye.get("okrug", ""),
                naselenie=dannye.get("population"),
                vrp=dannye.get("gdp") or dannye.get("vrp"),
                srednyaya_zp=dannye.get("avgWage") or dannye.get("srednyaya_zp"),
            )
    except Exception:
        logger.exception("Ошибка при получении данных региона %s", kod)

    return DannyeRegiona(
        kod=kod,
        nazvanie=info_o_regionye["nazvanie"],
        federalny_okrug=info_o_regionye.get("okrug", ""),
    )


async def poluchit_federalny_okrug(kod: str) -> dict[str, Any]:
    """Получение данных о федеральном округе.

    Аргументы:
        kod: Код федерального округа.

    Возвращает:
        Данные федерального округа.
    """
    info_ob_okruge = next((okrug for okrug in FEDERALNYE_OKRUGA if okrug["kod"] == kod), None)
    if not info_ob_okruge:
        return {"oshibka": f"Федеральный округ '{kod}' не найден"}

    regiony = [subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf.get("okrug") == kod]
    return {
        "kod": kod,
        "nazvanie": info_ob_okruge["nazvanie"],
        "kolichestvo_subiektov": len(regiony),
        "subiekty": [subiekt_rf["nazvanie"] for subiekt_rf in regiony],
    }


async def poluchit_inflyatsiyu(god: str = "") -> list[dict[str, Any]]:
    """Получение данных об инфляции (ИПЦ) из ЕМИСС.

    Аргументы:
        god: Фильтр по году.

    Возвращает:
        Список точек данных ИПЦ.
    """
    try:
        kod_emiss = EMISS_KODY_POKAZATELEY.get("ipcz", "31088")
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", [])
            if isinstance(elementy, list):
                return [
                    {
                        "period": zapis.get("date", zapis.get("period", "")),
                        "ipcz_mesyac": zapis.get("monthlyRate") or zapis.get("value"),
                        "ipcz_nakoplenny": zapis.get("cumulativeRate"),
                        "ipcz_god": zapis.get("yearlyRate"),
                    }
                    for zapis in elementy
                    if isinstance(zapis, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении данных об инфляции")
        return []


async def poluchit_demografiyu(subiekt: str = "") -> list[dict[str, Any]]:
    """Получение демографических данных из ЕМИСС.

    Аргументы:
        subiekt: Код региона (необязательно).

    Возвращает:
        Список точек демографических данных.
    """
    try:
        kod_emiss = EMISS_KODY_POKAZATELEY.get("naselenie", "24133")
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", [])
            if isinstance(elementy, list):
                return [
                    {
                        "period": zapis.get("date", zapis.get("period", "")),
                        "naselenie": zapis.get("population") or zapis.get("value"),
                        "rozhdaemost": zapis.get("birthRate"),
                        "smertnost": zapis.get("deathRate"),
                        "estestvenny_prirost": zapis.get("naturalGrowth"),
                    }
                    for zapis in elementy
                    if isinstance(zapis, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении демографических данных")
        return []


async def poluchit_vrp(subiekt: str = "", god: str = "") -> list[VRPDannye]:
    """Получение данных о валовом региональном продукте из ЕМИСС.

    Аргументы:
        subiekt: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных ВРП.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get("vrp", "26975")
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for zapis in elementy:
                    if not isinstance(zapis, dict):
                        continue
                    nazvanie_subiekta = ""
                    kod_reg = zapis.get("region", subiekt)
                    if kod_reg:
                        info_subiekta = next(
                            (
                                subiekt_rf
                                for subiekt_rf in SUBIEKTY_RF
                                if subiekt_rf["kod"] == str(kod_reg)
                            ),
                            None,
                        )
                        if info_subiekta:
                            nazvanie_subiekta = info_subiekta["nazvanie"]
                    rezultaty.append(
                        VRPDannye(
                            period=bezopasnaya_stroka(zapis.get("date", zapis.get("period", ""))),
                            subiekt=nazvanie_subiekta,
                            vrp=bezopasnoe_chislo(zapis.get("value")),
                            vrp_na_dushu=bezopasnoe_chislo(zapis.get("perCapita")),
                        )
                    )
                return rezultaty
        return []
    except Exception:
        logger.exception("Ошибка при получении данных о ВРП")
        return []


async def poluchit_zarplatu(subiekt: str = "", god: str = "") -> list[DannyeZarplaty]:
    """Получение данных о заработной плате из ЕМИСС.

    Аргументы:
        subiekt: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных о заработной плате.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get("zarplata", "24140")
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for zapis in elementy:
                    if not isinstance(zapis, dict):
                        continue
                    nazvanie_subiekta = ""
                    kod_reg = zapis.get("region", subiekt)
                    if kod_reg:
                        info_subiekta = next(
                            (
                                subiekt_rf
                                for subiekt_rf in SUBIEKTY_RF
                                if subiekt_rf["kod"] == str(kod_reg)
                            ),
                            None,
                        )
                        if info_subiekta:
                            nazvanie_subiekta = info_subiekta["nazvanie"]
                    rezultaty.append(
                        DannyeZarplaty(
                            period=bezopasnaya_stroka(zapis.get("date", zapis.get("period", ""))),
                            subiekt=nazvanie_subiekta,
                            nominalnaya_zp=bezopasnoe_chislo(zapis.get("value")),
                            realnaya_zp_izmenenie=bezopasnoe_chislo(zapis.get("realChange")),
                        )
                    )
                return rezultaty
        return []
    except Exception:
        logger.exception("Ошибка при получении данных о заработной плате")
        return []


async def poluchit_sravnenie_regionov(pokazatel: str) -> list[dict[str, Any]]:
    """Получение регионального показателя по всем регионам для сравнения.

    Аргументы:
        pokazatel: Код показателя из REGIONALNYE_POKAZATELI.

    Возвращает:
        Список пар «регион — значение».
    """
    kod_emiss = REGIONALNYE_POKAZATELI.get(pokazatel)
    if not kod_emiss:
        return []
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        dannye = await http_poluchit(adres_url, parametry={"groupByRegion": "true"}, taimaut=20.0)
        if isinstance(dannye, dict):
            elementy = dannye.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for zapis in elementy:
                    if not isinstance(zapis, dict):
                        continue
                    kod_subiekta = str(zapis.get("region", zapis.get("okato", "")))
                    nazvanie_subiekta = zapis.get("regionName", "")
                    if not nazvanie_subiekta:
                        info_subiekta = next(
                            (
                                subiekt_rf
                                for subiekt_rf in SUBIEKTY_RF
                                if subiekt_rf["kod"] == kod_subiekta
                            ),
                            None,
                        )
                        if info_subiekta:
                            nazvanie_subiekta = info_subiekta["nazvanie"]
                    rezultaty.append(
                        {
                            "subiekt": nazvanie_subiekta,
                            "kod": kod_subiekta,
                            "znachenie": zapis.get("value"),
                            "period": zapis.get("date", zapis.get("period", "")),
                        }
                    )
                return rezultaty
        return []
    except Exception:
        logger.exception("Ошибка при получении сравнения регионов по показателю %s", pokazatel)
        return []


async def poluchit_indikator_dannye(
    kod: str,
    subiekt: str = "",
    god: str = "",
) -> list[IndikatorDannye]:
    """Получение данных произвольного показателя по коду ЕМИСС или мнемоническому коду.

    Аргументы:
        kod: Код ЕМИСС (напр. '31088') или мнемонический код (напр. 'ipcz').
        subiekt: Код региона для фильтрации (необязательно).
        god: Фильтр по году (необязательно).

    Возвращает:
        Список точек данных показателя.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get(kod, kod)
    imya_indikatora = next(
        (pokazatel["nazvanie"] for pokazatel in KLYUCHEVYE_INDIKATORY if pokazatel["kod"] == kod),
        "",
    )
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if not isinstance(dannye, dict):
            return []
        elementy = dannye.get("data", [])
        if not isinstance(elementy, list):
            return []
        rezultaty = []
        for zapis in elementy:
            if not isinstance(zapis, dict):
                continue
            nazvanie_subiekta = ""
            kod_reg = zapis.get("region", subiekt)
            if kod_reg:
                info_subiekta = next(
                    (
                        subiekt_rf
                        for subiekt_rf in SUBIEKTY_RF
                        if subiekt_rf["kod"] == str(kod_reg)
                    ),
                    None,
                )
                if info_subiekta:
                    nazvanie_subiekta = info_subiekta["nazvanie"]
            rezultaty.append(
                IndikatorDannye(
                    kod_emiss=kod_emiss,
                    nazvanie=imya_indikatora or bezopasnaya_stroka(zapis.get("name"), kod),
                    period=bezopasnaya_stroka(zapis.get("date", zapis.get("period", ""))),
                    znachenie=bezopasnoe_chislo(zapis.get("value")),
                    edinitsa=bezopasnaya_stroka(zapis.get("unit")),
                    subiekt=nazvanie_subiekta,
                )
            )
        return rezultaty
    except Exception:
        logger.exception("Ошибка при получении данных индикатора %s", kod)
        return []


def _razobrat_otvet_indikatora(dannye: Any, kod: str) -> list[PokazatelRosstata]:
    """Разбор ответа API ЕМИСС в объекты PokazatelRosstata."""
    if not isinstance(dannye, dict):
        return []

    elementy = dannye.get("data", [])
    if not isinstance(elementy, list):
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        try:
            rezultaty.append(
                PokazatelRosstata(
                    kod=kod,
                    nazvanie=zapis.get("name", kod),
                    znachenie=float(zapis.get("value", 0)),
                    edinitsa=zapis.get("unit", ""),
                    data=zapis.get("date", ""),
                )
            )
        except (ValueError, TypeError):
            continue
    return rezultaty


def poluchit_spisok_subiektov() -> list[dict[str, str]]:
    """Возвращает список субъектов РФ, доступных для запросов."""
    return SUBIEKTY_RF


def poluchit_spisok_federalnykh_okrugov() -> list[dict[str, str]]:
    """Возвращает список федеральных округов, доступных для запросов."""
    return FEDERALNYE_OKRUGA


async def poluchit_otraslevuyu_strukturu_vrp(
    subiekt: str = "",
    god: str = "",
) -> list[OtraslevayaStrukturaVRP]:
    """Получение отраслевой структуры ВРП по разделам ОКВЭД.

    Аргументы:
        subiekt: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных отраслевой структуры.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get("struktura_vrp", "27103")
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if not isinstance(dannye, dict):
            return _rezerv_otraslevaya_struktura(subiekt, god)
        elementy = dannye.get("data", [])
        if not isinstance(elementy, list) or not elementy:
            return _rezerv_otraslevaya_struktura(subiekt, god)
        nazvanie_subiekta = ""
        if subiekt:
            info_subiekta = next(
                (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == subiekt), None
            )
            if info_subiekta:
                nazvanie_subiekta = info_subiekta["nazvanie"]
        rezultaty = []
        for zapis in elementy:
            if not isinstance(zapis, dict):
                continue
            znachenie_okved = zapis.get("znachenie_okved", zapis.get("code", ""))
            otrasl = next(
                (
                    otrasl["nazvanie"]
                    for otrasl in OTRASLEVAYA_STRUKTURA_VRP
                    if otrasl["kod"] == znachenie_okved
                ),
                zapis.get("name", znachenie_okved),
            )
            rezultaty.append(
                OtraslevayaStrukturaVRP(
                    subiekt=nazvanie_subiekta or bezopasnaya_stroka(zapis.get("regionName")),
                    period=bezopasnaya_stroka(zapis.get("date", zapis.get("period", god or ""))),
                    otrasl=bezopasnaya_stroka(otrasl),
                    kod_okved=bezopasnaya_stroka(znachenie_okved),
                    dolya_vvp=bezopasnoe_chislo(zapis.get("share") or zapis.get("dolya")),
                    vrp=bezopasnoe_chislo(zapis.get("value")),
                )
            )
        return rezultaty
    except Exception:
        logger.exception("Ошибка при получении отраслевой структуры ВРП")
        return _rezerv_otraslevaya_struktura(subiekt, god)


def _rezerv_otraslevaya_struktura(
    subiekt: str = "",
    god: str = "",
) -> list[OtraslevayaStrukturaVRP]:
    """Возврат справочных данных об отраслевой структуре как резервный вариант.

    Использует опубликованные данные Росстата за 2022 год при недоступности API.
    """
    nazvanie_subiekta = ""
    if subiekt:
        info_subiekta = next(
            (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == subiekt), None
        )
        if info_subiekta:
            nazvanie_subiekta = info_subiekta["nazvanie"]
    return [
        OtraslevayaStrukturaVRP(
            subiekt=nazvanie_subiekta,
            period=god or "2022",
            otrasl=bezopasnaya_stroka(otrasl["nazvanie"]),
            kod_okved=bezopasnaya_stroka(otrasl["kod"]),
            dolya_vvp=bezopasnoe_chislo(otrasl.get("dolya_2022")),
            vrp=bezopasnoe_chislo(otrasl.get("vrp_2022")),
        )
        for otrasl in OTRASLEVAYA_STRUKTURA_VRP
    ]


async def poluchit_investitsii_po_vidam(
    subiekt: str = "",
    god: str = "",
) -> list[InvestitsiiPoVidam]:
    """Получение данных об инвестициях по видам экономической деятельности.

    Аргументы:
        subiekt: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных об инвестициях по видам деятельности.
    """
    kod_emiss = EMISS_KODY_POKAZATELEY.get("investitsii_po_vidam", "24145")
    try:
        adres_url = f"{EMISS_BAZA_API}/data/{kod_emiss}"
        parametry: dict[str, str] = {"groupByActivity": "true"}
        if subiekt:
            parametry["region"] = subiekt
        if god:
            parametry["year"] = god
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=20.0)
        if not isinstance(dannye, dict):
            return _rezerv_investitsii_po_vidam(subiekt, god)
        elementy = dannye.get("data", [])
        if not isinstance(elementy, list) or not elementy:
            return _rezerv_investitsii_po_vidam(subiekt, god)
        nazvanie_subiekta = ""
        if subiekt:
            info_subiekta = next(
                (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == subiekt), None
            )
            if info_subiekta:
                nazvanie_subiekta = info_subiekta["nazvanie"]
        rezultaty = []
        for zapis in elementy:
            if not isinstance(zapis, dict):
                continue
            znachenie_okved = zapis.get("znachenie_okved", zapis.get("activityCode", ""))
            vid = next(
                (
                    vid_deyatelnosti["nazvanie"]
                    for vid_deyatelnosti in VIDY_DEYATELNOSTI_INVESTITSII
                    if vid_deyatelnosti["kod"] == znachenie_okved
                ),
                zapis.get("activityName", zapis.get("name", znachenie_okved)),
            )
            rezultaty.append(
                InvestitsiiPoVidam(
                    subiekt=nazvanie_subiekta or bezopasnaya_stroka(zapis.get("regionName")),
                    period=bezopasnaya_stroka(zapis.get("date", zapis.get("period", god or ""))),
                    vid_deyatelnosti=bezopasnaya_stroka(vid),
                    kod_okved=bezopasnaya_stroka(znachenie_okved),
                    investitsii=bezopasnoe_chislo(zapis.get("value")),
                    dolya=bezopasnoe_chislo(zapis.get("share") or zapis.get("dolya")),
                )
            )
        return rezultaty
    except Exception:
        logger.exception("Ошибка при получении инвестиций по видам деятельности")
        return _rezerv_investitsii_po_vidam(subiekt, god)


def _rezerv_investitsii_po_vidam(
    subiekt: str = "",
    god: str = "",
) -> list[InvestitsiiPoVidam]:
    """Возврат справочных данных об инвестиционной деятельности как резервный вариант.

    Использует опубликованные данные Росстата за 2022 год при недоступности API.
    """
    nazvanie_subiekta = ""
    if subiekt:
        info_subiekta = next(
            (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == subiekt), None
        )
        if info_subiekta:
            nazvanie_subiekta = info_subiekta["nazvanie"]
    return [
        InvestitsiiPoVidam(
            subiekt=nazvanie_subiekta,
            period=god or "2022",
            vid_deyatelnosti=bezopasnaya_stroka(vid["nazvanie"]),
            kod_okved=bezopasnaya_stroka(vid["kod"]),
            investitsii=bezopasnoe_chislo(vid.get("inv_2022")),
            dolya=bezopasnoe_chislo(vid.get("dolya_2022")),
        )
        for vid in VIDY_DEYATELNOSTI_INVESTITSII
    ]
