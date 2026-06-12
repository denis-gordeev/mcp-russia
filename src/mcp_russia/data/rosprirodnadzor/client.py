"""HTTP-клиент для модуля Росприроднадзора.

Интеграция с реальными API:
    - Росприроднадзор: rpn.gov.ru
    - Открытые данные Росприроднадзора: rpn.gov.ru/opendata
    - Реестр ОНВ: onv.register.rpn.gov.ru
    - Госуслуги ЭКО: gosuslugi.ru/api/eco
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    GOSUSLUGI_EKO_BASE,
    KATEGORII_OBNV,
    ONV_REGISTER_BASE,
    ROSPRIRODNADZOR_API_BASE,
    ROSPRIRODNADZOR_OPENDATA_BASE,
    VIDY_LITSENZIY_NEDRA,
    VIDY_NADZORA,
)

logger = logging.getLogger(__name__)


async def poisk_proverok(
    organizaciya: str = "",
    vid_nadzora: str = "",
    god: int = 0,
    limit: int = 20,
) -> list[dict[str, Any]]:
    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/inspections"
        params: dict[str, Any] = {"limit": limit}
        if organizaciya:
            params["organization"] = organizaciya
        if vid_nadzora:
            params["supervisionType"] = vid_nadzora
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_proverka(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен")

    try:
        url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/inspections"
        params: dict[str, Any] = {"limit": limit}
        if organizaciya:
            params["organization"] = organizaciya
        if god:
            params["year"] = god
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_proverka(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru/opendata недоступен")

    return []


async def info_proverki(nomer: str) -> dict[str, Any] | None:
    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/inspections/{nomer}"
        data = await http_get(url, timeout=15.0)
        if isinstance(data, dict):
            return _parse_proverka(data)
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для проверки №%s", nomer)
        return None


async def poisk_obektov_negativnogo(
    organizaciya: str = "",
    kategoriya: str = "",
    limit: int = 20,
) -> list[dict[str, Any]]:
    try:
        url = f"{ONV_REGISTER_BASE}/search"
        params: dict[str, Any] = {"limit": limit}
        if organizaciya:
            params["name"] = organizaciya
        if kategoriya:
            params["category"] = kategoriya
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_obekt_negativnogo(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("ONV реестр недоступен")

    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/onv"
        params: dict[str, Any] = {"limit": limit}
        if organizaciya:
            params["organization"] = organizaciya
        if kategoriya:
            params["category"] = kategoriya
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_obekt_negativnogo(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для ОНВ")

    return []


async def poisk_litsenziy_nedra(
    territory: str = "",
    vid_litsenzii: str = "",
    limit: int = 20,
) -> list[dict[str, Any]]:
    try:
        url = f"{ROSPRIRODNADZOR_OPENDATA_BASE}/licenses"
        params: dict[str, Any] = {"limit": limit}
        if territory:
            params["territory"] = territory
        if vid_litsenzii:
            params["licenseType"] = vid_litsenzii
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        if items:
            return [_parse_litsenziya(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru/opendata недоступен для лицензий")

    try:
        url = f"{ROSPRIRODNADZOR_API_BASE}/licenses"
        params: dict[str, Any] = {"limit": limit}
        if territory:
            params["territory"] = territory
        if vid_litsenzii:
            params["licenseType"] = vid_litsenzii
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_litsenziya(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("rpn.gov.ru API недоступен для лицензий")
        return []


async def poluchit_ekologicheskie_platezhi(
    god: int = 0,
    tip_platezha: str = "",
) -> list[dict[str, Any]]:
    try:
        url = f"{GOSUSLUGI_EKO_BASE}/payments"
        params: dict[str, Any] = {}
        if god:
            params["year"] = god
        if tip_platezha:
            params["paymentType"] = tip_platezha
        data = await http_get(url, params=params, timeout=15.0)
        items = _extract_list(data)
        return [_parse_ekologicheskiy_platezh(p) for p in items if isinstance(p, dict)]
    except Exception:
        logger.debug("Госуслуги ЭКО API недоступен")
        return []


def get_vidy_nadzora_list() -> list[dict[str, str]]:
    return VIDY_NADZORA


def get_kategori_obnv_list() -> list[dict[str, str]]:
    return KATEGORII_OBNV


def get_vidy_litsenziy_nedra_list() -> list[dict[str, str]]:
    return VIDY_LITSENZIY_NEDRA


def _extract_list(data: Any) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _parse_proverka(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "organizaciya": data.get("organization", "") or data.get("organizaciya", ""),
        "vid_nadzora": data.get("supervisionType", "") or data.get("vid_nadzora", ""),
        "data_nachala": data.get("startDate", "") or data.get("data_nachala", ""),
        "data_okonchaniya": data.get("endDate", "") or data.get("data_okonchaniya", ""),
        "status": data.get("status", ""),
        "vyavleno_narusheniy": data.get("violationsCount", 0)
        or data.get("vyavleno_narusheniy", 0),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _parse_obekt_negativnogo(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "nazvanie": data.get("title", "") or data.get("name", "") or data.get("nazvanie", ""),
        "kategoriya": data.get("category", "") or data.get("kategoriya", ""),
        "region": data.get("region", "") or data.get("subject", ""),
        "vid_deyatelnosti": data.get("activityType", "") or data.get("vid_deyatelnosti", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _parse_litsenziya(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "vid_litsenzii": data.get("licenseType", "") or data.get("vid_litsenzii", ""),
        "territory": data.get("territory", "") or data.get("region", ""),
        "srok_deystviya": data.get("validityPeriod", "") or data.get("srok_deystviya", ""),
        "derzhatel": data.get("holder", "") or data.get("derzhatel", ""),
        "istochnik": "Росприроднадзор (rpn.gov.ru)",
    }


def _parse_ekologicheskiy_platezh(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "nomer": data.get("id", "") or data.get("number", "") or data.get("nomer", ""),
        "tip_platezha": data.get("paymentType", "") or data.get("tip_platezha", ""),
        "summa": data.get("amount") or data.get("summa"),
        "god": data.get("year", "") or data.get("god", ""),
        "platelshchik": data.get("payer", "") or data.get("platelshchik", ""),
        "istochnik": "Госуслуги ЭКО (gosuslugi.ru)",
    }
