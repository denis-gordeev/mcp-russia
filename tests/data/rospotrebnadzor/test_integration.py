"""Интеграционные тесты для модуля Роспотребнадзора."""

import pytest
from fastmcp import Client

from mcp_russia.data.rospotrebnadzor.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_napravleniy",
        "spisok_tipov_proverok",
        "spisok_kategoriy_obiektov",
        "spisok_regionalnyh_upravleniy",
        "info_proverki",
        "poisk_proverok",
        "plan_proverok",
        "poisk_narusheniy",
        "spisok_sanpinov",
        "zhaloby_potrebiteley",
        "pokazateli_bezopasnosti",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://zakonodatelstvo",
        "data://struktura",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_prompty_zaregistrirovany(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_proverki", "obzor_sanitarnoy_situacii"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_napravleniy(client):
    async with client:
        rezultat = await client.call_tool("spisok_napravleniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Санитарно-эпидемиологический" in tekst


async def test_spisok_sanpinov(client):
    async with client:
        rezultat = await client.call_tool("spisok_sanpinov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "СанПиН" in tekst
