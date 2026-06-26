"""Тесты инструментов модуля Росгидромет."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosgidromet import tools as rosgidromet_tools
from mcp_russia.data.rosgidromet.client import (
    _gpa_v_mmrtst,
    _gradusy_v_napravlenie,
    _razobrat_openmeteo_ekologiyu,
    _razobrat_openmeteo_pogodu,
    _razobrat_openmeteo_prognoz,
)
from mcp_russia.data.rosgidromet.constants import STANCII_MONITORINGA


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_stanciy():
    ctx = _mock_ctx()
    result = await rosgidromet_tools.spisok_stanciy(ctx)
    assert "Станции мониторинга" in result
    assert "Москва" in result


async def test_spisok_tipov_dannykh():
    ctx = _mock_ctx()
    result = await rosgidromet_tools.spisok_tipov_dannykh(ctx)
    assert "метеорологических данных" in result
    assert "экологических данных" in result


async def test_pogoda_seychas_unavailable():
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "poluchit_pogodu", return_value=None):
        result = await rosgidromet_tools.pogoda_seychas(stanciya="99", ctx=ctx)
    assert "недоступны" in result


async def test_prognoz_pogody_unavailable():
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "poluchit_prognoz", return_value=[]):
        result = await rosgidromet_tools.prognoz_pogody(stanciya="99", ctx=ctx)
    assert "недоступен" in result


async def test_ekologiya_regiona_empty():
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "poluchit_ekologiyu", return_value=[]):
        result = await rosgidromet_tools.ekologiya_regiona(gorod="Тест", ctx=ctx)
    assert "недоступны" in result


async def test_preduprezhdeniya_empty():
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "poluchit_preduprezhdeniya", return_value=[]):
        result = await rosgidromet_tools.preduprezhdeniya(subiekt="Тест", ctx=ctx)
    assert "отсутствуют" in result


async def test_sputnik_monitoring_empty():
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "poluchit_sputnik_dannye", return_value=[]):
        result = await rosgidromet_tools.sputnik_monitoring(subiekt="Тест", ctx=ctx)
    assert "недоступны" in result


def test_razobrat_openmeteo_pogodu():
    data = {
        "current": {
            "temperature_2m": 5.3,
            "relative_humidity_2m": 72,
            "apparent_temperature": 2.1,
            "precipitation": 0.0,
            "weather_code": 3,
            "wind_speed_10m": 4.5,
            "wind_direction_10m": 180,
            "surface_pressure": 1013.2,
            "time": "2026-06-01T12:00",
        }
    }
    info = STANCII_MONITORINGA[0]
    result = _razobrat_openmeteo_pogodu(data, info)
    assert result.gorod == "Москва"
    assert result.temperatura == 5.3
    assert result.oshchushchaetsya_kak == 2.1
    assert result.vlazhnost == 72
    assert result.opisaniye == "Пасмурно"
    assert result.veter_napravlenie == "Ю"


def test_razobrat_openmeteo_prognoz():
    data = {
        "daily": {
            "time": ["2026-06-01", "2026-06-02"],
            "temperature_2m_max": [22.0, 24.0],
            "temperature_2m_min": [10.0, 12.0],
            "precipitation_probability_max": [30, 10],
            "wind_speed_10m_max": [5.0, 3.0],
            "weather_code": [1, 0],
        }
    }
    info = STANCII_MONITORINGA[0]
    result = _razobrat_openmeteo_prognoz(data, info)
    assert len(result) == 2
    assert result[0].gorod == "Москва"
    assert result[0].temperatura_dnem == 22.0
    assert result[0].temperatura_nochyu == 10.0
    assert result[0].opisaniye == "Преимущественно ясно"
    assert result[1].opisaniye == "Ясно"


def test_razobrat_openmeteo_ekologiyu():
    data = {
        "current": {
            "pm2_5": 12.5,
            "pm10": 35.0,
            "carbon_monoxide": 200.0,
            "nitrogen_dioxide": 15.0,
            "sulphur_dioxide": 5.0,
            "ozone": 80.0,
            "time": "2026-06-01T12:00",
        }
    }
    info = STANCII_MONITORINGA[0]
    result = _razobrat_openmeteo_ekologiyu(data, info)
    assert len(result) == 6
    assert result[0].pokazatel == "PM2.5"
    assert result[0].znachenie == 12.5
    assert result[0].prevyshenie is False
    assert result[1].pokazatel == "PM10"
    assert result[1].znachenie == 35.0
    assert result[1].prevyshenie is False


def test_razobrat_openmeteo_ekologiyu_prevyshenie():
    data = {
        "current": {
            "pm2_5": 55.0,
            "pm10": 80.0,
            "carbon_monoxide": 5.0,
            "nitrogen_dioxide": 50.0,
            "sulphur_dioxide": 25.0,
            "ozone": 150.0,
            "time": "2026-06-01T12:00",
        }
    }
    info = STANCII_MONITORINGA[0]
    result = _razobrat_openmeteo_ekologiyu(data, info)
    assert result[0].prevyshenie is True
    assert result[1].prevyshenie is True
    assert result[3].prevyshenie is True
    assert result[4].prevyshenie is True
    assert result[5].prevyshenie is True


def test_gpa_v_mmrtst():
    assert _gpa_v_mmrtst(None) is None
    assert _gpa_v_mmrtst(1013.25) == 760.0
    assert _gpa_v_mmrtst(1000.0) == 750.1


def test_gradusy_v_napravlenie():
    assert _gradusy_v_napravlenie(0) == "С"
    assert _gradusy_v_napravlenie(90) == "В"
    assert _gradusy_v_napravlenie(180) == "Ю"
    assert _gradusy_v_napravlenie(270) == "З"
