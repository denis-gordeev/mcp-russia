"""Интеграционные тесты для модуля Росгидромет."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosgidromet.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_stanciy",
        "spisok_tipov_dannykh",
        "pogoda_seychas",
        "prognoz_pogody",
        "ekologiya_regiona",
        "preduprezhdeniya",
        "sputnik_monitoring",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    """Проверка регистрации ресурсов."""
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://metodologiya",
        "data://opasnye-yavleniya",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_pogody_regiona", "obzor_ekologii"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_stanciy(client):
    """Проверка работы инструмента spisok_stanciy."""
    async with client:
        result = await client.call_tool("spisok_stanciy", {})
    assert result is not None
    text = str(result)
    assert "Москва" in text or "Санкт-Петербург" in text


async def test_spisok_tipov_dannykh(client):
    """Проверка работы инструмента spisok_tipov_dannykh."""
    async with client:
        result = await client.call_tool("spisok_tipov_dannykh", {})
    assert result is not None
    text = str(result)
    assert "погода" in text.lower() or "Температура" in text


async def test_preduprezhdeniya(client):
    """Проверка работы инструмента preduprezhdeniya."""
    async with client:
        result = await client.call_tool("preduprezhdeniya", {})
    assert result is not None
