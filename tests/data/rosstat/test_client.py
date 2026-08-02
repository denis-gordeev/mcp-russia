"""Проверки разбора ответов клиента Росстата."""

from unittest.mock import AsyncMock, patch

import pytest

from mcp_russia.data.rosstat import client


@pytest.mark.asyncio
async def test_vrp_normalizuet_pustoy_period_i_chislovye_stroki():
    otvet = {
        "data": [
            {
                "date": None,
                "region": "77",
                "value": "123.5",
                "perCapita": "45.25",
            }
        ]
    }

    with patch.object(client, "http_poluchit", AsyncMock(return_value=otvet)):
        rezultat = await client.poluchit_vrp(subiekt="77")

    assert len(rezultat) == 1
    assert rezultat[0].period == ""
    assert rezultat[0].vrp == 123.5
    assert rezultat[0].vrp_na_dushu == 45.25


@pytest.mark.asyncio
async def test_otraslevaya_struktura_ispolzuet_pole_kod_okved():
    otvet = {
        "data": [
            {
                "code": "C",
                "name": "Обрабатывающие производства",
                "period": 2024,
                "share": "18.5",
                "value": "4700",
            }
        ]
    }

    with patch.object(client, "http_poluchit", AsyncMock(return_value=otvet)):
        rezultat = await client.poluchit_otraslevuyu_strukturu_vrp()

    assert len(rezultat) == 1
    assert rezultat[0].kod_okved == "C"
    assert rezultat[0].period == "2024"
    assert rezultat[0].dolya_vvp == 18.5
    assert rezultat[0].vrp == 4700.0


@pytest.mark.asyncio
async def test_investitsii_ignoriruyut_nekorrektnoe_chislo():
    otvet = {
        "data": [
            {
                "activityCode": "A",
                "activityName": "Сельское хозяйство",
                "value": "нет данных",
                "share": "4.1",
            }
        ]
    }

    with patch.object(client, "http_poluchit", AsyncMock(return_value=otvet)):
        rezultat = await client.poluchit_investitsii_po_vidam()

    assert len(rezultat) == 1
    assert rezultat[0].kod_okved == "A"
    assert rezultat[0].investitsii is None
    assert rezultat[0].dolya == 4.1
