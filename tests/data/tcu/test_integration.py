"""Integration tests for the TCU feature using fastmcp.Client."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from mcp_russia.data.tcu.schemas import (
    Acordao,
    InabilitadoResultado,
)
from mcp_russia.data.tcu.server import mcp

CLIENT_MODULE = "mcp_russia.data.tcu.client"


class TestToolsRegistered:
    @pytest.mark.asyncio
    async def test_all_8_tools_registered(self) -> None:
        async with Client(mcp) as c:
            tool_list = await c.list_tools()
            names = {t.name for t in tool_list}
            expected = {
                "buscar_acordaos",
                "consultar_inabilitados",
                "consultar_inidoneos",
                "consultar_certidoes_apf",
                "calcular_debito_tcu",
                "buscar_pedidos_congresso",
                "buscar_contratos_tcu",
                "consultar_cadirreg",
            }
            assert expected.issubset(names), f"Missing: {expected - names}"

    @pytest.mark.asyncio
    async def test_tools_have_docstrings(self) -> None:
        async with Client(mcp) as c:
            tool_list = await c.list_tools()
            for tool in tool_list:
                assert tool.description, f"Tool {tool.name} has no description"


class TestResourcesRegistered:
    @pytest.mark.asyncio
    async def test_tipos_certidoes_resource(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "data://tipos-certidoes-apf" in uris, f"URIs: {uris}"

    @pytest.mark.asyncio
    async def test_tipos_certidoes_content(self) -> None:
        async with Client(mcp) as c:
            content = await c.read_resource("data://tipos-certidoes-apf")
            text = content[0].text if isinstance(content, list) else str(content)
            assert "Inidoneos" in text
            assert "CNIA" in text
            assert "CEIS" in text
            assert "CNEP" in text


class TestPromptsRegistered:
    @pytest.mark.asyncio
    async def test_investigar_empresa_prompt(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            assert "investigar_empresa_tcu" in names, f"Prompts: {names}"


class TestToolExecution:
    @pytest.mark.asyncio
    async def test_buscar_acordaos_e2e(self) -> None:
        mock_data = [
            Acordao(
                titulo="ACORDAO 100/2026 - PLENARIO",
                colegiado="Plenario",
                relator="BRUNO DANTAS",
            ),
        ]
        with patch(
            f"{CLIENT_MODULE}.buscar_acordaos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            async with Client(mcp) as c:
                result = await c.call_tool("buscar_acordaos", {})
                assert "ACORDAO 100/2026" in result.data

    @pytest.mark.asyncio
    async def test_consultar_inabilitados_empty(self) -> None:
        mock_data = InabilitadoResultado(items=[], count=0)
        with patch(
            f"{CLIENT_MODULE}.consultar_inabilitados",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            async with Client(mcp) as c:
                result = await c.call_tool("consultar_inabilitados", {"cpf": "99999999999"})
                assert "não consta" in result.data
