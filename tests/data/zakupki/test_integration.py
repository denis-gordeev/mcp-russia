"""Интеграционные тесты для модуля Закупки (ЕИС)."""

import pytest
from fastmcp import Client

from mcp_russia.data.zakupki.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "poisk_zakupok",
        "info_zakupki",
        "poisk_kontraktov",
        "info_zakazchika",
        "info_postavshchika",
        "statusy_zakupok",
        "sposoby_zakupok",
        "plany_zakupok",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    """Проверка регистрации ресурсов."""
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
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_zakupki", "obzor_zakupok"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_statusy_zakupok(client):
    """Проверка работы инструмента statusy_zakupok."""
    async with client:
        rezultat = await client.call_tool("statusy_zakupok", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Планирование" in tekst or "Завершена" in tekst


async def test_sposoby_zakupok(client):
    """Проверка работы инструмента sposoby_zakupok."""
    async with client:
        rezultat = await client.call_tool("sposoby_zakupok", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Электронный аукцион" in tekst or "аукцион" in tekst.lower()
