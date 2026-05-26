"""Тесты инструментов модуля RosAPI."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.rosapi import tools as rosapi_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_konsul_adres_po_indeksu_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "consult_address_by_postal",
        return_value={"error": "Требуется интеграция"},
    ):
        result = await rosapi_tools.konsul_adres_po_indeksu("101000", ctx)
    assert "101000" in result
    assert "интеграци" in result.lower() or "API" in result


async def test_poisk_adresa_empty():
    ctx = _mock_ctx()
    with patch.object(rosapi_tools.client, "search_address", return_value=[]):
        result = await rosapi_tools.poisk_adresa("Москва, Красная площадь", ctx)
    assert "не найден" in result


async def test_poisk_org_po_inn_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_org_by_inn",
        return_value={"error": "Требуется API-ключ"},
    ):
        result = await rosapi_tools.poisk_org_po_inn("7707083893", ctx)
    assert "7707083893" in result
    assert "API" in result or "ключ" in result.lower()


async def test_poisk_org_po_ogrn_error():
    ctx = _mock_ctx()
    with patch.object(
        rosapi_tools.client,
        "find_org_by_inn",
        return_value={"error": "не найдена"},
    ):
        result = await rosapi_tools.poisk_org_po_ogrn("1027700132195", ctx)
    assert "1027700132195" in result


async def test_spisok_bankov():
    ctx = _mock_ctx()
    result = await rosapi_tools.spisok_bankov(ctx)
    assert "Сбербанк" in result
    assert "ВТБ" in result
    assert "БИК" in result


async def test_konsul_bank_po_bik_found():
    ctx = _mock_ctx()
    result = await rosapi_tools.konsul_bank_po_bik("044525225", ctx)
    assert "Центральн" in result or "Сбербанк" in result


async def test_konsul_bank_po_bik_not_found():
    ctx = _mock_ctx()
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
