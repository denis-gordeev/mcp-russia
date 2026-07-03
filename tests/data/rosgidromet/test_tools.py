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


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_stanciy():
    ctx = _maket_konteksta()
    rezultat = await rosgidromet_tools.spisok_stanciy(ctx)
    assert "Станции мониторинга" in rezultat
    assert "Москва" in rezultat


async def test_spisok_tipov_dannykh():
    ctx = _maket_konteksta()
    rezultat = await rosgidromet_tools.spisok_tipov_dannykh(ctx)
    assert "метеорологических данных" in rezultat
    assert "экологических данных" in rezultat


async def test_pogoda_seychas_nedostupen():
    ctx = _maket_konteksta()
    with patch.object(rosgidromet_tools.client, "poluchit_pogodu", return_value=None):
        rezultat = await rosgidromet_tools.pogoda_seychas(stanciya="99", ctx=ctx)
    assert "недоступны" in rezultat


async def test_prognoz_pogody_nedostupen():
    ctx = _maket_konteksta()
    with patch.object(rosgidromet_tools.client, "poluchit_prognoz", return_value=[]):
        rezultat = await rosgidromet_tools.prognoz_pogody(stanciya="99", ctx=ctx)
    assert "недоступен" in rezultat


async def test_ekologiya_regiona_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosgidromet_tools.client, "poluchit_ekologiyu", return_value=[]):
        rezultat = await rosgidromet_tools.ekologiya_regiona(gorod="Тест", ctx=ctx)
    assert "недоступны" in rezultat


async def test_preduprezhdeniya_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosgidromet_tools.client, "poluchit_preduprezhdeniya", return_value=[]):
        rezultat = await rosgidromet_tools.preduprezhdeniya(subiekt="Тест", ctx=ctx)
    assert "отсутствуют" in rezultat


async def test_sputnik_monitoring_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosgidromet_tools.client, "poluchit_sputnik_dannye", return_value=[]):
        rezultat = await rosgidromet_tools.sputnik_monitoring(subiekt="Тест", ctx=ctx)
    assert "недоступны" in rezultat


def test_razobrat_openmeteo_pogodu():
    dannye = {
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
    rezultat = _razobrat_openmeteo_pogodu(dannye, info)
    assert rezultat.gorod == "Москва"
    assert rezultat.temperatura == 5.3
    assert rezultat.oshchushchaetsya_kak == 2.1
    assert rezultat.vlazhnost == 72
    assert rezultat.opisaniye == "Пасмурно"
    assert rezultat.veter_napravlenie == "Ю"


def test_razobrat_openmeteo_prognoz():
    dannye = {
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
    rezultat = _razobrat_openmeteo_prognoz(dannye, info)
    assert len(rezultat) == 2
    assert rezultat[0].gorod == "Москва"
    assert rezultat[0].temperatura_dnem == 22.0
    assert rezultat[0].temperatura_nochyu == 10.0
    assert rezultat[0].opisaniye == "Преимущественно ясно"
    assert rezultat[1].opisaniye == "Ясно"


def test_razobrat_openmeteo_ekologiyu():
    dannye = {
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
    rezultat = _razobrat_openmeteo_ekologiyu(dannye, info)
    assert len(rezultat) == 6
    assert rezultat[0].pokazatel == "PM2.5"
    assert rezultat[0].znachenie == 12.5
    assert rezultat[0].prevyshenie is False
    assert rezultat[1].pokazatel == "PM10"
    assert rezultat[1].znachenie == 35.0
    assert rezultat[1].prevyshenie is False


def test_razobrat_openmeteo_ekologiyu_prevyshenie():
    dannye = {
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
    rezultat = _razobrat_openmeteo_ekologiyu(dannye, info)
    assert rezultat[0].prevyshenie is True
    assert rezultat[1].prevyshenie is True
    assert rezultat[3].prevyshenie is True
    assert rezultat[4].prevyshenie is True
    assert rezultat[5].prevyshenie is True


def test_gpa_v_mmrtst():
    assert _gpa_v_mmrtst(None) is None
    assert _gpa_v_mmrtst(1013.25) == 760.0
    assert _gpa_v_mmrtst(1000.0) == 750.1


def test_gradusy_v_napravlenie():
    assert _gradusy_v_napravlenie(0) == "С"
    assert _gradusy_v_napravlenie(90) == "В"
    assert _gradusy_v_napravlenie(180) == "Ю"
    assert _gradusy_v_napravlenie(270) == "З"
