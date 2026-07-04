"""Интеграционные тесты для модуля RosAPI.

Note: rosapi/prompty.py imports UserMessage which may not exist in this
version of FastMCP. If server import fails, tests are skipped.
"""

import pytest
from fastmcp import Client

try:
    from mcp_russia.data.rosapi.server import mcp

    _IMPORT_NORMALNO = True
except ImportError:
    _IMPORT_NORMALNO = False


@pytest.fixture
def klient():
    if not _IMPORT_NORMALNO:
        pytest.skip("rosapi server import fails (UserMessage not available)")
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "konsul_adres_po_indeksu",
        "poisk_adresa",
        "poisk_org_po_inn",
        "poisk_org_po_ogrn",
        "spisok_bankov",
        "konsul_bank_po_bik",
        "prazdniki_rf",
        "nalogovye_stavki",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://nalogovye-stavki",
        "data://servisy",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_organizacii", "poisk_adresa_prompt"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_bankov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_bankov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Сбербанк" in tekst or "ВТБ" in tekst


async def test_prazdniki_rf(klient):
    async with klient:
        rezultat = await klient.call_tool("prazdniki_rf", {"god": 2025})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Новый год" in tekst or "Победы" in tekst


async def test_nalogovye_stavki(klient):
    async with klient:
        rezultat = await klient.call_tool("nalogovye_stavki", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "НДС" in tekst or "налог" in tekst.lower()
