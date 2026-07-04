"""Интеграционные тесты для модуля Роскомнадзора."""

import pytest
from fastmcp import Client

from mcp_russia.data.roskomnadzor.server import mcp


@pytest.fixture
def klient():
    return Client(mcp)


async def test_instrumenty_zaregistrirovany(klient):
    async with klient:
        instrumenty = await klient.list_tools()
    imena_instrumentov = {t.name for t in instrumenty}

    ozhidayemyy = {
        "spisok_napravleniy",
        "spisok_tipov_licenziy",
        "spisok_kategoriy_narusheniy",
        "spisok_reestrov",
        "spisok_tipov_smi",
        "spisok_kategoriy_pd_operatorov",
        "info_licenzii",
        "poisk_smi",
        "info_operatora_pd",
        "poisk_narusheniy",
        "proverka_blokirovki",
        "poisk_ori",
        "zapisi_reestra",
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

    ozhidayemyy = {"analiz_narusheniya", "obzor_reestrov"}
    assert ozhidayemyy.issubset(prompt_names), f"Отсутствуют промпты: {ozhidayemyy - prompt_names}"


async def test_spisok_reestrov(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_reestrov", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "запрещённых сайтов" in tekst


async def test_spisok_kategoriy_narusheniy(klient):
    async with klient:
        rezultat = await klient.call_tool("spisok_kategoriy_narusheniy", {})
    assert rezultat is not None
    tekst = str(rezultat)
    assert "персональных данных" in tekst
