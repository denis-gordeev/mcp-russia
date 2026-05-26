"""Интеграционные тесты для модуля Закупки (ЕИС)."""

import pytest
from fastmcp import Client

from mcp_brasil.data.zakupki.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "poisk_zakupok",
        "info_zakupki",
        "info_zakazchika",
        "info_postavshchika",
        "statusy_zakupok",
        "sposoby_zakupok",
        "plany_zakupok",
    }
    assert expected.issubset(tool_names), (
        f"Отсутствуют инструменты: {expected - tool_names}"
    )


async def test_has_resources(client):
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


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_zakupki", "obzor_zakupok"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_poisk_zakupok(client):
    """Проверка работы инструмента poisk_zakupok."""
    async with client:
        result = await client.call_tool("poisk_zakupok", {})
    assert result is not None
    text = str(result)
    assert "ЕИС" in text or "zakupki.gov.ru" in text


async def test_statusy_zakupok(client):
    """Проверка работы инструмента statusy_zakupok."""
    async with client:
        result = await client.call_tool("statusy_zakupok", {})
    assert result is not None
    text = str(result)
    assert "Планирование" in text or "Завершена" in text


async def test_plany_zakupok(client):
    """Проверка работы инструмента plany_zakupok."""
    async with client:
        result = await client.call_tool("plany_zakupok", {"god": 2025})
    assert result is not None
    text = str(result)
    assert "2025" in text
