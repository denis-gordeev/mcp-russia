"""Интеграционные тесты для модуля Госдума."""

import pytest
from fastmcp import Client

from mcp_russia.data.gosduma.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_deputatov",
        "info_deputata",
        "spisok_frakcii",
        "spisok_komitetov",
        "spisok_sozyvov",
        "zakonoproekty",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://struktura",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_deputata", "obzor_zakonodatelstva"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_frakcii(client):
    async with client:
        result = await client.call_tool("spisok_frakcii", {})
    assert result is not None
    text = str(result)
    assert "Единая Россия" in text


async def test_spisok_sozyvov(client):
    async with client:
        result = await client.call_tool("spisok_sozyvov", {})
    assert result is not None
    text = str(result)
    assert "VIII" in text or "созыв" in text.lower()


async def test_zakonoproekty(client):
    async with client:
        result = await client.call_tool("zakonoproekty", {})
    assert result is not None
    text = str(result)
    assert "Законопроект" in text or "СОЗД" in text
