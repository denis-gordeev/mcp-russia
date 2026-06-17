"""HTTP-клиент для модуля Росстата / ЕМИСС.

Интеграция с реальными API:
    - ЕМИСС (fedstat.ru) для статистических показателей
    - Росстат (rosstat.gov.ru) для опубликованных данных
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

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
    IndikatorDannye,
    InvestitsiiPoVidam,
    OtraslevayaStrukturaVRP,
    PokazatelRosstata,
    RegionData,
    VRPData,
    WagesData,
)

logger = logging.getLogger(__name__)


async def poluchit_indikator(code: str, date_range: str = "") -> list[PokazatelRosstata]:
    """Получение статистического показателя из ЕМИСС/Росстата.

    Аргументы:
        code: Код показателя (напр. 'cpi', 'population').
        date_range: Фильтр по диапазону дат (необязательно).

    Возвращает:
        Список значений показателя.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get(code, code)
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if date_range:
            params["date"] = date_range
        data = await http_get(url, params=params, timeout=20.0)
        return _parse_indikator_response(data, code)
    except Exception:
        logger.exception("Ошибка при получении индикатора %s", code)
        return []


async def poluchit_dannye_regiona(code: str) -> RegionData | None:
    """Получение данных о субъекте РФ.

    Аргументы:
        code: Код региона (ОКАТО/ОКТМО).

    Возвращает:
        Данные региона или None.
    """
    region_info = next((r for r in SUBIEKTY_RF if r["code"] == code), None)
    if not region_info:
        return None
    try:
        url = f"{EMISS_API_BASE}/region/{code}"
        data = await http_get(url, timeout=20.0)
        if isinstance(data, dict):
            return RegionData(
                code=code,
                name=region_info["name"],
                federalny_okrug=region_info.get("okrug", ""),
                population=data.get("population"),
                vrp=data.get("gdp") or data.get("vrp"),
                srednyaya_zp=data.get("avgWage") or data.get("srednyaya_zp"),
            )
    except Exception:
        logger.exception("Ошибка при получении данных региона %s", code)

    return RegionData(
        code=code,
        name=region_info["name"],
        federalny_okrug=region_info.get("okrug", ""),
    )


async def poluchit_federalny_okrug(code: str) -> dict[str, Any]:
    """Получение данных о федеральном округе.

    Аргументы:
        code: Код федерального округа.

    Возвращает:
        Данные федерального округа.
    """
    okrug_info = next((o for o in FEDERALNYE_OKRUGA if o["code"] == code), None)
    if not okrug_info:
        return {"error": f"Федеральный округ '{code}' не найден"}

    regiony = [r for r in SUBIEKTY_RF if r.get("okrug") == code]
    return {
        "code": code,
        "name": okrug_info["name"],
        "kolichestvo_subiektov": len(regiony),
        "subiekty": [r["name"] for r in regiony],
    }


