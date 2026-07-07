"""Интеграционные тесты для модуля ФССП."""

import pytest
from fastmcp import Client

from mcp_russia.data.fssp.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_vidov_proizvodstv",
        "spisok_statusov_proizvodstva",
        "spisok_ogranicheniy",
        "spisok_kategoriy_dolzhnikov",
        "spisok_osnovaniy_vozbuzhdeniya",
        "spisok_regionov",
        "info_proizvodstva",
        "poisk_dolzhnika",
        "ogranicheniya_dolzhnika",
        "rozysk_dolzhnika",
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
        "data://zakonodatelstvo",
        "data://struktura",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_dolzhnika", "obzor_ispolnitelnogo_proizvodstva"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_vidov_proizvodstv(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_vidov_proizvodstv", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ГИБДД" in tekst


async def test_spisok_ogranicheniy(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_ogranicheniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "выезд" in tekst
