"""Интеграционные тесты для модуля Росприроднадзор."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosprirodnadzor.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_vidov_nadzora",
        "spisok_kategoriy_obnv",
        "spisok_vidov_litsenziy_nedra",
        "poisk_proverok",
        "info_proverki",
        "poisk_obektov_negativnogo",
        "poisk_litsenziy_nedra",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://struktura",
        "data://zakonodatelstvo",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_spisok_vidov_nadzora(client):
    async with client:
        rezultat = await client.call_tool("spisok_vidov_nadzora", {})
    assert rezultat is not None
