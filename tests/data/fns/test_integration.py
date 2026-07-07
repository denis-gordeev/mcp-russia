"""Интеграционные тесты для модуля ФНС."""

import pytest
from fastmcp import Client

from mcp_russia.data.fns.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_nalogovyh_rezhimov",
        "spisok_vidov_nalogov",
        "spisok_tipov_proverok",
        "spisok_statusov_organizaciy",
        "spisok_kategoriy_nalogoplatelshchikov",
        "info_organizacii",
        "info_ip",
        "proverki_organizacii",
        "nalogovye_nachisleniya",
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

    ozhidayemyy = {"analiz_nalogoplatelshchika", "obzor_rezhimov_nalogooblozheniya"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_nalogovyh_rezhimov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_nalogovyh_rezhimov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ОСНО" in tekst


async def test_spisok_vidov_nalogov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_vidov_nalogov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "НДС" in tekst
