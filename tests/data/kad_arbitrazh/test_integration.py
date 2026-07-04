"""Интеграционные тесты для модуля Картотека арбитражных дел."""

import pytest
from fastmcp import Client

from mcp_russia.data.kad_arbitrazh.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "poisk_del",
        "info_dela",
        "akty_po_delu",
        "storony_dela",
        "spravochnik_kategoriy",
        "spravochnik_instantsiy",
        "spravochnik_statusov",
        "spravochnik_aktov",
    }
    assert ozhidayemyy.issubset(imena_instrumentov), (
        f"Отсутствуют инструменты: {ozhidayemyy - imena_instrumentov}"
    )


async def test_resursy_zaregistrirovany(klient):
    """Проверка регистрации ресурсов."""
    async with klient:
        resursy = await klient.list_resources()
    adresa_uri = {str(r.uri) for r in resursy}

    ozhidayemyy = {
        "data://istochniki",
        "data://sistema",
        "data://kodifikatsiya",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    prompt_names = {p.name for p in prompty}

    ozhidayemyy = {"analiz_dela", "analiz_uchastnika"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_poisk_del(klient):
    """Проверка работы инструмента poisk_del."""
    async with klient:
        rezultat = await klient.call_tool("poisk_del", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Картотека" in tekst or "kad.arbitr.ru" in tekst


async def test_spravochnik_kategoriy(klient):
    """Проверка работы инструмента spravochnik_kategoriy."""
    async with klient:
        rezultat = await klient.call_tool("spravochnik_kategoriy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Банкротство" in tekst or "Налоговые" in tekst


async def test_spravochnik_instantsiy(klient):
    """Проверка работы инструмента spravochnik_instantsiy."""
    async with klient:
        rezultat = await klient.call_tool("spravochnik_instantsiy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "первая инстанция" in tekst or "кассация" in tekst
