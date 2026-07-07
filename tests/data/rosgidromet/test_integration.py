"""Интеграционные тесты для модуля Росгидромет."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosgidromet.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_stanciy",
        "spisok_tipov_dannykh",
        "pogoda_seychas",
        "prognoz_pogody",
        "ekologiya_regiona",
        "preduprezhdeniya",
        "sputnik_monitoring",
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
        "data://metodologiya",
        "data://opasnye-yavleniya",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    imena_promtov = {p.name for p in prompty}

    ozhidayemyy = {"analiz_pogody_regiona", "obzor_ekologii"}
    assert ozhidayemyy.issubset(imena_promtov), (
        f"Отсутствуют промпты: {ozhidayemyy - imena_promtov}"
    )


async def test_spisok_stanciy(klient):
    """Проверка работы инструмента spisok_stanciy."""
    async with klient:
        rezultat = await klient.call_tool("spisok_stanciy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Москва" in tekst or "Санкт-Петербург" in tekst


async def test_spisok_tipov_dannykh(klient):
    """Проверка работы инструмента spisok_tipov_dannykh."""
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_dannykh", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "погода" in tekst.lower() or "Температура" in tekst


async def test_preduprezhdeniya(klient):
    """Проверка работы инструмента preduprezhdeniya."""
    async with klient:
        rezultat = await klient.call_tool("preduprezhdeniya", {})
    assert rezultat is not None
