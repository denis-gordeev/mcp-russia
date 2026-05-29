"""Integration tests for the root mcp-russia server.

Tests the fully composed server with all features mounted.
MCP_BRASIL_TOOL_SEARCH=none is set in conftest.py (before any import).
"""

import pytest
from fastmcp import Client

from mcp_russia.server import mcp


class TestRootServerTools:
    @pytest.mark.asyncio
    async def test_spisok_funktsiy_registered(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "spisok_funktsiy" in names

    @pytest.mark.asyncio
    async def test_rekomendovat_instrumenty_registered(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "rekomendovat_instrumenty" in names

    @pytest.mark.asyncio
    async def test_splanirovat_zapros_registered(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "splanirovat_zapros" in names

    @pytest.mark.asyncio
    async def test_ibge_tools_namespaced(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "ibge_listar_estados" in names
            assert "ibge_buscar_municipios" in names

    @pytest.mark.asyncio
    async def test_bacen_tools_namespaced(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "bacen_consultar_serie" in names
            assert "bacen_buscar_serie" in names

    @pytest.mark.asyncio
    async def test_camara_tools_namespaced(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "camara_listar_deputados" in names
            assert "camara_buscar_proposicao" in names
            assert "camara_votos_nominais" in names

    @pytest.mark.asyncio
    async def test_senado_tools_namespaced(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "senado_listar_senadores" in names
            assert "senado_buscar_materia" in names
            assert "senado_listar_comissoes" in names
            assert "senado_agenda_plenario" in names

    @pytest.mark.asyncio
    async def test_spisok_funktsiy_returns_summary(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool("spisok_funktsiy", {})
            assert "ibge" in result.data
            assert "bacen" in result.data
            assert "camara" in result.data
            assert "senado" in result.data
            assert "cekrf" in result.data
            assert "Legacy-слой BCB внутри mcp-russia" not in result.data
            assert "DEPRECATED" in result.data
            assert "Legacy-слой CNES/DataSUS внутри mcp-russia" in result.data


class TestRootServerResources:
    @pytest.mark.asyncio
    async def test_ibge_resources_namespaced(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "data://ibge/estados" in uris
            assert "data://ibge/regioes" in uris
            assert "data://ibge/niveis-territoriais" in uris

    @pytest.mark.asyncio
    async def test_bacen_resources_namespaced(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "data://bacen/catalogo" in uris
            assert "data://bacen/categorias" in uris
            assert "data://bacen/indicadores-chave" in uris

    @pytest.mark.asyncio
    async def test_camara_resources_namespaced(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "data://camara/tipos-proposicao" in uris
            assert "data://camara/legislaturas" in uris
            assert "data://camara/info-api" in uris

    @pytest.mark.asyncio
    async def test_senado_resources_namespaced(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "data://senado/tipos-materia" in uris
            assert "data://senado/info-api" in uris
            assert "data://senado/comissoes-permanentes" in uris


class TestRootServerPrompts:
    @pytest.mark.asyncio
    async def test_ibge_prompts_namespaced(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert "ibge_resumo_estado" in names
            assert "ibge_comparativo_regional" in names

    @pytest.mark.asyncio
    async def test_bacen_prompts_namespaced(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert "bacen_analise_economica" in names
            assert "bacen_comparar_indicadores" in names

    @pytest.mark.asyncio
    async def test_camara_prompts_namespaced(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert "camara_acompanhar_proposicao" in names
            assert "camara_perfil_deputado" in names
            assert "camara_analise_votacao" in names

    @pytest.mark.asyncio
    async def test_senado_prompts_namespaced(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert "senado_acompanhar_materia" in names
            assert "senado_perfil_senador" in names
            assert "senado_analise_votacao_senado" in names


class TestVypolnitPaket:
    @pytest.mark.asyncio
    async def test_registered(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "vypolnit_paket" in names

    @pytest.mark.asyncio
    async def test_has_docstring(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            tool = next(t for t in tools if t.name == "vypolnit_paket")
            assert tool.description
            assert "параллельно" in tool.description.lower()


class TestRootServerToolTags:
    @pytest.mark.asyncio
    async def test_tools_have_tags(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            ibge_tool = next((t for t in tools if t.name == "ibge_listar_estados"), None)
            assert ibge_tool is not None

    @pytest.mark.asyncio
    async def test_meta_tools_have_discovery_tag(self) -> None:
        async with Client(mcp) as c:
            tools = await c.list_tools()
            spisok = next((t for t in tools if t.name == "spisok_funktsiy"), None)
            assert spisok is not None
