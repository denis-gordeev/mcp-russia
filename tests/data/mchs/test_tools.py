"""Тесты инструментов модуля МЧС России."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.mchs import constants as mchs_constants
from mcp_russia.data.mchs import tools as mchs_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_vidov_chs():
    kontekst = _maket_konteksta()
    rezultat = await mchs_tools.spisok_vidov_chs(kontekst)
    assert "техногенн" in rezultat.lower() or "природн" in rezultat.lower()


async def test_spisok_klassov_chs():
    kontekst = _maket_konteksta()
    rezultat = await mchs_tools.spisok_klassov_chs(kontekst)
    assert "локальн" in rezultat.lower() or "федеральн" in rezultat.lower()


async def test_spisok_vidov_pojarov():
    kontekst = _maket_konteksta()
    rezultat = await mchs_tools.spisok_vidov_pojarov(kontekst)
    assert "пожар" in rezultat.lower()


async def test_spisok_tipov_opasnosti():
    kontekst = _maket_konteksta()
    rezultat = await mchs_tools.spisok_tipov_opasnosti(kontekst)
    assert "радиац" in rezultat.lower() or "опасн" in rezultat.lower()


async def test_statistika_pojarov_zapasnoy():
    kontekst = _maket_konteksta()
    with patch.object(mchs_tools.client, "statistika_pojarov", return_value=[]):
        rezultat = await mchs_tools.statistika_pojarov(kontekst)
    assert "356" in rezultat or "2023" in rezultat or "резервные данные" in rezultat


async def test_statistika_pojarov_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "П-2026-001",
            "data": "2026-01-15",
            "subiekt": "Московская область",
            "vid_pozhara": "Пожар в жилом секторе",
            "pogibshikh": 2,
            "postradavshikh": 5,
        },
    ]
    with patch.object(mchs_tools.client, "statistika_pojarov", return_value=maket_dannykh):
        rezultat = await mchs_tools.statistika_pojarov(kontekst)
    assert "Московск" in rezultat


async def test_poisk_chs_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mchs_tools.client, "poisk_chs", return_value=[]):
        rezultat = await mchs_tools.poisk_chs(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_chs_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "ЧС-2026-001",
            "vid_chs": "Техногенная",
            "klass_chs": "Региональная",
            "data_vozniknoveniya": "2026-03-10",
            "subiekt": "Свердловская область",
            "opisanie": "Взрыв на химическом предприятии",
            "sostoyanie": "Ликвидация последствий",
            "pogibshikh": 0,
            "postradavshikh": 3,
        },
    ]
    with patch.object(mchs_tools.client, "poisk_chs", return_value=maket_dannykh):
        rezultat = await mchs_tools.poisk_chs(kontekst)
    assert "Техногенн" in rezultat


async def test_radiatsionnyy_monitoring_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mchs_tools.client, "radiatsionnyy_monitoring", return_value=[]):
        rezultat = await mchs_tools.radiatsionnyy_monitoring(kontekst)
    assert isinstance(rezultat, str)


async def test_radiatsionnyy_monitoring_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "stantsiya": "Москва-1",
            "subiekt": "Москва",
            "uroven_radiatsii": 0.12,
            "edinitsa_izmereniya": "мкЗв/ч",
            "data_izmereniya": "2026-06-01",
            "norma": 0.30,
        },
    ]
    with patch.object(mchs_tools.client, "radiatsionnyy_monitoring", return_value=maket_dannykh):
        rezultat = await mchs_tools.radiatsionnyy_monitoring(kontekst)
    assert "Москва" in rezultat


async def test_gidrologicheskaya_obstanovka_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mchs_tools.client, "gidrologicheskaya_obstanovka", return_value=[]):
        rezultat = await mchs_tools.gidrologicheskaya_obstanovka(kontekst)
    assert isinstance(rezultat, str)


async def test_gidrologicheskaya_obstanovka_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "reka": "Амур",
            "punkt_nablyudeniya": "г. Хабаровск",
            "uroven_vody": 620,
            "opasnyy_uroven": 600,
            "tendentsiya": "рост",
            "data_izmereniya": "2026-06-10",
        },
    ]
    with patch.object(
        mchs_tools.client, "gidrologicheskaya_obstanovka", return_value=maket_dannykh
    ):
        rezultat = await mchs_tools.gidrologicheskaya_obstanovka(kontekst)
    assert "Амур" in rezultat


async def test_preduprezhdeniya_chs_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(mchs_tools.client, "preduprezhdeniya_chs", return_value=[]):
        rezultat = await mchs_tools.preduprezhdeniya_chs(kontekst)
    assert isinstance(rezultat, str)


async def test_preduprezhdeniya_chs_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "ПРД-2026-001",
            "tip_opasnosti": "Гидрологическая опасность",
            "subiekt": "Хабаровский край",
            "opisanie": "Повышение уровня воды в реке Амур",
            "data_nachala": "2026-06-10",
            "data_okonchaniya": "2026-06-20",
        },
    ]
    with patch.object(mchs_tools.client, "preduprezhdeniya_chs", return_value=maket_dannykh):
        rezultat = await mchs_tools.preduprezhdeniya_chs(kontekst)
    assert "гидролог" in rezultat.lower() or "Амур" in rezultat


def test_constants_vidy_chs():
    assert len(mchs_constants.VIDY_CHS) == 4


def test_constants_klassy_chs():
    assert len(mchs_constants.KLASSY_CHS) == 6


def test_constants_vidy_pojarov():
    assert len(mchs_constants.VIDY_POZHAROV) == 7


def test_constants_statistika_pojarov():
    s = mchs_constants.STATISTIKA_POZHAROV_2023
    assert s["vsego_pojarov"] > 300000
    assert len(s["po_fo"]) == 7
