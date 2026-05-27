"""Интеграционные тесты для модуля ФНС."""

import pytest
from fastmcp import Client

from mcp_brasil.data.fns.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_nalogovyh_rezhimov",
        "spisok_vidov_nalogov",
        "spisok_tipov_proverok",
        "spisok_statusov_organizaciy",
        "spisok_kategoriy_nalogoplatelshchikov",
        "info_organizacii",
        "info_ip",
        "proverki_organizacii",
        "nalogovye_nachisleniya",
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

    expected = {"analiz_nalogoplatelshchika", "obzor_rezhimov_nalogooblozheniya"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_spisok_nalogovyh_rezhimov(client):
    async with client:
        result = await client.call_tool("spisok_nalogovyh_rezhimov", {})
    assert result is not None
    text = str(result)
    assert "ОСНО" in text


async def test_spisok_vidov_nalogov(client):
    async with client:
        result = await client.call_tool("spisok_vidov_nalogov", {})
    assert result is not None
    text = str(result)
    assert "НДС" in text
