"""Интеграционные тесты для модуля ФССП."""

import pytest
from fastmcp import Client

from mcp_brasil.data.fssp.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_vidov_proizvodstv",
        "spisok_statusov_proizvodstva",
        "spisok_ogranicheniy",
        "spisok_kategoriy_dolzhnikov",
        "spisok_osnovaniy_vozbuzhdeniya",
        "info_proizvodstva",
        "poisk_dolzhnika",
        "ogranicheniya_dolzhnika",
        "rozysk_dolzhnika",
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
        "data://zakonodatelstvo",
        "data://struktura",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_dolzhnika", "obzor_ispolnitelnogo_proizvodstva"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_spisok_vidov_proizvodstv(client):
    async with client:
        result = await client.call_tool("spisok_vidov_proizvodstv", {})
    assert result is not None
    text = str(result)
    assert "ГИБДД" in text


async def test_spisok_ogranicheniy(client):
    async with client:
        result = await client.call_tool("spisok_ogranicheniy", {})
    assert result is not None
    text = str(result)
    assert "выезд" in text