async def poluchit_inflyaciyu(god: str = "") -> list[dict[str, Any]]:
    """Получение данных об инфляции (ИПЦ) из ЕМИСС.

    Аргументы:
        god: Фильтр по году.

    Возвращает:
        Список точек данных ИПЦ.
    """
    try:
        emiss_code = EMISS_KODY_POKAZATELEY.get("cpi", "31088")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
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
        emiss_code = EMISS_KODY_POKAZATELEY.get("population", "24133")
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if region:
            params["region"] = region
        data = await http_get(url, params=params, timeout=20.0)
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
        data = await http_get(url, params=params, timeout=20.0)
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
                        ri = next((r for r in SUBIEKTY_RF if r["code"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["name"]
                    results.append(
                        VRPData(
                            period=item.get("date", item.get("period", "")),
                            region=region_name,
                            vrp=item.get("value"),
                            vrp_per_capita=item.get("perCapita"),
                        )
                    )
                return results
        return []
    except Exception:
        logger.exception("Ошибка при получении данных о ВРП")
        return []


async def poluchit_zarplatu(region: str = "", god: str = "") -> list[WagesData]:
    """Получение данных о заработной плате из ЕМИСС.

    Аргументы:
        region: Код региона (необязательно).
        god: Фильтр по году.

    Возвращает:
        Список точек данных о заработной плате.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get("wages", "24140")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
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
                        ri = next((r for r in SUBIEKTY_RF if r["code"] == str(reg_code)), None)
                        if ri:
                            region_name = ri["name"]
                    results.append(
                        WagesData(
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
        data = await http_get(url, params={"groupByRegion": "true"}, timeout=20.0)
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
                        ri = next((r for r in SUBIEKTY_RF if r["code"] == region_code), None)
                        if ri:
                            region_name = ri["name"]
                    results.append(
                        {
                            "region": region_name,
                            "code": region_code,
                            "value": item.get("value"),
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
        kod: Код ЕМИСС (напр. '31088') или мнемонический код (напр. 'cpi').
        region: Код региона для фильтрации (необязательно).
        god: Фильтр по году (необязательно).

    Возвращает:
        Список точек данных показателя.
    """
    emiss_code = EMISS_KODY_POKAZATELEY.get(kod, kod)
    indicator_name = next(
        (p["name"] for p in KLYUCHEVYE_INDIKATORY if p["code"] == kod),
        "",
    )
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
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
                ri = next((r for r in SUBIEKTY_RF if r["code"] == str(reg_code)), None)
                if ri:
                    region_name = ri["name"]
            results.append(
                IndikatorDannye(
                    kod_emiss=emiss_code,
                    nazvanie=indicator_name or item.get("name", kod),
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


def _parse_indikator_response(data: Any, code: str) -> list[PokazatelRosstata]:
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
                    code=code,
                    name=item.get("name", code),
                    value=float(item.get("value", 0)),
                    unit=item.get("unit", ""),
                    date=item.get("date", ""),
                )
            )
        except (ValueError, TypeError):
            continue
    return results


def get_subiekty_list() -> list[dict[str, str]]:
    """Возвращает список субъектов РФ, доступных для запросов."""
    return SUBIEKTY_RF


def get_federalny_okruga_list() -> list[dict[str, str]]:
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
    emiss_code = EMISS_KODY_POKAZATELEY.get("vrp_structure", "27103")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _fallback_otraslevaya_struktura(region, god)
        items = data.get("data", [])
        if not isinstance(items, list) or not items:
            return _fallback_otraslevaya_struktura(region, god)
        region_name = ""
        if region:
            ri = next((r for r in SUBIEKTY_RF if r["code"] == region), None)
            if ri:
                region_name = ri["name"]
        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            okved = item.get("okved", item.get("code", ""))
            otrasl = next(
                (o["name"] for o in OTRASLEVAYA_STRUKTURA_VRP if o["code"] == okved),
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
        ri = next((r for r in SUBIEKTY_RF if r["code"] == region), None)
        if ri:
            region_name = ri["name"]
    return [
        OtraslevayaStrukturaVRP(
            region=region_name,
            period=god or "2022",
            otrasl=o["name"],
            kod_okved=o["code"],
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
    emiss_code = EMISS_KODY_POKAZATELEY.get("investments_by_activity", "24145")
    try:
        url = f"{EMISS_API_BASE}/data/{emiss_code}"
        params: dict[str, str] = {"groupByActivity": "true"}
        if region:
            params["region"] = region
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=20.0)
        if not isinstance(data, dict):
            return _fallback_investitsii_po_vidam(region, god)
        items = data.get("data", [])
        if not isinstance(items, list) or not items:
            return _fallback_investitsii_po_vidam(region, god)
        region_name = ""
        if region:
            ri = next((r for r in SUBIEKTY_RF if r["code"] == region), None)
            if ri:
                region_name = ri["name"]
        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            okved = item.get("okved", item.get("activityCode", ""))
            vid = next(
                (v["name"] for v in VIDY_DEYATELNOSTI_INVESTITSII if v["code"] == okved),
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
        ri = next((r for r in SUBIEKTY_RF if r["code"] == region), None)
        if ri:
            region_name = ri["name"]
    return [
        InvestitsiiPoVidam(
            region=region_name,
            period=god or "2022",
            vid_deyatelnosti=v["name"],
            kod_okved=v["code"],
            investitsii=v.get("inv_2022"),
            dolya=v.get("dolya_2022"),
        )
        for v in VIDY_DEYATELNOSTI_INVESTITSII
    ]
