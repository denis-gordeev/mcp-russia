"""Интеграционные тесты для модуля ЦБ РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.cbrf.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_has_tools(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "tekushchie_kursy",
        "uznat_kurs_valyuty",
        "spisok_valyut",
        "konvertirovat_valyutu",
        "kursy_po_stranam",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_has_resources(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://valyuty",
        "data://osnovnye",
        "data://spravochnik",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_has_prompts(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analise_valyut", "obzor_ekonomiki"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_valyut(client):
    async with client:
        result = await client.call_tool("spisok_valyut", {})
    assert result is not None
    text = str(result)
    assert "USD" in text or "валют" in text


async def test_uznat_kurs_valyuty(client):
    async with client:
        result = await client.call_tool("uznat_kurs_valyuty", {"kod": "USD"})
    assert result is not None
    text = str(result)
    assert "USD" in text or "ЦБ РФ" in text or "не найдена" in text


async def test_kursy_po_stranam(client):
    async with client:
        result = await client.call_tool("kursy_po_stranam", {})
    assert result is not None
