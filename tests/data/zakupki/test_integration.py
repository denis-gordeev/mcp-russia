"""Интеграционные тесты для модуля Закупки (ЕИС)."""

import pytest
from fastmcp import Client

from mcp_russia.data.zakupki.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "poisk_zakupok",
        "info_zakupki",
        "poisk_kontraktov",
        "info_zakazchika",
        "info_postavshchika",
        "statusy_zakupok",
        "sposoby_zakupok",
        "plany_zakupok",
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

    ozhidayemyy = {"analiz_zakupki", "obzor_zakupok"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_statusy_zakupok(klient):
    """Проверка работы инструмента statusy_zakupok."""
    async with klient:
        rezultat = await klient.call_tool("statusy_zakupok", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Планирование" in tekst or "Завершена" in tekst


async def test_sposoby_zakupok(klient):
    """Проверка работы инструмента sposoby_zakupok."""
    async with klient:
        rezultat = await klient.call_tool("sposoby_zakupok", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Электронный аукцион" in tekst or "аукцион" in tekst.lower()
