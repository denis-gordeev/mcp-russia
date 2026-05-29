"""Интеграционные тесты для модуля Картотека арбитражных дел."""

import pytest
from fastmcp import Client

from mcp_russia.data.kad_arbitrazh.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "poisk_del",
        "info_dela",
        "akty_po_delu",
        "storony_dela",
        "spravochnik_kategoriy",
        "spravochnik_instantsiy",
        "spravochnik_statusov",
        "spravochnik_aktov",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    """Проверка регистрации ресурсов."""
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://sistema",
        "data://kodifikatsiya",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_dela", "analiz_uchastnika"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_poisk_del(client):
    """Проверка работы инструмента poisk_del."""
    async with client:
        result = await client.call_tool("poisk_del", {})
    assert result is not None
    text = str(result)
    assert "Картотека" in text or "kad.arbitr.ru" in text


async def test_spravochnik_kategoriy(client):
    """Проверка работы инструмента spravochnik_kategoriy."""
    async with client:
        result = await client.call_tool("spravochnik_kategoriy", {})
    assert result is not None
    text = str(result)
    assert "Банкротство" in text or "Налоговые" in text


async def test_spravochnik_instantsiy(client):
    """Проверка работы инструмента spravochnik_instantsiy."""
    async with client:
        result = await client.call_tool("spravochnik_instantsiy", {})
    assert result is not None
    text = str(result)
    assert "первая инстанция" in text or "кассация" in text
