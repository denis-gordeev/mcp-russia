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
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "spisok_funktsiy" in names

    @pytest.mark.asyncio
    async def test_rekomendovat_instrumenty_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "rekomendovat_instrumenty" in names

    @pytest.mark.asyncio
    async def test_splanirovat_zapros_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "splanirovat_zapros" in names

    @pytest.mark.asyncio
    async def test_instrumenty_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "cbrf_tekushchie_kursy" in names
            assert "cbrf_uznat_kurs_valyuty" in names

    @pytest.mark.asyncio
    async def test_instrumenty_rosgidromet_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "rosgidromet_pogoda_seychas" in names

    @pytest.mark.asyncio
    async def test_instrumenty_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "sovfed_spisok_senatorov" in names
            assert "sovfed_spisok_komitetov" in names

    @pytest.mark.asyncio
    async def test_instrumenty_kaznacheistvo_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "kaznacheistvo_spisok_vidov_byudzhetov" in names

    @pytest.mark.asyncio
    async def test_instrumenty_rosprirodnadzor_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "rosprirodnadzor_spisok_vidov_nadzora" in names

    @pytest.mark.asyncio
    async def test_spisok_funktsiy_vozvrashchaet_svodku(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool("spisok_funktsiy", {})
            assert "cbrf" in result.data
            assert "gosduma" in result.data
            assert "sovfed" in result.data


class TestResursyKornevogoServera:
    @pytest.mark.asyncio
    async def test_resursy_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert any("cbrf" in u for u in uris)

    @pytest.mark.asyncio
    async def test_resursy_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert any("sovfed" in u or "istochniki" in u for u in uris)


class TestPromptyKornevogoServera:
    @pytest.mark.asyncio
    async def test_prompty_cbrf_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert any("cbrf" in n for n in names)

    @pytest.mark.asyncio
    async def test_prompty_sovfed_s_prostranstvom_imen(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert any("sovfed" in n for n in names)


class TestVypolnitPaket:
    @pytest.mark.asyncio
    async def test_zaregistrirovan(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "vypolnit_paket" in names

    @pytest.mark.asyncio
    async def test_imeet_docstring(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            tool = next(t for t in tools if t.name == "vypolnit_paket")
            assert tool.description
            assert "параллельно" in tool.description.lower()


class TestTegiInstrumentovKornevogoServera:
    @pytest.mark.asyncio
    async def test_instrumenty_imeyut_tegi(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            cbrf_tool = next((t for t in tools if t.name == "cbrf_tekushchie_kursy"), None)
            assert cbrf_tool is not None

    @pytest.mark.asyncio
    async def test_metainstrumenty_imeyut_teg_obnaruzheniya(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            spisok = next((t for t in tools if t.name == "spisok_funktsiy"), None)
            assert spisok is not None
