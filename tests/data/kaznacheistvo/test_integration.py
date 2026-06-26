"""Интеграционные тесты для модуля Федеральное казначейство."""

import pytest
from fastmcp import Client

from mcp_russia.data.kaznacheistvo.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_vidov_byudzhetov",
        "spisok_kategoriy_raskhodov",
        "ispolnenie_byudzheta",
        "poisk_uchastnikov_bp",
        "poisk_uchrezhdeniy",
        "mezhbyudzhetnye_transferty",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://kaznacheistvo/istochniki",
        "data://kaznacheistvo/struktura",
        "data://kaznacheistvo/byudzhetnaya-sistema",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_spisok_vidov_byudzhetov(client):
    async with client:
        result = await client.call_tool("spisok_vidov_byudzhetov", {})
    assert result is not None
