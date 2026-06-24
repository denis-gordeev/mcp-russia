"""Тесты общего жизненного цикла — HTTP-клиент."""

import contextlib

import pytest

from mcp_russia._shared.lifespan import http_zhiznennyy_tsikl


class TestHttpLifespan:
    """Проверяет, что http_zhiznennyy_tsikl создаёт и закрывает httpx.AsyncClient."""

    @pytest.mark.asyncio
    async def test_lifespan_creates_and_closes_client(self) -> None:
        """Lifespan должен вернуть http_client и закрыть его при выходе."""
        from fastmcp import FastMCP

        server = FastMCP("test")

        # Имитируем генератор жизненного цикла
        gen = http_zhiznennyy_tsikl._fn(server)
        context = await gen.__anext__()

        assert context is not None
        assert "http_client" in context

        client = context["http_client"]
        assert not client.is_closed

        # Очистка
        with contextlib.suppress(StopAsyncIteration):
            await gen.__anext__()

        assert client.is_closed

    @pytest.mark.asyncio
    async def test_lifespan_client_has_correct_headers(self) -> None:
        """HTTP-клиент должен иметь заголовки User-Agent и Accept."""
        from fastmcp import FastMCP

        server = FastMCP("test")

        gen = http_zhiznennyy_tsikl._fn(server)
        context = await gen.__anext__()

        assert context is not None
        client = context["http_client"]
        assert "User-Agent" in client.headers
        assert client.headers["Accept"] == "application/json"

        # Очистка
        with contextlib.suppress(StopAsyncIteration):
            await gen.__anext__()
