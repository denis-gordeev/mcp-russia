"""Тесты инструментов модуля RosAPI."""

from unittest.mock import AsyncMock, patch

import pytest

from mcp_russia.data.rosapi import tools as rosapi_tools
from mcp_russia.data.rosapi.client import _zagolovki_dadaty
from mcp_russia.data.rosapi.schemas import AdresRF, BankRF, Organizatsiya
from mcp_russia.exceptions import OshibkaAutentifikatsii


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_konsul_adres_po_indeksu_uspekh():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "konsultirovat_adres_po_pochtovomu",
        return_value=AdresRF(
            pochtovyy_indeks="101000",
            subiekt="г Москва",
            gorod="Москва",
            ulitsa="Красная площадь",
            dom="1",
            polnyy_adres="г Москва, Красная площадь, д 1",
        ),
    ):
        rezultat = await rosapi_tools.konsul_adres_po_indeksu("101000", kontekst)
    assert "101000" in rezultat
    assert "Москва" in rezultat
    assert "Dadata" in rezultat


async def test_konsul_adres_po_indeksu_oshibka():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "konsultirovat_adres_po_pochtovomu",
        return_value={"oshibka": "Адрес по индексу 000000 не найден"},
    ):
        rezultat = await rosapi_tools.konsul_adres_po_indeksu("000000", kontekst)
    assert "000000" in rezultat
    assert "Dadata" in rezultat or "API" in rezultat


async def test_poisk_adresa_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rosapi_tools.client, "poisk_adresa", return_value=[]):
        rezultat = await rosapi_tools.poisk_adresa("несуществующий адрес", kontekst)
    assert "не найден" in rezultat


async def test_poisk_adresa_uspekh():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "poisk_adresa",
        return_value=[
            {
                "znachenie": "г Москва, Красная площадь",
                "pochtovyy_indeks": "101000",
                "subiekt": "г Москва",
                "gorod": "Москва",
                "ulitsa": "Красная площадь",
                "dom": "",
                "identifikator_fias": "abc123",
            }
        ],
    ):
        rezultat = await rosapi_tools.poisk_adresa("Красная площадь", kontekst)
    assert "Красная площадь" in rezultat
    assert "Dadata" in rezultat


async def test_poisk_org_po_inn_uspekh():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_organizatsiyu_po_inn",
        return_value=Organizatsiya(
            inn="7707083893",
            kpp="773601001",
            ogrn="1027700132195",
            nazvanie_polnoe="Публичное акционерное общество «Сбербанк России»",
            nazvanie_kratkoe="ПАО Сбербанк",
            sostoyanie="ACTIVE",
            adres="г Москва, ул Вавилова, д 19",
            rukovoditel="Греф Герман Оскарович",
            data_registratsii="2002-08-23",
        ),
    ):
        rezultat = await rosapi_tools.poisk_org_po_inn("7707083893", kontekst)
    assert "7707083893" in rezultat
    assert "Сбербанк" in rezultat
    assert "Действующая" in rezultat


async def test_poisk_org_po_inn_oshibka():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_organizatsiyu_po_inn",
        return_value={"oshibka": "Не удалось подключиться к API Dadata"},
    ):
        rezultat = await rosapi_tools.poisk_org_po_inn("0000000000", kontekst)
    assert "Dadata" in rezultat or "API" in rezultat


async def test_poisk_org_po_ogrn_oshibka():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_organizatsiyu_po_ogrn",
        return_value={"oshibka": "не найдена"},
    ):
        rezultat = await rosapi_tools.poisk_org_po_ogrn("0000000000000", kontekst)
    assert "0000000000000" in rezultat


async def test_spisok_bankov():
    kontekst = _maket_konteksta()
    rezultat = await rosapi_tools.spisok_bankov(kontekst)
    assert "Сбербанк" in rezultat
    assert "ВТБ" in rezultat
    assert "БИК" in rezultat


async def test_konsul_bank_po_bik_dadata():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_bank_po_bik",
        return_value=BankRF(
            bik="044525225",
            nazvanie="Публичное акционерное общество «Сбербанк России»",
            nazvanie_kratkoe="ПАО Сбербанк",
            gorod="Москва",
            svift="SABRRUMM",
        ),
    ):
        rezultat = await rosapi_tools.konsul_bank_po_bik("044525225", kontekst)
    assert "Сбербанк" in rezultat
    assert "Dadata" in rezultat


async def test_konsul_bank_po_bik_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_bank_po_bik",
        return_value={"oshibka": "Банк с БИК 000000000 не найден"},
    ):
        rezultat = await rosapi_tools.konsul_bank_po_bik("000000000", kontekst)
    assert "не найден" in rezultat


async def test_prazdniki_rf():
    kontekst = _maket_konteksta()
    rezultat = await rosapi_tools.prazdniki_rf(god=2025, kontekst=kontekst)
    assert "Новый год" in rezultat
    assert "День Победы" in rezultat
    assert "2025" in rezultat


async def test_prazdniki_rf_god_po_umolchaniyu():
    kontekst = _maket_konteksta()
    rezultat = await rosapi_tools.prazdniki_rf(kontekst=kontekst)
    assert "Новый год" in rezultat


async def test_nalogovye_stavki():
    kontekst = _maket_konteksta()
    rezultat = await rosapi_tools.nalogovye_stavki(kontekst)
    assert "НДС" in rezultat
    assert "20%" in rezultat
    assert "НДФЛ" in rezultat
    assert "13%" in rezultat


async def test_zagolovki_dadaty_vyzyvaet_oshibku_bez_klyucha():
    with (
        patch("mcp_russia.data.rosapi.client.KLYUCH_DADATA_API", ""),
        pytest.raises(OshibkaAutentifikatsii, match="MCP_RUSSIA_DADATA_API_KEY"),
    ):
        _zagolovki_dadaty()


async def test_zagolovki_dadaty_s_klyuchom():
    with patch("mcp_russia.data.rosapi.client.KLYUCH_DADATA_API", "proverochnyy-klyuch"):
        zagolovki = _zagolovki_dadaty()
        assert zagolovki["Authorization"] == "Token proverochnyy-klyuch"
