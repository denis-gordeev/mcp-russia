"""Интеграционные тесты для модуля ГИБДД/МВД."""

from unittest.mock import patch

import pytest
from fastmcp import Client

from mcp_russia.data.gibdd.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_tipov_ts",
        "spisok_kategoriyy_vu",
        "spisok_vidov_narusheniy",
        "spisok_statusov_shtrafov",
        "spisok_tipov_dtp",
        "spisok_regionov_registratsii",
        "info_ts",
        "info_vu",
        "shtrafy_po_ts",
        "shtrafy_po_vu",
        "statistika_dtp",
        "istoriya_registraciy",
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
    prompt_names = {p.name for p in prompty}

    ozhidayemyy = {"analiz_transportnogo_sredstva", "analiz_voditelya"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_tool_spisok_tipov_ts(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_tipov_ts", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "Легковой" in tekst


async def test_tool_info_ts(klient):
    from mcp_russia.data.gibdd import tools as gibdd_tools

    with patch.object(gibdd_tools, "_polnaya_proverka_ts", return_value=([], [], [], [])):
        async with klient:
            rezultat = await klient.call_tool("info_ts", {"vin": "XTA21140052XXXXXX"})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "не найден" in tekst
