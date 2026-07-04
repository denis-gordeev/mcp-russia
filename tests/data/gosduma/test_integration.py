"""Интеграционные тесты для модуля Госдума."""

import pytest
from fastmcp import Client

from mcp_russia.data.gosduma.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_deputatov",
        "info_deputata",
        "spisok_frakcii",
        "spisok_komitetov",
        "spisok_sozyvov",
        "zakonoproekty",
        "golosovaniya",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://istochniki",
        "data://struktura",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    async with klient:
        prompty = await klient.list_prompts()
    prompt_names = {p.name for p in prompty}

    ozhidayemyy = {"analiz_deputata", "obzor_zakonodatelstva"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_spisok_frakcii(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_frakcii", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Единая Россия" in tekst


async def test_spisok_sozyvov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_sozyvov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "VIII" in tekst or "созыв" in tekst.lower()


async def test_spisok_komitetov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_komitetov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Комитет" in tekst
