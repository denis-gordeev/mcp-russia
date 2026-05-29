"""Integration tests for the Dados Abertos feature using fastmcp.Client.

These tests verify the full pipeline: server -> tools -> client (mocked HTTP).
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from mcp_russia.data.dados_abertos.schemas import ConjuntoDados, ConjuntoResultado
from mcp_russia.data.dados_abertos.server import mcp

CLIENT_MODULE = "mcp_russia.data.dados_abertos.client"


class TestToolsRegistered:
    @pytest.mark.asyncio
    async def test_all_4_tools_registered(self) -> None:
        async with Client(mcp) as c:
            tool_list = await c.list_tools()
            names = {t.name for t in tool_list}
            expected = {
                "buscar_conjuntos",
                "detalhar_conjunto",
                "listar_organizacoes",
                "buscar_recursos",
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
    async def test_1_resource_registered(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            expected = {"data://formatos"}
            assert expected.issubset(uris), f"Missing: {expected - uris}"


class TestPromptsRegistered:
    @pytest.mark.asyncio
    async def test_1_prompt_registered(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            expected = {"explorar_dados"}
            assert expected.issubset(names), f"Missing: {expected - names}"


class TestToolExecution:
    @pytest.mark.asyncio
    async def test_buscar_conjuntos_e2e(self) -> None:
        mock_data = ConjuntoResultado(
            total=1,
            conjuntos=[
                ConjuntoDados(
                    id="abc-123",
                    titulo="Dados de Saúde Pública",
                    organizacao_nome="Ministério da Saúde",
                    temas=["Saúde"],
                    data_atualizacao="2024-06-20",
                ),
            ],
        )
        with patch(
            f"{CLIENT_MODULE}.buscar_conjuntos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            async with Client(mcp) as c:
                result = await c.call_tool(
                    "buscar_conjuntos",
                    {"texto": "saúde"},
                )
                assert "Dados de Saúde Pública" in result.data
                assert "Ministério da Saúde" in result.data

    @pytest.mark.asyncio
    async def test_detalhar_conjunto_not_found(self) -> None:
        with patch(
            f"{CLIENT_MODULE}.detalhar_conjunto",
            new_callable=AsyncMock,
            return_value=None,
        ):
            async with Client(mcp) as c:
                result = await c.call_tool(
                    "detalhar_conjunto",
                    {"conjunto_id": "nao-existe"},
                )
                assert "não encontrado" in result.data
