"""Тесты инструментов модуля RosAPI."""

from unittest.mock import AsyncMock, patch

import pytest

from mcp_russia.data.rosapi import tools as rosapi_tools
from mcp_russia.data.rosapi.client import _zagolovki_dadaty
from mcp_russia.data.rosapi.schemas import AdresRF, BankRF, Organizatsiya
from mcp_russia.exceptions import OshibkaAutentifikatsii


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_konsul_adres_po_indeksu_uspekh():
    ctx = _maket_konteksta()
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
        result = await rosapi_tools.konsul_adres_po_indeksu("101000", ctx)
    assert "101000" in result
    assert "Москва" in result
    assert "Dadata" in result


async def test_konsul_adres_po_indeksu_oshibka():
    ctx = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "konsultirovat_adres_po_pochtovomu",
        return_value={"oshibka": "Адрес по индексу 000000 не найден"},
    ):
        result = await rosapi_tools.konsul_adres_po_indeksu("000000", ctx)
    assert "000000" in result
    assert "Dadata" in result or "API" in result


async def test_poisk_adresa_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosapi_tools.client, "poisk_adresa", return_value=[]):
        result = await rosapi_tools.poisk_adresa("несуществующий адрес", ctx)
    assert "не найден" in result


async def test_poisk_adresa_uspekh():
    ctx = _maket_konteksta()
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
        result = await rosapi_tools.poisk_adresa("Красная площадь", ctx)
    assert "Красная площадь" in result
    assert "Dadata" in result


async def test_poisk_org_po_inn_uspekh():
    ctx = _maket_konteksta()
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
        result = await rosapi_tools.poisk_org_po_inn("7707083893", ctx)
    assert "7707083893" in result
    assert "Сбербанк" in result
    assert "Действующая" in result


async def test_poisk_org_po_inn_oshibka():
    ctx = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_organizatsiyu_po_inn",
        return_value={"oshibka": "Не удалось подключиться к API Dadata"},
    ):
        result = await rosapi_tools.poisk_org_po_inn("0000000000", ctx)
    assert "Dadata" in result or "API" in result


async def test_poisk_org_po_ogrn_oshibka():
    ctx = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_organizatsiyu_po_ogrn",
        return_value={"oshibka": "не найдена"},
    ):
        result = await rosapi_tools.poisk_org_po_ogrn("0000000000000", ctx)
    assert "0000000000000" in result


async def test_spisok_bankov():
    ctx = _maket_konteksta()
    result = await rosapi_tools.spisok_bankov(ctx)
    assert "Сбербанк" in result
    assert "ВТБ" in result
    assert "БИК" in result


async def test_konsul_bank_po_bik_dadata():
    ctx = _maket_konteksta()
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
        result = await rosapi_tools.konsul_bank_po_bik("044525225", ctx)
    assert "Сбербанк" in result
    assert "Dadata" in result


async def test_konsul_bank_po_bik_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(
        rosapi_tools.client,
        "nayti_bank_po_bik",
        return_value={"oshibka": "Банк с БИК 000000000 не найден"},
    ):
        result = await rosapi_tools.konsul_bank_po_bik("000000000", ctx)
    assert "не найден" in result


async def test_prazdniki_rf():
    ctx = _maket_konteksta()
    result = await rosapi_tools.prazdniki_rf(god=2025, ctx=ctx)
    assert "Новый год" in result
    assert "День Победы" in result
    assert "2025" in result


async def test_prazdniki_rf_default_year():
    ctx = _maket_konteksta()
    result = await rosapi_tools.prazdniki_rf(ctx=ctx)
    assert "Новый год" in result


async def test_nalogovye_stavki():
    ctx = _maket_konteksta()
    result = await rosapi_tools.nalogovye_stavki(ctx)
    assert "НДС" in result
    assert "20%" in result
    assert "НДФЛ" in result
    assert "13%" in result


async def test_zagolovki_dadaty_raises_auth_error_without_key():
    with (
        patch("mcp_russia.data.rosapi.client.KLYUCH_DADATA_API", ""),
        pytest.raises(OshibkaAutentifikatsii, match="MCP_RUSSIA_DADATA_API_KEY"),
    ):
        _zagolovki_dadaty()


async def test_zagolovki_dadaty_with_key():
    with patch("mcp_russia.data.rosapi.client.KLYUCH_DADATA_API", "test-key"):
        headers = _zagolovki_dadaty()
        assert headers["Authorization"] == "Token test-key"
