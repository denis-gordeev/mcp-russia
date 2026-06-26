"""Интеграционные тесты для модуля Роскомнадзора."""

import pytest
from fastmcp import Client

from mcp_russia.data.roskomnadzor.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(client):
    async with client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}

    expected = {
        "spisok_napravleniy",
        "spisok_tipov_licenziy",
        "spisok_kategoriy_narusheniy",
        "spisok_reestrov",
        "spisok_tipov_smi",
        "spisok_kategoriy_pd_operatorov",
        "info_licenzii",
        "poisk_smi",
        "info_operatora_pd",
        "poisk_narusheniy",
        "proverka_blokirovki",
        "poisk_ori",
        "zapisi_reestra",
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

    expected = {"analiz_narusheniya", "obzor_reestrov"}
    assert expected.issubset(prompt_names), f"Отсутствуют промпты: {expected - prompt_names}"


async def test_spisok_reestrov(client):
    async with client:
        result = await client.call_tool("spisok_reestrov", {})
    assert result is not None
    text = str(result)
    assert "запрещённых сайтов" in text


async def test_spisok_kategoriy_narusheniy(client):
    async with client:
        result = await client.call_tool("spisok_kategoriy_narusheniy", {})
    assert result is not None
    text = str(result)
    assert "персональных данных" in text
