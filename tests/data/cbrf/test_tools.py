"""Тесты инструментов модуля ЦБ РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.cbrf import tools as cbrf_tools
from mcp_russia.data.cbrf.schemas import ZnachenieValyuty


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


def _maket_valyuty(
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
    kontekst = _maket_konteksta()
    valyuty = [
        _maket_valyuty("USD", "Доллар США", 1, 90.0, 89.0),
        _maket_valyuty("EUR", "Евро", 1, 98.0, 97.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=valyuty):
        rezultat = await cbrf_tools.tekushchie_kursy(kontekst)
    assert "ЦБ РФ" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_tekushchie_kursy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_osnovnye_valyuty", return_value=[]):
        rezultat = await cbrf_tools.tekushchie_kursy(kontekst)
    assert "Не удалось" in rezultat


async def test_uznat_kurs_valyuty():
    kontekst = _maket_konteksta()
    valyuta = _maket_valyuty("USD", "Доллар США", 1, 90.0, 89.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        rezultat = await cbrf_tools.uznat_kurs_valyuty("USD", kontekst)
    assert "Доллар США" in rezultat
    assert "USD" in rezultat
    assert "90" in rezultat


async def test_uznat_kurs_valyuty_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        rezultat = await cbrf_tools.uznat_kurs_valyuty("XYZ", kontekst)
    assert "не найдена" in rezultat


async def test_spisok_valyut():
    kontekst = _maket_konteksta()
    syryye_dannye = {
        "Valute": {
            "USD": {"Name": "Доллар США", "Nominal": 1, "Value": 90.0},
            "EUR": {"Name": "Евро", "Nominal": 1, "Value": 98.0},
        }
    }
    with patch.object(cbrf_tools.client, "poluchit_vse_valyuty", return_value=syryye_dannye):
        rezultat = await cbrf_tools.spisok_valyut(kontekst)
    assert "2 валют" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_konvertirovat_valyutu():
    kontekst = _maket_konteksta()
    valyuta = _maket_valyuty("USD", "Доллар США", 1, 90.0)
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=valyuta):
        rezultat = await cbrf_tools.konvertirovat_valyutu("USD", 100, kontekst)
    assert "9.000" in rezultat or "9 000" in rezultat or "9000" in rezultat
    assert "Конвертация" in rezultat


async def test_konvertirovat_valyutu_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyutu", return_value=None):
        rezultat = await cbrf_tools.konvertirovat_valyutu("XYZ", 100, kontekst)
    assert "не найдена" in rezultat


async def test_sravnit_valyuty():
    kontekst = _maket_konteksta()
    valyuty = [
        _maket_valyuty("USD", "Доллар США", 1, 90.0, 89.0),
        _maket_valyuty("EUR", "Евро", 1, 98.0, 97.0),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        rezultat = await cbrf_tools.sravnit_valyuty(["USD", "EUR"], kontekst)
    assert "Сравнение" in rezultat
    assert "USD" in rezultat
    assert "EUR" in rezultat


async def test_sravnit_valyuty_po_umolchaniyu():
    kontekst = _maket_konteksta()
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=[]):
        rezultat = await cbrf_tools.sravnit_valyuty(kontekst=kontekst)
    assert "Не удалось" in rezultat


async def test_sravnit_valyuty_slishkom_mnogo():
    kody = [f"C{i}" for i in range(11)]
    rezultat = await cbrf_tools.sravnit_valyuty(kody)
    assert "не более 10" in rezultat


async def test_kursy_po_stranam():
    kontekst = _maket_konteksta()
    valyuty = [
        _maket_valyuty("USD", "Доллар США", 1, 90.0),
        _maket_valyuty("CNY", "Китайский юань", 1, 12.5),
    ]
    with patch.object(cbrf_tools.client, "poluchit_valyuty_spisok", return_value=valyuty):
        rezultat = await cbrf_tools.kursy_po_stranam(kontekst)
    assert "стран" in rezultat.lower() or "партнёр" in rezultat.lower()
    assert "USD" in rezultat
