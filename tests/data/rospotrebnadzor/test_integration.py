"""Интеграционные тесты для модуля Роспотребнадзора."""

import pytest
from fastmcp import Client

from mcp_russia.data.rospotrebnadzor.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_napravleniy",
        "spisok_tipov_proverok",
        "spisok_kategoriy_obiektov",
        "spisok_regionalnyh_upravleniy",
        "info_proverki",
        "poisk_proverok",
        "plan_proverok",
        "poisk_narusheniy",
        "spisok_sanpinov",
        "zhaloby_potrebiteley",
        "pokazateli_bezopasnosti",
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

    ozhidayemyy = {"analiz_proverki", "obzor_sanitarnoy_situacii"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_napravleniy(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_napravleniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Санитарно-эпидемиологический" in tekst


async def test_spisok_sanpinov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_sanpinov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "СанПиН" in tekst
