"""Тесты общего HTTP-клиента."""

from unittest.mock import patch

import httpx
import pytest
import respx

from mcp_russia._shared.http_client import http_poluchit, sozdat_klienta
from mcp_russia.exceptions import OshibkaHttpClienta


class TestSozdatKlienta:
    def test_vozvrashchaet_asinkhronnyy_klienta(self) -> None:
        klient = sozdat_klienta()
        assert isinstance(klient, httpx.AsyncClient)

    def test_ustanavlivaet_zagolovki_po_umolchaniyu(self) -> None:
        klient = sozdat_klienta()
        assert "mcp-russia" in klient.headers["user-agent"]
        assert klient.headers["accept"] == "application/json"

    def test_polzovatelskiy_bazovyy_url(self) -> None:
        klient = sozdat_klienta(bazovyy_adres_url="https://www.cbr.ru")
        assert str(klient.base_url) == "https://www.cbr.ru"

    def test_polzovatelskiy_taimaut(self) -> None:
        klient = sozdat_klienta(taimaut=5.0)
        assert klient.timeout.connect == 5.0

    def test_polzovatelskie_zagolovki_obedineny(self) -> None:
        klient = sozdat_klienta(zagolovki={"X-Api-Key": "secret"})
        assert klient.headers["x-api-key"] == "secret"
        assert "mcp-russia" in klient.headers["user-agent"]

    def test_perenapravleniya_vklucheny(self) -> None:
        klient = sozdat_klienta()
        assert klient.follow_redirects is True


class TestHttpPoluchit:
    @pytest.mark.asyncio
    @respx.mock
    async def test_uspekh_vozvrashchaet_json(self) -> None:
        respx.get("https://api.example.com/data").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        rezultat = await http_poluchit("https://api.example.com/data")
        assert rezultat == {"ok": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_s_parametrami(self) -> None:
        respx.get("https://api.example.com/search").mock(
            return_value=httpx.Response(200, json=[1, 2, 3])
        )
        rezultat = await http_poluchit("https://api.example.com/search", parametry={"q": "test"})
        assert rezultat == [1, 2, 3]

    @pytest.mark.asyncio
    @respx.mock
    async def test_404_vyzyvaet_nemedlenno(self) -> None:
        """Ошибки 4xx (кроме 429) не должны повторяться."""
        respx.get("https://api.example.com/missing").mock(
            return_value=httpx.Response(404, text="Not Found")
        )
        with pytest.raises(OshibkaHttpClienta, match="HTTP 404"):
            await http_poluchit("https://api.example.com/missing", maks_povtorov=2)

    @pytest.mark.asyncio
    @respx.mock
    async def test_500_povtoryaet_zatem_uspekh(self) -> None:
        """Ошибка сервера при первой попытке, успех при второй."""
        marshrut = respx.get("https://api.example.com/flaky")
        marshrut.side_effect = [
            httpx.Response(500, text="Internal Server Error"),
            httpx.Response(200, json={"recovered": True}),
        ]
        with patch("mcp_russia._shared.http_client.asyncio.sleep"):
            rezultat = await http_poluchit("https://api.example.com/flaky", maks_povtorov=2)
        assert rezultat == {"recovered": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_429_povtoryaet(self) -> None:
        """Запросы с ограничением скорости должны повторяться."""
        marshrut = respx.get("https://api.example.com/limited")
        marshrut.side_effect = [
            httpx.Response(429, text="Too Many Requests"),
            httpx.Response(200, json={"ok": True}),
        ]
        with patch("mcp_russia._shared.http_client.asyncio.sleep"):
            rezultat = await http_poluchit("https://api.example.com/limited", maks_povtorov=2)
        assert rezultat == {"ok": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_vse_povtory_ischerpany(self) -> None:
        """После исчерпания всех попыток возбуждает OshibkaHttpClienta."""
        respx.get("https://api.example.com/down").mock(
            return_value=httpx.Response(503, text="Service Unavailable")
        )
        with (
            patch("mcp_russia._shared.http_client.asyncio.sleep"),
            pytest.raises(OshibkaHttpClienta, match="не удался после"),
        ):
            await http_poluchit("https://api.example.com/down", maks_povtorov=1)

    @pytest.mark.asyncio
    @respx.mock
    async def test_taimaut_povtoryaet(self) -> None:
        """Ошибки таймаута должны повторяться."""
        marshrut = respx.get("https://api.example.com/slow")
        marshrut.side_effect = [
            httpx.ReadTimeout("timeout"),
            httpx.Response(200, json={"ok": True}),
        ]
        with patch("mcp_russia._shared.http_client.asyncio.sleep"):
            rezultat = await http_poluchit("https://api.example.com/slow", maks_povtorov=2)
        assert rezultat == {"ok": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_nol_povtorov_bez_povtora(self) -> None:
        """При maks_povtorov=0 повторных запросов не происходит."""
        respx.get("https://api.example.com/once").mock(
            return_value=httpx.Response(500, text="Error")
        )
        with pytest.raises(OshibkaHttpClienta, match="HTTP 500"):
            await http_poluchit("https://api.example.com/once", maks_povtorov=0)
