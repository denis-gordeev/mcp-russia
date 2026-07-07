"""Интеграционные тесты для модуля Росстат."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosstat.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
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
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://istochniki",
        "data://metodologiya",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_regiona", "obzor_inflyacii"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_regionov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_regionov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Москва" in tekst or "Санкт-Петербург" in tekst


async def test_pokazateli_rosstata(klient):
    async with klient:
        rezultat = await klient.call_tool("pokazateli_rosstata", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "населени" in tekst.lower() or "показател" in tekst.lower()


async def test_inflyaciya(klient):
    async with klient:
        rezultat = await klient.call_tool("inflyaciya", {"god": "2025"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ИПЦ" in tekst or "Инфляц" in tekst


async def test_vrp_dannye(klient):
    async with klient:
        rezultat = await klient.call_tool("vrp_dannye", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ВРП" in tekst or "Валовой" in tekst


async def test_zarplata_dannye(klient):
    async with klient:
        rezultat = await klient.call_tool("zarplata_dannye", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "заработ" in tekst.lower()


async def test_indikator_dannye(klient):
    async with klient:
        rezultat = await klient.call_tool("indikator_dannye", {"kod": "ipcz"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "ИПЦ" in tekst or "Инфляц" in tekst or "31088" in tekst
