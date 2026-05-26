"""Интеграционные тесты для модуля Минздрав РФ."""

import pytest
from fastmcp import Client

from mcp_brasil.data.minzdrav.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "poisk_med_organizatsiy",
        "info_med_organizatsii",
        "pokazateli_zdorovya",
        "statistika_zabolevaniy",
        "spravochnik_mo",
        "spravochnik_spetsialnostey",
        "spravochnik_mkb10",
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
        "data://klassifikatsii",
        "data://okruga",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    """Проверка регистрации промптов."""
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_zdorovya_regiona", "obzor_med_organizatsiy"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_poisk_med_organizatsiy(client):
    """Проверка работы инструмента poisk_med_organizatsiy."""
    async with client:
        result = await client.call_tool("poisk_med_organizatsiy", {})
    assert result is not None
    text = str(result)
    assert "Медицинские организации" in text or "minzdrav.gov.ru" in text


async def test_spravochnik_mo(client):
    """Проверка работы инструмента spravochnik_mo."""
    async with client:
        result = await client.call_tool("spravochnik_mo", {})
    assert result is not None
    text = str(result)
    assert "Больница" in text or "Поликлиника" in text


async def test_pokazateli_zdorovya(client):
    """Проверка работы инструмента pokazateli_zdorovya."""
    async with client:
        result = await client.call_tool("pokazateli_zdorovya", {"god": 2024})
    assert result is not None
    text = str(result)
    assert "2024" in text or "продолжительность" in text
