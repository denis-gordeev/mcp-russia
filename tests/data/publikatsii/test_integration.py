"""Интеграционные тесты для модуля Официальные публикации РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.publikatsii.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_tipov_aktov",
        "spisok_otrasley",
        "spisok_istochnikov",
        "spisok_statusov",
        "info_normativnogo_akta",
        "info_zakonproekta",
        "poisk_aktov",
        "publikatsii_po_datam",
        "izmeneniya_akta",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    """Проверка регистрации ресурсов."""
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://poryadok-opublikovaniya",
        "data://struktura-zakonodatelstva",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_normativnogo_akta", "obzor_zakonodatelstva"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_tipov_aktov(client):
    """Проверка работы инструмента spisok_tipov_aktov."""
    async with client:
        result = await client.call_tool("spisok_tipov_aktov", {})
    assert result is not None
    text = str(result)
    assert "Федеральный закон" in text or "Указ" in text


async def test_spisok_otrasley(client):
    """Проверка работы инструмента spisok_otrasley."""
    async with client:
        result = await client.call_tool("spisok_otrasley", {})
    assert result is not None
    text = str(result)
    assert "Гражданское" in text or "Уголовное" in text


async def test_spisok_statusov(client):
    """Проверка работы инструмента spisok_statusov."""
    async with client:
        result = await client.call_tool("spisok_statusov", {})
    assert result is not None
    text = str(result)
    assert "Действующий" in text or "Утратил" in text
