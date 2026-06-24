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
    VRPData,
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
        return {"error": f"Федеральный округ '{kod}' не найден"}

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
            items = data.get("data", [])
            if isinstance(items, list):
                return [
                    {
                        "period": item.get("date", item.get("period", "")),
                        "ipcz_mesyac": item.get("monthlyRate") or item.get("value"),
                        "ipcz_nakoplenny": item.get("cumulativeRate"),
                        "ipcz_god": item.get("yearlyRate"),
                    }
                    for item in items
                    if isinstance(item, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении данных об инфляции")
        return []


async def poluchit_demografiyu(region: str = "") -> list[dict[str, Any]]:
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
        if region:
            params["region"] = region
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            items = data.get("data", [])
            if isinstance(items, list):
                return [
                    {
                        "period": item.get("date", item.get("period", "")),
                        "naselenie": item.get("population") or item.get("value"),
                        "rozhdaemost": item.get("birthRate"),
                        "smertnost": item.get("deathRate"),
                        "estestvenny_prirost": item.get("naturalGrowth"),
                    }
                    for item in items
                    if isinstance(item, dict)
                ]
        return []
    except Exception:
        logger.exception("Ошибка при получении демографических данных")
        return []


async def poluchit_vrp(region: str = "", god: str = "") -> list[VRPData]:
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
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            items = data.get("data", [])
            if isinstance(items, list):
                results = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    region_name = ""
                    reg_code = item.get("region", region)
                    if reg_code:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    results.append(
                        VRPData(
                            period=item.get("date", item.get("period", "")),
                            region=region_name,
                            vrp=item.get("value"),
                            vrp_na_dushu=item.get("perCapita"),
                        )
                    )
                return results
        return []
    except Exception:
        logger.exception("Ошибка при получении данных о ВРП")
        return []


async def poluchit_zarplatu(region: str = "", god: str = "") -> list[DannyeZarplaty]:
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
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if isinstance(data, dict):
            items = data.get("data", [])
            if isinstance(items, list):
                results = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    region_name = ""
                    reg_code = item.get("region", region)
                    if reg_code:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    results.append(
                        DannyeZarplaty(
                            period=item.get("date", item.get("period", "")),
                            region=region_name,
                            nominalnaya_zp=item.get("value"),
                            realnaya_zp_change=item.get("realChange"),
                        )
                    )
                return results
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
            items = data.get("data", [])
            if isinstance(items, list):
                results = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    region_code = str(item.get("region", item.get("okato", "")))
                    region_name = item.get("regionName", "")
                    if not region_name:
                        ri = next((r for r in SUBIEKTY_RF if r["kod"] == region_code), None)
                        if ri:
                            region_name = ri["nazvanie"]
                    results.append(
                        {
                            "region": region_name,
                            "kod": region_code,
                            "znachenie": item.get("value"),
                            "period": item.get("date", item.get("period", "")),
                        }
                    )
                return results
        return []
    except Exception:
        logger.exception("Ошибка при получении сравнения регионов по показателю %s", pokazatel)
        return []


async def poluchit_indikator_dannye(
    kod: str,
    region: str = "",
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
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return []
        items = data.get("data", [])
        if not isinstance(items, list):
            return []
        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            region_name = ""
            reg_code = item.get("region", region)
            if reg_code:
                ri = next((r for r in SUBIEKTY_RF if r["kod"] == str(reg_code)), None)
                if ri:
                    region_name = ri["nazvanie"]
            results.append(
                IndikatorDannye(
                    kod_emiss=emiss_code,
                    nazvanie=imya_indikatora or item.get("name", kod),
                    period=item.get("date", item.get("period", "")),
                    znachenie=item.get("value"),
                    edinitsa=item.get("unit", ""),
                    region=region_name,
                )
            )
        return results
    except Exception:
        logger.exception("Ошибка при получении данных индикатора %s", kod)
        return []


def _razobrat_otvet_indikatora(data: Any, code: str) -> list[PokazatelRosstata]:
    """Разбор ответа API ЕМИСС в объекты PokazatelRosstata."""
    if not isinstance(data, dict):
        return []

    items = data.get("data", [])
    if not isinstance(items, list):
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            results.append(
                PokazatelRosstata(
                    kod=code,
                    nazvanie=item.get("name", code),
                    znachenie=float(item.get("value", 0)),
                    edinitsa=item.get("unit", ""),
                    data=item.get("date", ""),
                )
            )
        except (ValueError, TypeError):
            continue
    return results


def poluchit_spisok_subiektov() -> list[dict[str, str]]:
    """Возвращает список субъектов РФ, доступных для запросов."""
    return SUBIEKTY_RF


def poluchit_spisok_federalnykh_okrugov() -> list[dict[str, str]]:
    """Возвращает список федеральных округов, доступных для запросов."""
    return FEDERALNYE_OKRUGA


async def poluchit_otraslevuyu_strukturu_vrp(
    region: str = "",
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
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _fallback_otraslevaya_struktura(region, god)
        items = data.get("data", [])
        if not isinstance(items, list) or not items:
            return _fallback_otraslevaya_struktura(region, god)
        region_name = ""
        if region:
            ri = next((r for r in SUBIEKTY_RF if r["kod"] == region), None)
            if ri:
                region_name = ri["nazvanie"]
        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            okved = item.get("okved", item.get("code", ""))
            otrasl = next(
                (o["nazvanie"] for o in OTRASLEVAYA_STRUKTURA_VRP if o["kod"] == okved),
                item.get("name", okved),
            )
            results.append(
                OtraslevayaStrukturaVRP(
                    region=region_name or item.get("regionName", ""),
                    period=item.get("date", item.get("period", god or "")),
                    otrasl=otrasl,
                    kod_okved=okved,
                    dolya_vvp=item.get("share") or item.get("dolya"),
                    vrp=item.get("value"),
                )
            )
        return results
    except Exception:
        logger.exception("Ошибка при получении отраслевой структуры ВРП")
        return _fallback_otraslevaya_struktura(region, god)


def _fallback_otraslevaya_struktura(
    region: str = "",
    god: str = "",
) -> list[OtraslevayaStrukturaVRP]:
    """Возврат справочных данных об отраслевой структуре как резервный вариант.

    Использует опубликованные данные Росстата за 2022 год при недоступности API.
    """
    region_name = ""
    if region:
        ri = next((r for r in SUBIEKTY_RF if r["kod"] == region), None)
        if ri:
            region_name = ri["nazvanie"]
    return [
        OtraslevayaStrukturaVRP(
            region=region_name,
            period=god or "2022",
            otrasl=o["nazvanie"],
            kod_okved=o["kod"],
            dolya_vvp=o.get("dolya_2022"),
            vrp=o.get("vrp_2022"),
        )
        for o in OTRASLEVAYA_STRUKTURA_VRP
    ]


async def poluchit_investitsii_po_vidam(
    region: str = "",
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
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_poluchit(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _fallback_investitsii_po_vidam(region, god)
        items = data.get("data", [])
        if not isinstance(items, list) or not items:
            return _fallback_investitsii_po_vidam(region, god)
        region_name = ""
        if region:
            ri = next((r for r in SUBIEKTY_RF if r["kod"] == region), None)
            if ri:
                region_name = ri["nazvanie"]
        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            okved = item.get("okved", item.get("activityCode", ""))
            vid = next(
                (v["nazvanie"] for v in VIDY_DEYATELNOSTI_INVESTITSII if v["kod"] == okved),
                item.get("activityName", item.get("name", okved)),
            )
            results.append(
                InvestitsiiPoVidam(
                    region=region_name or item.get("regionName", ""),
                    period=item.get("date", item.get("period", god or "")),
                    vid_deyatelnosti=vid,
                    kod_okved=okved,
                    investitsii=item.get("value"),
                    dolya=item.get("share") or item.get("dolya"),
                )
            )
        return results
    except Exception:
        logger.exception("Ошибка при получении инвестиций по видам деятельности")
        return _fallback_investitsii_po_vidam(region, god)


def _fallback_investitsii_po_vidam(
    region: str = "",
    god: str = "",
) -> list[InvestitsiiPoVidam]:
    """Возврат справочных данных об инвестиционной деятельности как резервный вариант.

    Использует опубликованные данные Росстата за 2022 год при недоступности API.
    """
    region_name = ""
    if region:
        ri = next((r for r in SUBIEKTY_RF if r["kod"] == region), None)
        if ri:
            region_name = ri["nazvanie"]
    return [
        InvestitsiiPoVidam(
            region=region_name,
            period=god or "2022",
            vid_deyatelnosti=v["nazvanie"],
            kod_okved=v["kod"],
            investitsii=v.get("inv_2022"),
            dolya=v.get("dolya_2022"),
        )
        for v in VIDY_DEYATELNOSTI_INVESTITSII
    ]
