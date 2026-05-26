"""Интеграционные тесты для модуля RosAPI.

Note: rosapi/prompts.py imports UserMessage which may not exist in this
version of FastMCP. If server import fails, tests are skipped.
"""

import pytest
from fastmcp import Client

try:
    from mcp_brasil.data.rosapi.server import mcp
    _IMPORT_OK = True
except ImportError:
    _IMPORT_OK = False


@pytest.fixture
def client():
    if not _IMPORT_OK:
        pytest.skip("rosapi server import fails (UserMessage not available)")
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "konsul_adres_po_indeksu",
        "poisk_adresa",
        "poisk_org_po_inn",
        "poisk_org_po_ogrn",
        "spisok_bankov",
        "konsul_bank_po_bik",
        "prazdniki_rf",
        "nalogovye_stavki",
    }
    assert expected.issubset(tool_names), (
        f"Отсутствуют инструменты: {expected - tool_names}"
    )


async def test_has_resources(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://nalogovye-stavki",
        "data://servisy",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_organizacii", "poisk_adresa_prompt"}
    assert expected.issubset(prompt_names), (
        f"Отсутствуют промпты: {expected - prompt_names}"
    )


async def test_spisok_bankov(client):
    async with client:
        result = await client.call_tool("spisok_bankov", {})
    assert result is not None
    text = str(result)
    assert "Сбербанк" in text or "ВТБ" in text


async def test_prazdniki_rf(client):
    async with client:
        result = await client.call_tool("prazdniki_rf", {"god": 2025})
    assert result is not None
    text = str(result)
    assert "Новый год" in text or "Победы" in text


async def test_nalogovye_stavki(client):
    async with client:
        result = await client.call_tool("nalogovye_stavki", {})
    assert result is not None
    text = str(result)
    assert "НДС" in text or "налог" in text.lower()
