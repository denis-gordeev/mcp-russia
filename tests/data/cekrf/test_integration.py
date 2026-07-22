"""Интеграционные тесты для модуля ЦИК РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.cekrf.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "tipy_vyborov",
        "subiekty_rf",
        "dolzhnosti_federalnye",
        "partii_rf",
        "gody_vyborov",
        "poisk_kandidata",
        "kandidat_podrobno",
        "rezultaty_vyborov",
        "yavka_i_itogi",
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
        "data://tipy-vyborov",
        "data://subiekty-rf",
        "data://partii-rf",
        "data://svedeniya-ob-api",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_kandidata", "sravnenie_partiy"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_tipy_vyborov(klient):
    """Проверка работы инструмента tipy_vyborov."""
    async with klient:
        rezultat = await klient.call_tool("tipy_vyborov", {})
    assert rezultat is not None
    tekst = str(rezultat.content) if hasattr(rezultat, "content") else str(rezultat)
    assert "Президент" in tekst or "Государственная" in tekst


async def test_subiekty_rf(klient):
    """Проверка работы инструмента subiekty_rf."""
    async with klient:
        rezultat = await klient.call_tool("subiekty_rf", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Москва" in tekst or "Санкт-Петербург" in tekst


async def test_partii_rf(klient):
    """Проверка работы инструмента partii_rf."""
    async with klient:
        rezultat = await klient.call_tool("partii_rf", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Единая Россия" in tekst


async def test_gody_vyborov(klient):
    """Проверка работы инструмента gody_vyborov."""
    async with klient:
        rezultat = await klient.call_tool("gody_vyborov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "2024" in tekst or "2021" in tekst
