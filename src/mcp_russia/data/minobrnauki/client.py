"""HTTP client stubs for the Минобрнауки feature.

All functions are placeholders — real API integration with
minobrnauki.gov.ru / vuz.minobrnauki.gov.ru requires separate work.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import MINOBRNAUKI_API_BASE

logger = logging.getLogger(__name__)

API_BASE = MINOBRNAUKI_API_BASE


async def poluchit_vuz(nazvanie: str) -> dict[str, Any] | None:
    """Return данные вуза (placeholder)."""
    url = f"{API_BASE}/vuz"
    try:
        data = await http_get(url, params={"nazvanie": nazvanie})
        return data if isinstance(data, dict) else None
    except Exception:
        logger.exception("Ошибка при получении данных вуза «%s»", nazvanie)
        return None


async def poluchit_programmy(vuz: str, uroven: str = "") -> list[dict[str, Any]]:
    """Return образовательные программы вуза (placeholder)."""
    url = f"{API_BASE}/programmy"
    try:
        params: dict[str, Any] = {"vuz": vuz}
        if uroven:
            params["uroven"] = uroven
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении программ вуза «%s»", vuz)
        return []


async def poluchit_granty(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Return гранты и научные исследования (placeholder)."""
    url = f"{API_BASE}/granty"
    try:
        params: dict[str, Any] = {}
        if organizatsiya:
            params["organizatsiya"] = organizatsiya
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении грантов")
        return []


async def poluchit_reyting(tip_reytinga: str = "", god: int = 0) -> list[dict[str, Any]]:
    """Return рейтинг вузов (placeholder)."""
    url = f"{API_BASE}/reyting"
    try:
        params: dict[str, Any] = {}
        if tip_reytinga:
            params["tip_reytinga"] = tip_reytinga
        if god:
            params["god"] = god
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении рейтинга вузов")
        return []


async def poluchit_aspirantov(organizatsiya: str = "") -> list[dict[str, Any]]:
    """Return данные об аспирантах (placeholder)."""
    url = f"{API_BASE}/aspiranty"
    try:
        params: dict[str, Any] = {}
        if organizatsiya:
            params["organizatsiya"] = organizatsiya
        data = await http_get(url, params=params)
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("Ошибка при получении данных об аспирантах")
        return []
