"""Интеграционные тесты для модуля Совет Федерации РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.sovfed.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_senatorov",
        "info_senatora",
        "spisok_komitetov",
        "spisok_komissiy",
        "poisk_zakonoproektov",
        "spisok_zasedaniy",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://istochniki-sovfeda",
        "data://struktura-sovfeda",
        "data://reglament-sovfeda",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_spisok_komitetov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_komitetov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Комитет" in tekst
