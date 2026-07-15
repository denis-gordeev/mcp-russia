"""Интеграционные тесты для модуля Минобрнауки."""

import pytest
from fastmcp import Client

from mcp_russia.data.minobrnauki.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_tipov_vuzov",
        "spisok_form_obucheniya",
        "spisok_urovney_obrazovaniya",
        "spisok_otrasley_nauki",
        "spisok_tipov_grantov",
        "spisok_statusov_akkreditatsii",
        "spisok_federalnyh_okrugov",
        "info_vuza",
        "programmy_vuza",
        "granty_i_isledovaniya",
        "reyting_vuzov",
        "aspirantura",
        "poisk_licenziy",
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

    ozhidayemyy = {"analiz_vuza", "obzor_nauchnyh_grantov"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_tool_spisok_tipov_vuzov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_vuzov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Университет" in tekst


async def test_tool_info_vuza(klient):
    async with klient:
        rezultat = await klient.call_tool("info_vuza", {"nazvanie": "МГУ"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "не найден" in tekst or "не найдена" in tekst or "zaglushka" in tekst.lower()
