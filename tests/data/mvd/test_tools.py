"""Тесты инструментов модуля МВД России."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.mvd import constants as mvd_constants
from mcp_russia.data.mvd import tools as mvd_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_naborov_dannykh():
    kontekst = _maket_konteksta()
    rezultat = await mvd_tools.spisok_naborov_dannykh(kontekst)
    assert "преступност" in rezultat.lower() or "ДТП" in rezultat


async def test_spisok_vidov_prestupleniy():
    kontekst = _maket_konteksta()
    rezultat = await mvd_tools.spisok_vidov_prestupleniy(kontekst)
    assert "Кража" in rezultat or "Мошенничество" in rezultat


async def test_spisok_vidov_dtp():
    kontekst = _maket_konteksta()
    rezultat = await mvd_tools.spisok_vidov_dtp(kontekst)
    assert "Столкнов" in rezultat or "Наезд" in rezultat


async def test_spisok_federalnykh_okrugov():
    kontekst = _maket_konteksta()
    rezultat = await mvd_tools.spisok_federalnykh_okrugov(kontekst)
    assert "Центральн" in rezultat


async def test_statistika_prestupnosti_zapasnoy():
    kontekst = _maket_konteksta()
    with patch.object(mvd_tools.client, "statistika_prestupnosti", return_value=[]):
        rezultat = await mvd_tools.statistika_prestupnosti(kontekst)
    assert "2024" in rezultat or "резервные данные" in rezultat


async def test_statistika_prestupnosti_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "subiekt": "Московская область",
            "god": 2024,
            "zaregistrirovano": 45000,
            "raskryto": 28000,
            "neraskryto": 17000,
            "tyazhkie_osobo_tyazhkie": 8000,
        },
    ]
    with patch.object(mvd_tools.client, "statistika_prestupnosti", return_value=maket_dannykh):
        rezultat = await mvd_tools.statistika_prestupnosti(kontekst)
    assert "Московск" in rezultat


async def test_statistika_dtp_zapasnoy():
    kontekst = _maket_konteksta()
    with patch.object(mvd_tools.client, "statistika_dtp", return_value=[]):
        rezultat = await mvd_tools.statistika_dtp(kontekst)
    assert "2024" in rezultat or "резервные данные" in rezultat or "гибдд" in rezultat.lower()


async def test_statistika_dtp_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "subiekt": "г. Москва",
            "god": 2024,
            "vid_dtp": "Столкновение",
            "vsego_dtp": 8500,
            "pogibshikh": 320,
            "postradavshikh": 9800,
        },
    ]
    with patch.object(mvd_tools.client, "statistika_dtp", return_value=maket_dannykh):
        rezultat = await mvd_tools.statistika_dtp(kontekst)
    assert "Москва" in rezultat


async def test_rozysk_del_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mvd_tools.client, "rozysk_del", return_value=[]):
        rezultat = await mvd_tools.rozysk_del(kontekst)
    assert isinstance(rezultat, str)


async def test_rozysk_del_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "kategoriya": "Розыск лиц",
            "subiekt": "Московская область",
            "kolichestvo": 1250,
            "data": "2024-01",
        },
    ]
    with patch.object(mvd_tools.client, "rozysk_del", return_value=maket_dannykh):
        rezultat = await mvd_tools.rozysk_del(kontekst)
    assert "Розыск" in rezultat


async def test_narkotiki_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mvd_tools.client, "narkotiki", return_value=[]):
        rezultat = await mvd_tools.narkotiki(kontekst)
    assert isinstance(rezultat, str)


async def test_narkotiki_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "subiekt": "Красноярский край",
            "vid_prestupleniya": "Сбыт наркотиков",
            "kolichestvo_prestupleniy": 420,
            "izyato_gramm": 15000.0,
            "vid_narkotika": "Синтетические",
        },
    ]
    with patch.object(mvd_tools.client, "narkotiki", return_value=maket_dannykh):
        rezultat = await mvd_tools.narkotiki(kontekst)
    assert "Красноярск" in rezultat


def test_constants_vidy_prestupleniy():
    assert len(mvd_constants.VIDY_PRESTUPLENIY) == 12


def test_constants_vidy_dtp():
    assert len(mvd_constants.VIDY_DTP) == 7


def test_constants_nabory_dannykh():
    assert len(mvd_constants.NABORY_DANNYKH) >= 10


def test_constants_statistika_prestupnosti():
    s = mvd_constants.STATISTIKA_PRESTUPNOSTI_2024
    assert s["zaregistrirovano_prestupleniy"] > 1000000
    assert len(s["po_fo"]) == 8


def test_constants_statistika_dtp():
    s = mvd_constants.STATISTIKA_DTP_2024
    assert s["vsego_dtp"] > 100000
