"""Общий lifespan для mcp-russia — создаёт/закрывает httpx.AsyncClient.

HTTP-клиент доступен в инструментах через kontekst.lifespan_context["http_klient"].

Использование:
    from mcp_russia._shared.lifespan import http_zhiznennyy_tsikl

    mcp = FastMCP("mcp-russia", instructions="...", version="0.5.0", lifespan=http_zhiznennyy_tsikl)
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from mcp_russia.settings import POLZOVATELSKIY_AGENT, TAIMAUT_HTTP

logger = logging.getLogger(__name__)


@lifespan
async def http_zhiznennyy_tsikl(
    server_funktsiya: FastMCP[Any],
) -> AsyncIterator[dict[str, Any] | None]:
    """Создание общего httpx.AsyncClient при запуске, закрытие при завершении."""
    logger.info("Запуск общего HTTP-клиента")
    klient = httpx.AsyncClient(
        timeout=httpx.Timeout(TAIMAUT_HTTP),
        headers={
            "User-Agent": POLZOVATELSKIY_AGENT,
            "Accept": "application/json",
        },
        follow_redirects=True,
    )
    try:
        yield {"http_klient": klient}
    finally:
        await klient.aclose()
        logger.info("Общий HTTP-клиент закрыт")
