"""Интеграционные тесты для модуля Официальные публикации РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.publikatsii.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_tipov_aktov",
        "spisok_otrasley",
        "spisok_istochnikov",
        "spisok_statusov",
        "info_normativnogo_akta",
        "info_zakonproekta",
        "poisk_aktov",
        "publikatsii_po_datam",
        "izmeneniya_akta",
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
        "data://poryadok-opublikovaniya",
        "data://struktura-zakonodatelstva",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_normativnogo_akta", "obzor_zakonodatelstva"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_tipov_aktov(klient):
    """Проверка работы инструмента spisok_tipov_aktov."""
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_aktov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Федеральный закон" in tekst or "Указ" in tekst


async def test_spisok_otrasley(klient):
    """Проверка работы инструмента spisok_otrasley."""
    async with klient:
        rezultat = await klient.call_tool("spisok_otrasley", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Гражданское" in tekst or "Уголовное" in tekst


async def test_spisok_statusov(klient):
    """Проверка работы инструмента spisok_statusov."""
    async with klient:
        rezultat = await klient.call_tool("spisok_statusov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Действующий" in tekst or "Утратил" in tekst
