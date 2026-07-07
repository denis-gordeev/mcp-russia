"""Интеграционные тесты для модуля Счётная палата РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosaudit.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_napravleniy",
        "spisok_tipov_meropriyatiy",
        "spisok_subiektov_audita",
        "poisk_kontrolnyh_meropriyatiy",
        "info_kontrolnogo_meropriyatiya",
        "info_auditorskogo_zaklyucheniya",
        "ispolnenie_byudzheta",
        "poisk_narusheniy",
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
        "data://zakonodatelstvo",
        "data://struktura",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_auditorskogo_zaklyucheniya", "obzor_ispolneniya_byudzheta"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_napravleniy(klient):
    """Проверка работы инструмента spisok_napravleniy."""
    async with klient:
        rezultat = await klient.call_tool("spisok_napravleniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "бюджет" in tekst.lower() or "Контроль" in tekst


async def test_spisok_tipov_meropriyatiy(klient):
    """Проверка работы инструмента spisok_tipov_meropriyatiy."""
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_meropriyatiy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Проверка" in tekst or "Экспертиза" in tekst


async def test_spisok_subiektov_audita(klient):
    """Проверка работы инструмента spisok_subiektov_audita."""
    async with klient:
        rezultat = await klient.call_tool("spisok_subiektov_audita", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Федеральные" in tekst or "Государственные" in tekst
