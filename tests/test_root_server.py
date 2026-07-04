"""Интеграционные тесты для корневого сервера mcp-russia.

Проверяет полностью собранный сервер со всеми подключенными features.
MCP_RUSSIA_TOOL_SEARCH=none устанавливается в conftest.py (до импорта).
"""

import pytest
from fastmcp import Client

from mcp_russia.server import mcp


class TestInstrumentyKornevogoServera:
    @pytest.mark.asyncio
    async def test_spisok_funktsiy_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "spisok_funktsiy" in imena

    @pytest.mark.asyncio
    async def test_rekomendovat_instrumenty_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "rekomendovat_instrumenty" in imena

    @pytest.mark.asyncio
    async def test_splanirovat_zapros_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "splanirovat_zapros" in imena

    @pytest.mark.asyncio
    async def test_instrumenty_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "cbrf_tekushchie_kursy" in imena
            assert "cbrf_uznat_kurs_valyuty" in imena

    @pytest.mark.asyncio
    async def test_instrumenty_rosgidromet_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "rosgidromet_pogoda_seychas" in imena

    @pytest.mark.asyncio
    async def test_instrumenty_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "sovfed_spisok_senatorov" in imena
            assert "sovfed_spisok_komitetov" in imena

    @pytest.mark.asyncio
    async def test_instrumenty_kaznacheistvo_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "kaznacheistvo_spisok_vidov_byudzhetov" in imena

    @pytest.mark.asyncio
    async def test_instrumenty_rosprirodnadzor_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "rosprirodnadzor_spisok_vidov_nadzora" in imena

    @pytest.mark.asyncio
    async def test_spisok_funktsiy_vozvrashchaet_svodku(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.call_tool("spisok_funktsiy", {})
            assert "cbrf" in rezultat.data
            assert "gosduma" in rezultat.data
            assert "sovfed" in rezultat.data


class TestResursyKornevogoServera:
    @pytest.mark.asyncio
    async def test_resursy_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            resursy = await c.list_resources()
            adresa_uri = {str(r.uri) for r in resursy}
            assert any("cbrf" in u for u in adresa_uri)

    @pytest.mark.asyncio
    async def test_resursy_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            resursy = await c.list_resources()
            adresa_uri = {str(r.uri) for r in resursy}
            assert any("sovfed" in u or "istochniki" in u for u in adresa_uri)


class TestPromptyKornevogoServera:
    @pytest.mark.asyncio
    async def test_prompty_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            prompty = await c.list_prompts()
            imena = {p.name for p in prompty}
            assert any("cbrf" in n for n in imena)

    @pytest.mark.asyncio
    async def test_prompty_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            prompty = await c.list_prompts()
            imena = {p.name for p in prompty}
            assert any("sovfed" in n for n in imena)


class TestVypolnitPaket:
    @pytest.mark.asyncio
    async def test_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            imena = {t.name for t in instrumenty}
            assert "vypolnit_paket" in imena

    @pytest.mark.asyncio
    async def test_imeet_docstring(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            instrument = next(t for t in instrumenty if t.name == "vypolnit_paket")
            assert instrument.description
            assert "параллельно" in instrument.description.lower()


class TestTegiInstrumentovKornevogoServera:
    @pytest.mark.asyncio
    async def test_instrumenty_imeyut_tegi(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            cbrf_instrument = next(
                (t for t in instrumenty if t.name == "cbrf_tekushchie_kursy"), None
            )
            assert cbrf_instrument is not None

    @pytest.mark.asyncio
    async def test_metainstrumenty_imeyut_teg_obnaruzheniya(self) -> None:
        async with Client(mcp) as c:
            instrumenty = await c.list_tools()
            spisok = next((t for t in instrumenty if t.name == "spisok_funktsiy"), None)
            assert spisok is not None
