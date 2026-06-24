"""Общий lifespan для mcp-russia — создаёт/закрывает httpx.AsyncClient.

HTTP-клиент доступен в инструментах через ctx.lifespan_context["http_client"].

Использование:
    from mcp_russia._shared.lifespan import http_zhiznennyy_tsikl

    mcp = FastMCP("mcp-russia", lifespan=http_zhiznennyy_tsikl)
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from mcp_russia.settings import HTTP_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)


@lifespan
async def http_zhiznennyy_tsikl(server: FastMCP[Any]) -> AsyncIterator[dict[str, Any] | None]:
    """Создание общего httpx.AsyncClient при запуске, закрытие при завершении."""
    logger.info("Запуск общего HTTP-клиента")
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(HTTP_TIMEOUT),
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        follow_redirects=True,
    )
    try:
        yield {"http_client": client}
    finally:
        await client.aclose()
        logger.info("Общий HTTP-клиент закрыт")
