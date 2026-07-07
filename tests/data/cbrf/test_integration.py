"""Интеграционные тесты для модуля ЦБ РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.cbrf.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "tekushchie_kursy",
        "uznat_kurs_valyuty",
        "spisok_valyut",
        "konvertirovat_valyutu",
        "kursy_po_stranam",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://valyuty",
        "data://osnovnye",
        "data://spravochnik",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_valyut", "obzor_ekonomiki"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_valyut(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_valyut", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "USD" in tekst or "валют" in tekst


async def test_uznat_kurs_valyuty(klient):
    async with klient:
        rezultat = await klient.call_tool("uznat_kurs_valyuty", {"kod": "USD"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "USD" in tekst or "ЦБ РФ" in tekst or "не найдена" in tekst


async def test_kursy_po_stranam(klient):
    async with klient:
        rezultat = await klient.call_tool("kursy_po_stranam", {})
    assert rezultat is not None
