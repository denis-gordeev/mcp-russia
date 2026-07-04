"""Интеграционные тесты для модуля Федеральное казначейство."""

import pytest
from fastmcp import Client

from mcp_russia.data.kaznacheistvo.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_vidov_byudzhetov",
        "spisok_kategoriy_raskhodov",
        "ispolnenie_byudzheta",
        "poisk_uchastnikov_bp",
        "poisk_uchrezhdeniy",
        "mezhbyudzhetnye_transferty",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://kaznacheistvo/istochniki",
        "data://kaznacheistvo/struktura",
        "data://kaznacheistvo/byudzhetnaya-sistema",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_spisok_vidov_byudzhetov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_vidov_byudzhetov", {})
    assert rezultat is not None
