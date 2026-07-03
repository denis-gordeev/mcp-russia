"""Тесты инструментов модуля МЧС России."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.mchs import constants as mchs_constants
from mcp_russia.data.mchs import tools as mchs_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_vidov_chs():
    ctx = _maket_konteksta()
    result = await mchs_tools.spisok_vidov_chs(ctx)
    assert "техногенн" in result.lower() or "природн" in result.lower()


async def test_spisok_klassov_chs():
    ctx = _maket_konteksta()
    result = await mchs_tools.spisok_klassov_chs(ctx)
    assert "локальн" in result.lower() or "федеральн" in result.lower()


async def test_spisok_vidov_pojarov():
    ctx = _maket_konteksta()
    result = await mchs_tools.spisok_vidov_pojarov(ctx)
    assert "пожар" in result.lower()


async def test_spisok_tipov_opasnosti():
    ctx = _maket_konteksta()
    result = await mchs_tools.spisok_tipov_opasnosti(ctx)
    assert "радиац" in result.lower() or "опасн" in result.lower()


async def test_statistika_pojarov_zapasnoy():
    ctx = _maket_konteksta()
    with patch.object(mchs_tools.client, "statistika_pojarov", return_value=[]):
        result = await mchs_tools.statistika_pojarov(ctx)
    assert "356" in result or "2023" in result or "резервные данные" in result


async def test_statistika_pojarov_s_dannymi():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "П-2026-001",
            "data": "2026-01-15",
            "subiekt": "Московская область",
            "vid_pozhara": "Пожар в жилом секторе",
            "pogibshikh": 2,
            "postradavshikh": 5,
        },
    ]
    with patch.object(mchs_tools.client, "statistika_pojarov", return_value=mock_data):
        result = await mchs_tools.statistika_pojarov(ctx)
    assert "Московск" in result


async def test_poisk_chs_pustoy():
    ctx = _maket_konteksta()
    with patch.object(mchs_tools.client, "poisk_chs", return_value=[]):
        result = await mchs_tools.poisk_chs(ctx)
    assert isinstance(result, str)


async def test_poisk_chs_nayden():
    ctx = _maket_konteksta()
    mock_data = [
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
    with patch.object(mchs_tools.client, "poisk_chs", return_value=mock_data):
        result = await mchs_tools.poisk_chs(ctx)
    assert "Техногенн" in result


async def test_radiatsionnyy_monitoring_pustoy():
    ctx = _maket_konteksta()
    with patch.object(mchs_tools.client, "radiatsionnyy_monitoring", return_value=[]):
        result = await mchs_tools.radiatsionnyy_monitoring(ctx)
    assert isinstance(result, str)


async def test_radiatsionnyy_monitoring_s_dannymi():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "stantsiya": "Москва-1",
            "subiekt": "Москва",
            "uroven_radiatsii": 0.12,
            "edinitsa": "мкЗв/ч",
            "data_izmereniya": "2026-06-01",
            "norma": 0.30,
        },
    ]
    with patch.object(mchs_tools.client, "radiatsionnyy_monitoring", return_value=mock_data):
        result = await mchs_tools.radiatsionnyy_monitoring(ctx)
    assert "Москва" in result


async def test_gidrologicheskaya_obstanovka_pustoy():
    ctx = _maket_konteksta()
    with patch.object(mchs_tools.client, "gidrologicheskaya_obstanovka", return_value=[]):
        result = await mchs_tools.gidrologicheskaya_obstanovka(ctx)
    assert isinstance(result, str)


async def test_gidrologicheskaya_obstanovka_s_dannymi():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "reka": "Амур",
            "punkt_nablyudeniya": "г. Хабаровск",
            "uroven_vody": 620,
            "opasnyy_uroven": 600,
            "tendentsiya": "рост",
            "data_izmereniya": "2026-06-10",
        },
    ]
    with patch.object(mchs_tools.client, "gidrologicheskaya_obstanovka", return_value=mock_data):
        result = await mchs_tools.gidrologicheskaya_obstanovka(ctx)
    assert "Амур" in result


async def test_preduprezhdeniya_chs_pustoy():
    ctx = _maket_konteksta()
    with patch.object(mchs_tools.client, "preduprezhdeniya_chs", return_value=[]):
        result = await mchs_tools.preduprezhdeniya_chs(ctx)
    assert isinstance(result, str)


async def test_preduprezhdeniya_chs_s_dannymi():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "ПРД-2026-001",
            "tip_opasnosti": "Гидрологическая опасность",
            "subiekt": "Хабаровский край",
            "opisanie": "Повышение уровня воды в реке Амур",
            "data_nachala": "2026-06-10",
            "data_okonchaniya": "2026-06-20",
        },
    ]
    with patch.object(mchs_tools.client, "preduprezhdeniya_chs", return_value=mock_data):
        result = await mchs_tools.preduprezhdeniya_chs(ctx)
    assert "гидролог" in result.lower() or "Амур" in result


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
