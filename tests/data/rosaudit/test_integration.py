"""Интеграционные тесты для модуля Счётная палата РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosaudit.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    """Проверка регистрации инструментов."""
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_napravleniy",
        "spisok_tipov_meropriyatiy",
        "spisok_subiektov_audita",
        "poisk_kontrolnyh_meropriyatiy",
        "info_kontrolnogo_meropriyatiya",
        "info_auditorskogo_zaklyucheniya",
        "ispolnenie_byudzheta",
        "poisk_narusheniy",
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

    expected = {"analiz_auditorskogo_zaklyucheniya", "obzor_ispolneniya_byudzheta"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_napravleniy(client):
    """Проверка работы инструмента spisok_napravleniy."""
    async with client:
        rezultat = await client.call_tool("spisok_napravleniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "бюджет" in tekst.lower() or "Контроль" in tekst


async def test_spisok_tipov_meropriyatiy(client):
    """Проверка работы инструмента spisok_tipov_meropriyatiy."""
    async with client:
        rezultat = await client.call_tool("spisok_tipov_meropriyatiy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Проверка" in tekst or "Экспертиза" in tekst


async def test_spisok_subiektov_audita(client):
    """Проверка работы инструмента spisok_subiektov_audita."""
    async with client:
        rezultat = await client.call_tool("spisok_subiektov_audita", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Федеральные" in tekst or "Государственные" in tekst
