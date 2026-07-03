"""Интеграционные тесты для модуля Росстат."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosstat.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_regionov",
        "spisok_okrugov",
        "informatsiya_o_regionye",
        "informatsiya_ob_okruge",
        "pokazateli_rosstata",
        "inflyaciya",
        "demografiya",
        "vrp_dannye",
        "zarplata_dannye",
        "sravnenie_regionov",
        "indikator_dannye",
    }
    assert expected.issubset(tool_names), f"Отсутствуют инструменты: {expected - tool_names}"


async def test_resursy_zaregistrirovany(client):
    async with client:
        resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}

    expected = {
        "data://istochniki",
        "data://metodologiya",
    }
    assert expected.issubset(uris), f"Отсутствуют ресурсы: {expected - uris}"


async def test_prompty_zaregistrirovany(client):
    async with client:
        prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}

    expected = {"analiz_regiona", "obzor_inflyacii"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_regionov(client):
    async with client:
        rezultat = await client.call_tool("spisok_regionov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Москва" in tekst or "Санкт-Петербург" in tekst


async def test_pokazateli_rosstata(client):
    async with client:
        rezultat = await client.call_tool("pokazateli_rosstata", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "населени" in tekst.lower() or "показател" in tekst.lower()


async def test_inflyaciya(client):
    async with client:
        rezultat = await client.call_tool("inflyaciya", {"god": "2025"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ИПЦ" in tekst or "Инфляц" in tekst


async def test_vrp_dannye(client):
    async with client:
        rezultat = await client.call_tool("vrp_dannye", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ВРП" in tekst or "Валовой" in tekst


async def test_zarplata_dannye(client):
    async with client:
        rezultat = await client.call_tool("zarplata_dannye", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "заработ" in tekst.lower()


async def test_indikator_dannye(client):
    async with client:
        rezultat = await client.call_tool("indikator_dannye", {"kod": "ipcz"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ИПЦ" in tekst or "Инфляц" in tekst or "31088" in tekst
