"""Тесты инструментов модуля ЦБ РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.cbrf import tools as cbrf_tools
from mcp_russia.data.cbrf.schemas import ZnachenieValyuty


def _maket_konteksta():
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
    ctx = _maket_konteksta()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_valyuta("EUR", "Евро", 1, 98.0, 97.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=valyuty):
        rezultat = await cbrf_tools.tekushchie_kursy(ctx)
    assert "ЦБ РФ" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_tekushchie_kursy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=[]):
        rezultat = await cbrf_tools.tekushchie_kursy(ctx)
    assert "Не удалось" in rezultat


async def test_uznat_kurs_valyuty():
    ctx = _maket_konteksta()
    valyuta = _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        rezultat = await cbrf_tools.uznat_kurs_valyuty("USD", ctx)
    assert "Доллар США" in rezultat
    assert "USD" in rezultat
    assert "90" in rezultat


async def test_uznat_kurs_valyuty_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        rezultat = await cbrf_tools.uznat_kurs_valyuty("XYZ", ctx)
    assert "не найдена" in rezultat


async def test_spisok_valyut():
    ctx = _maket_konteksta()
    raw = {
        "Valute": {
            "USD": {"Name": "Доллар США", "Nominal": 1, "Value": 90.0},
            "EUR": {"Name": "Евро", "Nominal": 1, "Value": 98.0},
        }
    }
    with patch.object(cbrf_tools.client, "poluchit_vse_valyuty", return_value=raw):
        rezultat = await cbrf_tools.spisok_valyut(ctx)
    assert "2 валют" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_konvertirovat_valyutu():
    ctx = _maket_konteksta()
    valyuta = _mock_valyuta("USD", "Доллар США", 1, 90.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        rezultat = await cbrf_tools.konvertirovat_valyutu("USD", 100, ctx)
    assert "9.000" in rezultat or "9 000" in rezultat or "9000" in rezultat
    assert "Конвертация" in rezultat


async def test_konvertirovat_valyutu_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        rezultat = await cbrf_tools.konvertirovat_valyutu("XYZ", 100, ctx)
    assert "не найдена" in rezultat


async def test_sravnit_valyuty():
    ctx = _maket_konteksta()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_valyuta("EUR", "Евро", 1, 98.0, 97.0),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        rezultat = await cbrf_tools.sravnit_valyuty(["USD", "EUR"], ctx)
    assert "Сравнение" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_sravnit_valyuty_po_umolchaniyu():
    ctx = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=[]):
        rezultat = await cbrf_tools.sravnit_valyuty(ctx=ctx)
    assert "Не удалось" in rezultat


async def test_sravnit_valyuty_slishkom_mnogo():
    codes = [f"C{i}" for i in range(11)]
    rezultat = await cbrf_tools.sravnit_valyuty(codes)
    assert "не более 10" in rezultat


async def test_kursy_po_stranam():
    ctx = _maket_konteksta()
    valyuty = [
        _mock_valyuta("USD", "Доллар США", 1, 90.0),
        _mock_valyuta("CNY", "Китайский юань", 1, 12.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        rezultat = await cbrf_tools.kursy_po_stranam(ctx)
    assert "стран" in rezultat.lower() or "партнёр" in rezultat.lower()
    assert "USD" in rezultat
