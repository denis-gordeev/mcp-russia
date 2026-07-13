"""Тесты инструментов модуля Федеральное казначейство."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.kaznacheistvo import tools as kaznacheistvo_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_vidov_byudzhetov():
    kontekst = _maket_konteksta()
    rezultat = await kaznacheistvo_tools.spisok_vidov_byudzhetov(kontekst)
    assert "бюджет" in rezultat.lower()


async def test_spisok_kategoriy_raskhodov():
    kontekst = _maket_konteksta()
    rezultat = await kaznacheistvo_tools.spisok_kategoriy_raskhodov(kontekst)
    assert "Образование" in rezultat or "Расходы" in rezultat


async def test_ispolnenie_byudzheta_nedostupen():
    kontekst = _maket_konteksta()
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_ispolnenie_byudzheta", return_value=None
    ):
        rezultat = await kaznacheistvo_tools.ispolnenie_byudzheta(kontekst)
    assert isinstance(rezultat, str)


async def test_ispolnenie_byudzheta_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "period": "2025",
        "tip": "Федеральный бюджет",
        "dohody": 28000.5,
        "raskhody": 31000.2,
        "defitsit": -2999.7,
    }
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_ispolnenie_byudzheta", return_value=maket_dannykh
    ):
        rezultat = await kaznacheistvo_tools.ispolnenie_byudzheta(kontekst, god=2025)
    assert "2025" in rezultat


async def test_poisk_uchastnikov_bp_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(kaznacheistvo_tools.client, "poisk_uchastnikov_bp", return_value=[]):
        rezultat = await kaznacheistvo_tools.poisk_uchastnikov_bp(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_uchastnikov_bp_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "inn": "7707083893",
            "nazvanie": "Минфин России",
            "tip_uchastnika": "ГРБС",
            "byudzhet": "Федеральный",
        },
    ]
    with patch.object(
        kaznacheistvo_tools.client, "poisk_uchastnikov_bp", return_value=maket_dannykh
    ):
        rezultat = await kaznacheistvo_tools.poisk_uchastnikov_bp(kontekst, inn="7707083893")
    assert "Минфин" in rezultat


async def test_poisk_uchrezhdeniy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(kaznacheistvo_tools.client, "poisk_uchrezhdeniy", return_value=[]):
        rezultat = await kaznacheistvo_tools.poisk_uchrezhdeniy(kontekst)
    assert isinstance(rezultat, str)


async def test_mezhbyudzhetnye_transferty_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "vid": "Дотация",
            "otpravitel": "Федеральный центр",
            "poluchatel": "Республика Татарстан",
            "summa": 15000.0,
            "god": "2025",
        },
    ]
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_mezhbyudzhetnye", return_value=maket_dannykh
    ):
        rezultat = await kaznacheistvo_tools.mezhbyudzhetnye_transferty(kontekst, god=2025)
    assert "Татарстан" in rezultat
