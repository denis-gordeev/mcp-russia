"""Интеграционные тесты для модуля Минобрнауки."""

import pytest
from fastmcp import Client

from mcp_russia.data.minobrnauki.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_tipov_vuzov",
        "spisok_form_obucheniya",
        "spisok_urovney_obrazovaniya",
        "spisok_otrasley_nauki",
        "spisok_tipov_grantov",
        "spisok_statusov_akkreditatsii",
        "spisok_federalnyh_okrugov",
        "info_vuza",
        "programmy_vuza",
        "granty_i_isledovaniya",
        "reyting_vuzov",
        "aspirantura",
        "poisk_licenziy",
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

    expected = {"analiz_vuza", "obzor_nauchnyh_grantov"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_tool_spisok_tipov_vuzov(client):
    async with client:
        rezultat = await client.call_tool("spisok_tipov_vuzov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Университет" in tekst


async def test_tool_info_vuza(client):
    async with client:
        rezultat = await client.call_tool("info_vuza", {"nazvanie": "МГУ"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "не найден" in tekst or "не найдена" in tekst or "placeholder" in tekst.lower()
