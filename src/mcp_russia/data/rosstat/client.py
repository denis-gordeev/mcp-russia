"""HTTP-клиент для модуля Росстата / ЕМИСС.

Интеграция с реальными API:
    - ЕМИСС (fedstat.ru) для статистических показателей
    - Росстат (rosstat.gov.ru) для опубликованных данных
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    EMISS_API_BASE,
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
    emiss_code = EMISS_KODY_POKAZATELEY.get(kod, kod)
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if diapazon_dat:
            params["date"] = diapazon_dat
        data = await http_poluchit(url, params=params, timeout=20.0)
        return _razobrat_otvet_indikatora(data, kod)
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
    info_o_regionye = next((r for r in SUBIEKTY_RF if r["kod"] == kod), None)
    if not info_o_regionye:
        return None
    try:
        url = f"{EMISS_API_BASE}/region/{kod}"
        data = await http_poluchit(url, timeout=20.0)
        if isinstance(data, dict):
            return DannyeRegiona(
                kod=kod,
                nazvanie=info_o_regionye["nazvanie"],
                federalny_okrug=info_o_regionye.get("okrug", ""),
                naselenie=data.get("population"),
                vrp=data.get("gdp") or data.get("vrp"),
                srednyaya_zp=data.get("avgWage") or data.get("srednyaya_zp"),
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
    info_ob_okruge = next((o for o in FEDERALNYE_OKRUGA if o["kod"] == kod), None)
    if not info_ob_okruge:
        return {"oshibka": f"Федеральный округ '{kod}' не найден"}

    regiony = [r for r in SUBIEKTY_RF if r.get("okrug") == kod]
    return {
        "kod": kod,
        "nazvanie": info_ob_okruge["nazvanie"],
        "kolichestvo_subiektov": len(regiony),
        "subiekty": [r["nazvanie"] for r in regiony],
    }


async def poluchit_inflyaciyu(god: str = "") -> list[dict[str, Any]]:
    """Получение данных об инфляции (ИПЦ) из ЕМИСС.

    Аргументы:
        god: Фильтр по году.

    Возвращает:
        Список точек данных ИПЦ.
    """
    try:
        emiss_code = EMISS_KODY_POKAZATELEY.get("ipcz", "31088")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            elementy = data.get("data", [])
            if isinstance(elementy, list):
                return [
                    {
                        "period": element.get("date", element.get("period", "")),
                        "ipcz_mesyac": element.get("monthlyRate") or element.get("value"),
                        "ipcz_nakoplenny": element.get("cumulativeRate"),
                        "ipcz_god": element.get("yearlyRate"),
                    }
                    for element in elementy
                    if isinstance(element, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении данных об инфляции")
        return []


async def poluchit_demografiyu(subiekt: str = "") -> list[dict[str, Any]]:
    """Получение демографических данных из ЕМИСС.

    Аргументы:
        region: Код региона (необязательно).

    Возвращает:
        Список точек демографических данных.
    """
    try:
        emiss_code = EMISS_KODY_POKAZATELEY.get("naselenie", "24133")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if subiekt:
            params["region"] = subiekt
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            elementy = data.get("data", [])
            if isinstance(elementy, list):
                return [
                    {
                        "period": element.get("date", element.get("period", "")),
                        "naselenie": element.get("population") or element.get("value"),
                        "rozhdaemost": element.get("birthRate"),
                        "smertnost": element.get("deathRate"),
                        "estestvenny_prirost": element.get("naturalGrowth"),
                    }
                    for element in elementy
                    if isinstance(element, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении демографических данных")
        return []


async def poluchit_vrp(subiekt: str = "", god: str = "") -> list[VRPDannye]:
    """Получение данных о валовом региональном продукте из ЕМИСС.

    Аргументы:
        region: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных ВРП.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get("vrp", "26975")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if subiekt:
            params["region"] = subiekt
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            elementy = data.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for element in elementy:
                    if not isinstance(element, dict):
                        continue
                    region_name = ""
                    reg_code = element.get("region", subiekt)
                    if reg_code:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    rezultaty.append(
                        VRPDannye(
                            period=element.get("date", element.get("period", "")),
                            subiekt=region_name,
                            vrp=element.get("value"),
                            vrp_na_dushu=element.get("perCapita"),
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
        region: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных о заработной плате.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get("zarplata", "24140")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if subiekt:
            params["region"] = subiekt
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            elementy = data.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for element in elementy:
                    if not isinstance(element, dict):
                        continue
                    region_name = ""
                    reg_code = element.get("region", subiekt)
                    if reg_code:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    rezultaty.append(
                        DannyeZarplaty(
                            period=element.get("date", element.get("period", "")),
                            subiekt=region_name,
                            nominalnaya_zp=element.get("value"),
                            realnaya_zp_izmenenie=element.get("realChange"),
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
    emiss_code = REGIONALNYE_POKAZATELI.get(pokazatel)
    if not emiss_code:
        return []
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        data = await http_poluchit(url, params={"groupByRegion": "true"}, timeout=20.0)
        if isinstance(data, dict):
            elementy = data.get("data", [])
            if isinstance(elementy, list):
                rezultaty = []
                for element in elementy:
                    if not isinstance(element, dict):
                        continue
                    region_code = str(element.get("region", element.get("okato", "")))
                    region_name = element.get("regionName", "")
                    if not region_name:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == region_code), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    rezultaty.append(
                        {
                            "subiekt": region_name,
                            "kod": region_code,
                            "znachenie": element.get("value"),
                            "period": element.get("date", element.get("period", "")),
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
        region: Код региона для фильтрации (необязательно).
        god: Фильтр по году (необязательно).

    Возвращает:
        Список точек данных показателя.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get(kod, kod)
    imya_indikatora = next(
        (p["nazvanie"] for p in KLYUCHEVYE_INDIKATORY if p["kod"] == kod),
        "",
    )
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if subiekt:
            params["region"] = subiekt
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return []
        elementy = data.get("data", [])
        if not isinstance(elementy, list):
            return []
        rezultaty = []
        for element in elementy:
            if not isinstance(element, dict):
                continue
            region_name = ""
            reg_code = element.get("region", subiekt)
            if reg_code:
                ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                if ri:
                    region_name = ri["nazvanie"]
            rezultaty.append(
                IndikatorDannye(
                    kod_emiss=emiss_code,
                    nazvanie=imya_indikatora or element.get("name", kod),
                    period=element.get("date", element.get("period", "")),
                    znachenie=element.get("value"),
                    edinitsa=element.get("unit", ""),
                    subiekt=region_name,
                )
            )
        return rezultaty
    except Exception:
        logger.exception("Ошибка при получении данных индикатора %s", kod)
        return []


def _razobrat_otvet_indikatora(data: Any, code: str) -> list[PokazatelRosstata]:
    """Разбор ответа API ЕМИСС в объекты PokazatelRosstata."""
    if not isinstance(data, dict):
        return []

    elementy = data.get("data", [])
    if not isinstance(elementy, list):
        return []

    rezultaty = []
    for element in elementy:
        if not isinstance(element, dict):
            continue
        try:
            rezultaty.append(
                PokazatelRosstata(
                    kod=code,
                    nazvanie=element.get("name", code),
                    znachenie=float(element.get("value", 0)),
                    edinitsa=element.get("unit", ""),
                    data=element.get("date", ""),
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
        region: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных отраслевой структуры.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get("struktura_vrp", "27103")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if subiekt:
            params["region"] = subiekt
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _rezerv_otraslevaya_struktura(subiekt, god)
        elementy = data.get("data", [])
        if not isinstance(elementy, list) or not elementy:
            return _rezerv_otraslevaya_struktura(subiekt, god)
        region_name = ""
        if subiekt:
            ri = next((r for r in SUBIEKTY_RF if r["kod"] == subiekt), None)
            if ri:
                region_name = ri["nazvanie"]
        rezultaty = []
        for element in elementy:
            if not isinstance(element, dict):
                continue
            okved = element.get("okved", element.get("code", ""))
            otrasl = next(
                (o["nazvanie"] for o in OTRASLEVAYA_STRUKTURA_VRP if o["kod"] == okved),
                element.get("name", okved),
            )
            rezultaty.append(
                OtraslevayaStrukturaVRP(
                    subiekt=region_name or element.get("regionName", ""),
                    period=element.get("date", element.get("period", god or "")),
                    otrasl=otrasl,
                    kod_okved=okved,
                    dolya_vvp=element.get("share") or element.get("dolya"),
                    vrp=element.get("value"),
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
    region_name = ""
    if subiekt:
        ri = next((r for r in SUBIEKTY_RF if r["kod"] == subiekt), None)
        if ri:
            region_name = ri["nazvanie"]
    return [
        OtraslevayaStrukturaVRP(
            subiekt=region_name,
            period=god or "2022",
            otrasl=o["nazvanie"],
            kod_okved=o["kod"],
            dolya_vvp=o.get("dolya_2022"),
            vrp=o.get("vrp_2022"),
        )
        for o in OTRASLEVAYA_STRUKTURA_VRP
    ]


async def poluchit_investitsii_po_vidam(
    subiekt: str = "",
    god: str = "",
) -> list[InvestitsiiPoVidam]:
    """Получение данных об инвестициях по видам экономической деятельности.

    Аргументы:
        region: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных об инвестициях по видам деятельности.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get("investitsii_po_vidam", "24145")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {"groupByActivity": "true"}
        if subiekt:
            params["region"] = subiekt
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _rezerv_investitsii_po_vidam(subiekt, god)
        elementy = data.get("data", [])
        if not isinstance(elementy, list) or not elementy:
            return _rezerv_investitsii_po_vidam(subiekt, god)
        region_name = ""
        if subiekt:
            ri = next((r for r in SUBIEKTY_RF if r["kod"] == subiekt), None)
            if ri:
                region_name = ri["nazvanie"]
        rezultaty = []
        for element in elementy:
            if not isinstance(element, dict):
                continue
            okved = element.get("okved", element.get("activityCode", ""))
            vid = next(
                (v["nazvanie"] for v in VIDY_DEYATELNOSTI_INVESTITSII if v["kod"] == okved),
                element.get("activityName", element.get("name", okved)),
            )
            rezultaty.append(
                InvestitsiiPoVidam(
                    subiekt=region_name or element.get("regionName", ""),
                    period=element.get("date", element.get("period", god or "")),
                    vid_deyatelnosti=vid,
                    kod_okved=okved,
                    investitsii=element.get("value"),
                    dolya=element.get("share") or element.get("dolya"),
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
    region_name = ""
    if subiekt:
        ri = next((r for r in SUBIEKTY_RF if r["kod"] == subiekt), None)
        if ri:
            region_name = ri["nazvanie"]
    return [
        InvestitsiiPoVidam(
            subiekt=region_name,
            period=god or "2022",
            vid_deyatelnosti=v["nazvanie"],
            kod_okved=v["kod"],
            investitsii=v.get("inv_2022"),
            dolya=v.get("dolya_2022"),
        )
        for v in VIDY_DEYATELNOSTI_INVESTITSII
    ]
