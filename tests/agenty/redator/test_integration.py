"""Интеграционные тесты модуля официальных документов с fastmcp.Client."""

import pytest
from fastmcp import Client

from mcp_russia.agenty.redator.server import mcp


class TestToolsRegistered:
    @pytest.mark.asyncio
    async def test_all_5_tools_registered(self) -> None:
        async with Client(mcp) as c:
            tool_list = await c.list_tools()
            names = {t.name for t in tool_list}
            expected = {
                "formatirovat_data_extenso",
                "generirovat_numeraciyu",
                "konsulitirovat_obrashchenie",
                "validirovat_dokument",
                "spisok_tipov_dokumentov",
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
    async def test_all_resources_registered(self) -> None:
        async with Client(mcp) as c:
            resources = await c.list_resources()
            uris = {str(r.uri) for r in resources}
            expected = {
                "template://pismo",
                "template://prikaz",
                "template://rasporyazhenie",
                "template://akt",
                "template://spravka",
                "template://protokol",
                "template://dokladnaya_zapiska",
                "normas://manual",
                "normas://obrashcheniya",
                "normas://zaklyuchitelnye",
            }
            assert expected.issubset(uris), f"Missing: {expected - uris}"


class TestPromptsRegistered:
    @pytest.mark.asyncio
    async def test_all_prompts_registered(self) -> None:
        async with Client(mcp) as c:
            prompts = await c.list_prompts()
            names = {p.name for p in prompts}
            expected = {
                "redaktor_pismo",
                "redaktor_prikaz",
                "redaktor_rasporyazhenie",
                "redaktor_akt",
                "redaktor_spravka",
                "redaktor_protokol",
                "redaktor_dokladnaya_zapiska",
            }
            assert expected.issubset(names), f"Missing: {expected - names}"


class TestToolExecution:
    @pytest.mark.asyncio
    async def test_formatirovat_data_e2e(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool(
                "formatirovat_data_extenso",
                {"gorod": "Санкт-Петербург"},
            )
            assert "г. Санкт-Петербург" in result.data

    @pytest.mark.asyncio
    async def test_generirovat_numeraciyu_e2e(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool(
                "generirovat_numeraciyu",
                {"tip": "письмо", "nomer": 42, "god": 2026, "otdel": "Д-15"},
            )
            assert "ПИСЬМО № 42/2026/Д-15" in result.data

    @pytest.mark.asyncio
    async def test_konsulitirovat_obrashchenie_e2e(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool(
                "konsulitirovat_obrashchenie",
                {"dolzhnost": "Губернатор"},
            )
            assert "Уважаемый господин Губернатор" in result.data

    @pytest.mark.asyncio
    async def test_spisok_tipov_e2e(self) -> None:
        async with Client(mcp) as c:
            result = await c.call_tool("spisok_tipov_dokumentov", {})
            assert "приказ" in result.data
            assert "письмо" in result.data


class TestResourceExecution:
    @pytest.mark.asyncio
    async def test_read_template_pismo(self) -> None:
        async with Client(mcp) as c:
            content = await c.read_resource("template://pismo")
            text = content[0].text if hasattr(content[0], "text") else str(content[0])
            assert "ПИСЬМО" in text or "ОФИЦИАЛЬНОЕ ПИСЬМО" in text

    @pytest.mark.asyncio
    async def test_read_template_prikaz(self) -> None:
        async with Client(mcp) as c:
            content = await c.read_resource("template://prikaz")
            text = content[0].text if hasattr(content[0], "text") else str(content[0])
            assert "ПРИКАЗ" in text

    @pytest.mark.asyncio
    async def test_read_normas_manual(self) -> None:
        async with Client(mcp) as c:
            content = await c.read_resource("normas://manual")
            text = content[0].text if hasattr(content[0], "text") else str(content[0])
            assert "ГОСТ" in text or "единообразие" in text.lower()

    @pytest.mark.asyncio
    async def test_read_normas_obrashcheniya(self) -> None:
        async with Client(mcp) as c:
            content = await c.read_resource("normas://obrashcheniya")
            text = content[0].text if hasattr(content[0], "text") else str(content[0])
            assert "Президент" in text or "Уважаемый" in text


class TestPromptExecution:
    @pytest.mark.asyncio
    async def test_prompt_pismo(self) -> None:
        async with Client(mcp) as c:
            result = await c.get_prompt(
                "redaktor_pismo",
                arguments={
                    "adresat": "Иванов Иван Иванович",
                    "dolzhnost_adresata": "Министр",
                    "tema": "Согласование проекта",
                },
            )
            messages = result.messages
            assert len(messages) == 2
            assert "ПИСЬМО" in messages[0].content.text
            assert "Согласование проекта" in messages[0].content.text

    @pytest.mark.asyncio
    async def test_prompt_prikaz(self) -> None:
        async with Client(mcp) as c:
            result = await c.get_prompt(
                "redaktor_prikaz",
                arguments={"tema": "О проведении инвентаризации"},
            )
            messages = result.messages
            assert len(messages) == 2
            assert "ПРИКАЗ" in messages[0].content.text
            assert "инвентаризации" in messages[0].content.text
