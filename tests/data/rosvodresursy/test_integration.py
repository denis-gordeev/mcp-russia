"""Интеграционные тесты для модуля Росводресурсы."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosvodresursy.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_basseynovykh_okrugov",
        "spisok_tipov_vodnykh_obektov",
        "spisok_vodokhranilishch",
        "poisk_vodnykh_obektov",
        "info_vodnogo_obekta",
        "gidro_monitoring",
        "info_vodokhranilishcha",
        "vodopolzovanie_regionov",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    """Проверка регистрации ресурсов."""
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://basseynovye-okruga",
        "data://vodokhozyaystvo",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_vodnogo_obekta", "obzor_vodokhranilishch"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_basseynovykh_okrugov(client):
    """Проверка работы инструмента spisok_basseynovykh_okrugov."""
    async with client:
        result = await client.call_tool("spisok_basseynovykh_okrugov", {})
    assert result is not None
    text = str(result)
    assert "Волжский" in text or "Донской" in text


async def test_spisok_vodokhranilishch(client):
    """Проверка работы инструмента spisok_vodokhranilishch."""
    async with client:
        result = await client.call_tool("spisok_vodokhranilishch", {})
    assert result is not None
    text = str(result)
    assert "Братское" in text or "Куйбышевское" in text


async def test_gidro_monitoring(client):
    async with client:
        result = await client.call_tool("gidro_monitoring", {"identifikator_posta": ""})
    assert result is not None
