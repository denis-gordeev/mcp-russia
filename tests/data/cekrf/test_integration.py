"""Интеграционные тесты для модуля ЦИК РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.cekrf.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "tipy_vyborov",
        "subyekty_rf",
        "dolzhnosti_federal",
        "partii_rf",
        "gody_vyborov",
        "poisk_kandidata",
        "kandidat_podrobno",
        "rezultaty_vyborov",
        "yavka_i_itogi",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    """Проверка регистрации ресурсов."""
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://tipy-vyborov",
        "data://subyekty-rf",
        "data://partii-rf",
        "data://info-api",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_kandidata", "sravnenie_partiy"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_tipy_vyborov(client):
    """Проверка работы инструмента tipy_vyborov."""
    async with client:
        result = await client.call_tool("tipy_vyborov", {})
    assert result is not None
    text = str(result.content) if hasattr(result, "content") else str(result)
    assert "Президент" in text or "Государственная" in text


async def test_subyekty_rf(client):
    """Проверка работы инструмента subyekty_rf."""
    async with client:
        result = await client.call_tool("subyekty_rf", {})
    assert result is not None
    text = str(result)
    assert "Москва" in text or "Санкт-Петербург" in text


async def test_partii_rf(client):
    """Проверка работы инструмента partii_rf."""
    async with client:
        result = await client.call_tool("partii_rf", {})
    assert result is not None
    text = str(result)
    assert "Единая Россия" in text


async def test_gody_vyborov(client):
    """Проверка работы инструмента gody_vyborov."""
    async with client:
        result = await client.call_tool("gody_vyborov", {})
    assert result is not None
    text = str(result)
    assert "2024" in text or "2021" in text
