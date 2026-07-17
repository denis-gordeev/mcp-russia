"""Интеграционные тесты для модуля Росреестра."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosreestr.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_tipov_nedvizhimosti",
        "spisok_kategoriy_zemel",
        "spisok_vidov_ispolzovaniya",
        "spisok_statusov_obekta",
        "spisok_form_sobstvennosti",
        "info_obekta",
        "kadastrovaya_stoimost",
        "prava_na_obekt",
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

    ozhidayemyy = {"analiz_nedvizhimosti", "obzor_zemelnogo_uchastka"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_tipov_nedvizhimosti(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_nedvizhimosti", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Земельный участок" in tekst


async def test_spisok_kategoriy_zemel(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_kategoriy_zemel", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "населённых пунктов" in tekst
