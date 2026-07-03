"""Интеграционные тесты для модуля Госдума."""

import pytest
from fastmcp import Client

from mcp_russia.data.gosduma.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
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
        "golosovaniya",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://struktura",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_prompty_zaregistrirovany(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_deputata", "obzor_zakonodatelstva"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_frakcii(client):
    async with client:
        rezultat = await client.call_tool("spisok_frakcii", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Единая Россия" in tekst


async def test_spisok_sozyvov(client):
    async with client:
        rezultat = await client.call_tool("spisok_sozyvov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "VIII" in tekst or "созыв" in tekst.lower()


async def test_spisok_komitetov(client):
    async with client:
        rezultat = await client.call_tool("spisok_komitetov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Комитет" in tekst
