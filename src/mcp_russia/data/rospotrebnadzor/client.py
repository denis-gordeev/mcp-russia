"""HTTP client stubs for the Роспотребнадзор feature.

All functions are placeholders — real API integration with
rospotrebnadzor.ru requires separate work.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import ROSPOTREBNADZOR_API_BASE

logger = logging.getLogger(__name__)

API_BASE = ROSPOTREBNADZOR_API_BASE


async def get_napravleniya() -> list[dict[str, Any]]:
    """Return направления деятельности (placeholder)."""
    url = f"{API_BASE}/napravleniya"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении направлений деятельности")
        return []


async def get_tipy_proverok() -> list[dict[str, Any]]:
    """Return типы проверок (placeholder)."""
    url = f"{API_BASE}/tipy-proverok"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении типов проверок")
        return []


async def get_kategorii_obiektov() -> list[dict[str, Any]]:
    """Return категории объектов надзора (placeholder)."""
    url = f"{API_BASE}/kategorii-obiektov"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении категорий объектов")
        return []


async def get_regionalnye_upravleniya() -> list[dict[str, Any]]:
    """Return региональные управления (placeholder)."""
    url = f"{API_BASE}/regionalnye-upravleniya"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении региональных управлений")
        return []


async def get_proverka(nomer: str) -> dict[str, Any] | None:
    """Return info проверки (placeholder)."""
    url = f"{API_BASE}/proverka/{nomer}"
    try:
        data = await http_get(url)
        return data if isinstance(data, dict) else None
    except Exception:
        logger.exception("Ошибка при получении проверки №%s", nomer)
        return None


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


async def get_pokazateli(kod: str = "") -> list[dict[str, Any]]:
    """Return показатели безопасности (placeholder)."""
    url = f"{API_BASE}/pokazateli"
    try:
        params: dict[str, Any] = {}
        if kod:
            params["kod"] = kod
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении показателей безопасности")
        return []


async def get_zhaloby(organizaciya: str = "") -> list[dict[str, Any]]:
    """Return жалобы потребителей (placeholder)."""
    url = f"{API_BASE}/zhaloby"
    try:
        params: dict[str, Any] = {}
        if organizaciya:
            params["organizaciya"] = organizaciya
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении жалоб потребителей")
        return []


async def get_sanpiny() -> list[dict[str, Any]]:
    """Return список основных СанПиН (placeholder)."""
    url = f"{API_BASE}/sanpiny"
    try:
        data = await http_get(url)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении списка СанПиН")
        return []
