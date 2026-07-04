"""Интеграционные тесты для модуля Росприроднадзор."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosprirodnadzor.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_vidov_nadzora",
        "spisok_kategoriy_obnv",
        "spisok_vidov_litsenziy_nedra",
        "poisk_proverok",
        "info_proverki",
        "poisk_obektov_negativnogo",
        "poisk_litsenziy_nedra",
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
        "data://zakonodatelstvo",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_spisok_vidov_nadzora(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_vidov_nadzora", {})
    assert rezultat is not None
