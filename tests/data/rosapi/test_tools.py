"""Тесты инструментов модуля RosAPI."""

from unittest.mock import AsyncMock, patch

import pytest

from mcp_russia.data.rosapi import tools as rosapi_tools
from mcp_russia.data.rosapi.client import _dadata_headers
from mcp_russia.data.rosapi.schemas import AdresRF, BankRF, Organizatsiya
from mcp_russia.exceptions import AuthError


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_konsul_adres_po_indeksu_success():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "consult_address_by_postal",
        return_value=AdresRF(
            postal_code="101000",
            region="г Москва",
            city="Москва",
            street="Красная площадь",
            house="1",
            full_address="г Москва, Красная площадь, д 1",
        ),
    ):
        result = await rosapi_tools.konsul_adres_po_indeksu("101000", ctx)
    assert "101000" in result
    assert "Москва" in result
    assert "Dadata" in result


async def test_konsul_adres_po_indeksu_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "consult_address_by_postal",
        return_value={"error": "Адрес по индексу 000000 не найден"},
    ):
        result = await rosapi_tools.konsul_adres_po_indeksu("000000", ctx)
    assert "000000" in result
    assert "Dadata" in result or "API" in result


async def test_poisk_adresa_empty():
    ctx = _mock_ctx()
    with patch.object(rosapi_tools.client, "search_address", return_value=[]):
        result = await rosapi_tools.poisk_adresa("несуществующий адрес", ctx)
    assert "не найден" in result


async def test_poisk_adresa_success():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "search_address",
        return_value=[
            {
                "value": "г Москва, Красная площадь",
                "postal_code": "101000",
                "region": "г Москва",
                "city": "Москва",
                "street": "Красная площадь",
                "house": "",
                "fias_id": "abc123",
            }
        ],
    ):
        result = await rosapi_tools.poisk_adresa("Красная площадь", ctx)
    assert "Красная площадь" in result
    assert "Dadata" in result


async def test_poisk_org_po_inn_success():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_org_by_inn",
        return_value=Organizatsiya(
            inn="7707083893",
            kpp="773601001",
            ogrn="1027700132195",
            name_full="Публичное акционерное общество «Сбербанк России»",
            name_short="ПАО Сбербанк",
            status="ACTIVE",
            address="г Москва, ул Вавилова, д 19",
            director="Греф Герман Оскарович",
            registration_date="2002-08-23",
        ),
    ):
        result = await rosapi_tools.poisk_org_po_inn("7707083893", ctx)
    assert "7707083893" in result
    assert "Сбербанк" in result
    assert "Действующая" in result


async def test_poisk_org_po_inn_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_org_by_inn",
        return_value={"error": "Не удалось подключиться к API Dadata"},
    ):
        result = await rosapi_tools.poisk_org_po_inn("0000000000", ctx)
    assert "Dadata" in result or "API" in result


async def test_poisk_org_po_ogrn_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_org_by_ogrn",
        return_value={"error": "не найдена"},
    ):
        result = await rosapi_tools.poisk_org_po_ogrn("0000000000000", ctx)
    assert "0000000000000" in result


async def test_spisok_bankov():
    ctx = _mock_ctx()
    result = await rosapi_tools.spisok_bankov(ctx)
    assert "Сбербанк" in result
    assert "ВТБ" in result
    assert "БИК" in result


async def test_konsul_bank_po_bik_dadata():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_bank_by_bik",
        return_value=BankRF(
            bik="044525225",
            name="Публичное акционерное общество «Сбербанк России»",
            name_short="ПАО Сбербанк",
            city="Москва",
            swift="SABRRUMM",
        ),
    ):
        result = await rosapi_tools.konsul_bank_po_bik("044525225", ctx)
    assert "Сбербанк" in result
    assert "Dadata" in result


async def test_konsul_bank_po_bik_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_bank_by_bik",
        return_value={"error": "Банк с БИК 000000000 не найден"},
    ):
        result = await rosapi_tools.konsul_bank_po_bik("000000000", ctx)
    assert "не найден" in result


async def test_prazdniki_rf():
    ctx = _mock_ctx()
    result = await rosapi_tools.prazdniki_rf(god=2025, ctx=ctx)
    assert "Новый год" in result
    assert "День Победы" in result
    assert "2025" in result


async def test_prazdniki_rf_default_year():
    ctx = _mock_ctx()
    result = await rosapi_tools.prazdniki_rf(ctx=ctx)
    assert "Новый год" in result


async def test_nalogovye_stavki():
    ctx = _mock_ctx()
    result = await rosapi_tools.nalogovye_stavki(ctx)
    assert "НДС" in result
    assert "20%" in result
    assert "НДФЛ" in result
    assert "13%" in result


async def test_dadata_headers_raises_auth_error_without_key():
    with patch("mcp_russia.data.rosapi.client.DADATA_API_KEY", ""), \
         pytest.raises(AuthError, match="MCP_RUSSIA_DADATA_API_KEY"):
        _dadata_headers()


async def test_dadata_headers_with_key():
    with patch("mcp_russia.data.rosapi.client.DADATA_API_KEY", "test-key"):
        headers = _dadata_headers()
        assert headers["Authorization"] == "Token test-key"
