"""Интеграционные тесты для модуля ГИБДД/МВД."""

from unittest.mock import patch

import pytest
from fastmcp import Client

from mcp_russia.data.gibdd.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_tipov_ts",
        "spisok_kategoriyy_vu",
        "spisok_vidov_narusheniy",
        "spisok_statusov_shtrafov",
        "spisok_tipov_dtp",
        "spisok_regionov_registratsii",
        "info_ts",
        "info_vu",
        "shtrafy_po_ts",
        "shtrafy_po_vu",
        "statistika_dtp",
        "istoriya_registraciy",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
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
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_transportnogo_sredstva", "analiz_voditelya"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_tool_spisok_tipov_ts(client):
    async with client:
        result = await client.call_tool("spisok_tipov_ts", {})
    assert result is not None
    text = str(result)
    assert "Легковой" in text


async def test_tool_info_ts(client):
    from mcp_russia.data.gibdd import tools as gibdd_tools

    with patch.object(gibdd_tools, "_polnaya_proverka_ts", return_value=([], [], [], [])):
        async with client:
            result = await client.call_tool("info_ts", {"vin": "XTA21140052XXXXXX"})
    assert result is not None
    text = str(result)
    assert "не найден" in text
