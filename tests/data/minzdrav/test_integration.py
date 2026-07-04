"""Интеграционные тесты для модуля Минздрав РФ."""

import pytest
from fastmcp import Client

from mcp_russia.data.minzdrav.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "poisk_med_organizatsiy",
        "info_med_organizatsii",
        "poisk_litsenziy",
        "pokazateli_zdorovya",
        "statistika_zabolevaniy",
        "spravochnik_mo",
        "spravochnik_spetsialnostey",
        "spravochnik_mkb10",
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
        "data://klassifikatsii",
        "data://okruga",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    prompt_names = {p.name for p in prompty}

    ozhidayemyy = {"analiz_zdorovya_regiona", "obzor_med_organizatsiy"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_poisk_med_organizatsiy(klient):
    """Проверка работы инструмента poisk_med_organizatsiy."""
    async with klient:
        rezultat = await klient.call_tool("poisk_med_organizatsiy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Медицинские организации" in tekst or "minzdrav.gov.ru" in tekst


async def test_spravochnik_mo(klient):
    """Проверка работы инструмента spravochnik_mo."""
    async with klient:
        rezultat = await klient.call_tool("spravochnik_mo", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Больница" in tekst or "Поликлиника" in tekst


async def test_pokazateli_zdorovya(klient):
    async with klient:
        rezultat = await klient.call_tool("pokazateli_zdorovya", {"god": 2024})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Показатели" in tekst or "Минздрав" in tekst
