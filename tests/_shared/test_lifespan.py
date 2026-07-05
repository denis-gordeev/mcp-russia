"""Тесты общего жизненного цикла — HTTP-клиент."""

import contextlib

import pytest

from mcp_russia._shared.lifespan import http_zhiznennyy_tsikl


class TestHttpZhiznennyyTsikl:
    """Проверяет, что http_zhiznennyy_tsikl создаёт и закрывает httpx.AsyncClient."""

    @pytest.mark.asyncio
    async def test_zhiznennyy_tsikl_sozdaet_i_zakryvaet_klienta(self) -> None:
        """Жизненный цикл должен вернуть HTTP-клиент и закрыть его при выходе."""
        from fastmcp import FastMCP

        server_funktsiya = FastMCP("test")

        # Имитируем генератор жизненного цикла
        generator = http_zhiznennyy_tsikl._fn(server_funktsiya)
        kontekst = await generator.__anext__()

        assert kontekst is not None
        assert "http_klient" in kontekst

        klient = kontekst["http_klient"]
        assert not klient.is_closed

        # Очистка
        with contextlib.suppress(StopAsyncIteration):
            await generator.__anext__()

        assert klient.is_closed

    @pytest.mark.asyncio
    async def test_klient_imeet_pravilnye_zagolovki(self) -> None:
        """HTTP-клиент должен иметь заголовки User-Agent и Accept."""
        from fastmcp import FastMCP

        server_funktsiya = FastMCP("test")

        generator = http_zhiznennyy_tsikl._fn(server_funktsiya)
        kontekst = await generator.__anext__()

        assert kontekst is not None
        klient = kontekst["http_klient"]
        assert "User-Agent" in klient.headers
        assert klient.headers["Accept"] == "application/json"

        # Очистка
        with contextlib.suppress(StopAsyncIteration):
            await generator.__anext__()
