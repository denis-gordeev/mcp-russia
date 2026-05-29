"""Интеграционные тесты для модуля Росреестра."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosreestr.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_tipov_nedvizhimosti",
        "spisok_kategoriy_zemel",
        "spisok_vidov_ispolzovaniya",
        "spisok_statusov_obiekta",
        "spisok_form_sobstvennosti",
        "info_obekta",
        "kadastrovaya_stoimost",
        "prava_na_obekt",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://zakonodatelstvo",
        "data://struktura",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_nedvizhimosti", "obzor_zemelnogo_uchastka"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_tipov_nedvizhimosti(client):
    async with client:
        result = await client.call_tool("spisok_tipov_nedvizhimosti", {})
    assert result is not None
    text = str(result)
    assert "Земельный участок" in text


async def test_spisok_kategoriy_zemel(client):
    async with client:
        result = await client.call_tool("spisok_kategoriy_zemel", {})
    assert result is not None
    text = str(result)
    assert "населённых пунктов" in text
