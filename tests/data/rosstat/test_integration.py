"""Интеграционные тесты для модуля Росстат."""

import pytest
from fastmcp import Client

from mcp_brasil.data.rosstat.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_regionov",
        "spisok_okrugov",
        "region_info",
        "okrug_info",
        "pokazateli_rosstata",
        "inflyaciya",
        "demografiya",
    }
    assert expected.issubset(tool_names), (
        f"Отсутствуют инструменты: {expected - tool_names}"
    )


async def test_has_resources(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://metodologiya",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_regiona", "obzor_inflyacii"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_spisok_regionov(client):
    async with client:
        result = await client.call_tool("spisok_regionov", {})
    assert result is not None
    text = str(result)
    assert "Москва" in text or "Санкт-Петербург" in text


async def test_pokazateli_rosstata(client):
    async with client:
        result = await client.call_tool("pokazateli_rosstata", {})
    assert result is not None
    text = str(result)
    assert "населени" in text.lower() or "показател" in text.lower()


async def test_inflyaciya(client):
    async with client:
        result = await client.call_tool("inflyaciya", {"god": "2025"})
    assert result is not None
    text = str(result)
    assert "ИПЦ" in text or "Инфляц" in text
