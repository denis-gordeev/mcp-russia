"""Интеграционные тесты для модуля Росводресурсы."""

import pytest
from fastmcp import Client

from mcp_russia.data.rosvodresursy.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    """Проверка регистрации инструментов."""
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_basseynovykh_okrugov",
        "spisok_tipov_vodnykh_obektov",
        "spisok_vodokhranilishch",
        "poisk_vodnykh_obektov",
        "info_vodnogo_obekta",
        "gidro_monitoring",
        "info_vodokhranilishcha",
        "vodopolzovanie_regionov",
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
        "data://basseynovye-okruga",
        "data://vodokhozyaystvo",
    }
    assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют ресурсы: {ozhidayemyy - adresa_uri}"


async def test_prompty_zaregistrirovany(klient):
    """Проверка регистрации промптов."""
    async with klient:
        prompty = await klient.list_prompts()
    prompt_names = {p.name for p in prompty}

    ozhidayemyy = {"analiz_vodnogo_obekta", "obzor_vodokhranilishch"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_spisok_basseynovykh_okrugov(klient):
    """Проверка работы инструмента spisok_basseynovykh_okrugov."""
    async with klient:
        rezultat = await klient.call_tool("spisok_basseynovykh_okrugov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Волжский" in tekst or "Донской" in tekst


async def test_spisok_vodokhranilishch(klient):
    """Проверка работы инструмента spisok_vodokhranilishch."""
    async with klient:
        rezultat = await klient.call_tool("spisok_vodokhranilishch", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Братское" in tekst or "Куйбышевское" in tekst


async def test_gidro_monitoring(klient):
    async with klient:
        rezultat = await klient.call_tool("gidro_monitoring", {"identifikator_posta": ""})
    assert rezultat is not None
