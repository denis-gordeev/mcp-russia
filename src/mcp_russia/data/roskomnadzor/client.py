"""HTTP client stubs for the Роскомнадзор feature.

All functions are placeholders — real API integration with
rkn.gov.ru requires separate work.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import RKN_API_BASE

logger = logging.getLogger(__name__)

API_BASE = RKN_API_BASE


async def get_napravleniya() -> list[dict[str, Any]]:
    """Return направления деятельности (placeholder)."""
    url = f"{API_BASE}/napravleniya"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении направлений деятельности")
        return []


async def get_tipy_licenziy() -> list[dict[str, Any]]:
    """Return типы лицензий связи (placeholder)."""
    url = f"{API_BASE}/tipy-licenziy"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении типов лицензий")
        return []


async def get_kategorii_narusheniy() -> list[dict[str, Any]]:
    """Return категории нарушений (placeholder)."""
    url = f"{API_BASE}/kategorii-narusheniy"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении категорий нарушений")
        return []


async def get_reestry() -> list[dict[str, Any]]:
    """Return список реестров (placeholder)."""
    url = f"{API_BASE}/reestry"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении списка реестров")
        return []


async def get_tipy_smi() -> list[dict[str, Any]]:
    """Return типы СМИ (placeholder)."""
    url = f"{API_BASE}/tipy-smi"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении типов СМИ")
        return []


async def get_licenziya(nomer: str) -> dict[str, Any] | None:
    """Return info лицензии (placeholder)."""
    url = f"{API_BASE}/licenziya/{nomer}"
    try:
        data = await http_get(url)
        return data if isinstance(data, dict) else None
    except Exception:
        logger.exception("Ошибка при получении лицензии №%s", nomer)
        return None


async def get_smi(registracionnyy_nomer: str = "") -> list[dict[str, Any]]:
    """Return список СМИ (placeholder)."""
    url = f"{API_BASE}/smi"
    try:
        params: dict[str, Any] = {}
        if registracionnyy_nomer:
            params["registracionnyy_nomer"] = registracionnyy_nomer
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении списка СМИ")
        return []


async def get_operator_pd(inn: str = "") -> list[dict[str, Any]]:
    """Return операторы персональных данных (placeholder)."""
    url = f"{API_BASE}/operator-pd"
    try:
        params: dict[str, Any] = {}
        if inn:
            params["inn"] = inn
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении операторов ПД")
        return []


async def get_narusheniya(organizaciya: str = "") -> list[dict[str, Any]]:
    """Return список нарушений (placeholder)."""
    url = f"{API_BASE}/narusheniya"
    try:
        params: dict[str, Any] = {}
        if organizaciya:
            params["organizaciya"] = organizaciya
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении нарушений")
        return []


async def get_zapis_reestra(reestr_code: str, zapisi_id: str) -> dict[str, Any] | None:
    """Return запись из реестра (placeholder)."""
    url = f"{API_BASE}/reestr/{reestr_code}/{zapisi_id}"
    try:
        data = await http_get(url)
        return data if isinstance(data, dict) else None
    except Exception:
        logger.exception("Ошибка при получении записи реестра %s/%s", reestr_code, zapisi_id)
        return None
