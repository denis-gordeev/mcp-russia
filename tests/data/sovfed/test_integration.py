"""Интеграционные тесты для модуля Совет Федерации РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.sovfed.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_senatorov",
        "info_senatora",
        "spisok_komitetov",
        "spisok_komissiy",
        "poisk_zakonoproektov",
        "spisok_zasedaniy",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki-sovfeda",
        "data://struktura-sovfeda",
        "data://reglament-sovfeda",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_spisok_komitetov(client):
    async with client:
        rezultat = await client.call_tool("spisok_komitetov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Комитет" in tekst
