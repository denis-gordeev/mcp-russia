"""Тесты инструментов модуля ЦБ РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.cbrf import tools as cbrf_tools
from mcp_russia.data.cbrf.schemas import ZnachenieValyuty


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


def _mock_valyuta(
    kod="USD",
    nazvanie="Доллар США",
    nominal=1,
    znachenie=90.0,
    predydushchee_znachenie=89.0,
    data="2025-01-15",
):
    return ZnachenieValyuty(
        kod=kod,
        nazvanie=nazvanie,
        nominal=nominal,
        znachenie=znachenie,
        predydushchee_znachenie=predydushchee_znachenie,
        data=data,
    )


async def test_tekushchie_kursy():
    ctx = _mock_ctx()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_valyuta("EUR", "Евро", 1, 98.0, 97.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=valyuty):
        result = await cbrf_tools.tekushchie_kursy(ctx)
    assert "ЦБ РФ" in result
    assert "USD" in result
    assert "EUR" in result


async def test_tekushchie_kursy_empty():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=[]):
        result = await cbrf_tools.tekushchie_kursy(ctx)
    assert "Не удалось" in result


async def test_uznat_kurs_valyuty():
    ctx = _mock_ctx()
    valyuta = _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        result = await cbrf_tools.uznat_kurs_valyuty("USD", ctx)
    assert "Доллар США" in result
    assert "USD" in result
    assert "90" in result


async def test_uznat_kurs_valyuty_not_found():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        result = await cbrf_tools.uznat_kurs_valyuty("XYZ", ctx)
    assert "не найдена" in result


async def test_spisok_valyut():
    ctx = _mock_ctx()
    raw = {
        "Valute": {
            "USD": {"Name": "Доллар США", "Nominal": 1, "Value": 90.0},
            "EUR": {"Name": "Евро", "Nominal": 1, "Value": 98.0},
        }
    }
    with patch.object(cbrf_tools.client, "poluchit_vse_valyuty", return_value=raw):
        result = await cbrf_tools.spisok_valyut(ctx)
    assert "2 валют" in result
    assert "USD" in result
    assert "EUR" in result


async def test_konvertirovat_valyutu():
    ctx = _mock_ctx()
    valyuta = _mock_valyuta("USD", "Доллар США", 1, 90.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        result = await cbrf_tools.konvertirovat_valyutu("USD", 100, ctx)
    assert "9.000" in result or "9 000" in result or "9000" in result
    assert "Конвертация" in result


async def test_konvertirovat_valyutu_not_found():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        result = await cbrf_tools.konvertirovat_valyutu("XYZ", 100, ctx)
    assert "не найдена" in result


async def test_sravnit_valyuty():
    ctx = _mock_ctx()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_valyuta("EUR", "Евро", 1, 98.0, 97.0),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        result = await cbrf_tools.sravnit_valyuty(["USD", "EUR"], ctx)
    assert "Сравнение" in result
    assert "USD" in result
    assert "EUR" in result


async def test_sravnit_valyuty_default():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=[]):
        result = await cbrf_tools.sravnit_valyuty(ctx=ctx)
    assert "Не удалось" in result


async def test_sravnit_valyuty_too_many():
    codes = [f"C{i}" for i in range(11)]
    result = await cbrf_tools.sravnit_valyuty(codes)
    assert "не более 10" in result


async def test_kursy_po_stranam():
    ctx = _mock_ctx()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0),
        _mock_valyuta("CNY", "Китайский юань", 1, 12.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        result = await cbrf_tools.kursy_po_stranam(ctx)
    assert "стран" in result.lower() or "партнёр" in result.lower()
    assert "USD" in result
