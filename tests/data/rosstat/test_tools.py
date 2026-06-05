"""Тесты инструментов модуля Росстат."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosstat import tools as rosstat_tools
from mcp_russia.data.rosstat.schemas import RegionData


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_regionov():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_regionov(ctx)
    assert "Субъект" in result
    assert "Москва" in result


async def test_spisok_regionov_has_many():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_regionov(ctx)
    assert "Татарстан" in result
    assert "Краснодар" in result


async def test_spisok_okrugov():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_okrugov(ctx)
    assert "Федеральн" in result
    assert "Центральн" in result


async def test_region_info():
    ctx = _mock_ctx()
    region = RegionData(code="77", name="г. Москва", federalny_okrug="ЦФО", population=13000000)
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=region):
        result = await rosstat_tools.region_info("77", ctx)
    assert "Москва" in result
    assert "13" in result


async def test_region_info_not_found():
    ctx = _mock_ctx()
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=None):
        result = await rosstat_tools.region_info("999", ctx)
    assert "не найден" in result


async def test_okrug_info():
    ctx = _mock_ctx()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={
            "code": "CFO",
            "name": "Центральный федеральный округ",
            "kolichestvo_subiektov": 18,
            "subiekty": ["г. Москва", "Московская область"],
        },
    ):
        result = await rosstat_tools.okrug_info("CFO", ctx)
    assert "Центральн" in result
    assert "18" in result


async def test_okrug_info_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={"error": "не найден"},
    ):
        result = await rosstat_tools.okrug_info("ZZZ", ctx)
    assert "не найден" in result


async def test_pokazateli_rosstata():
    ctx = _mock_ctx()
    result = await rosstat_tools.pokazateli_rosstata(ctx)
    assert "показател" in result.lower()
    assert "населени" in result or "population" in result


async def test_inflyaciya_fallback():
    result = await rosstat_tools.inflyaciya(god="2025")
    assert "Инфляц" in result or "ИПЦ" in result
    assert "2025" in result


async def test_inflyaciya_with_data():
    mock_data = [
        {"period": "2025-01", "ipcz_mesyac": 0.5, "ipcz_nakoplenny": 0.5, "ipcz_god": 9.9},
    ]
    with patch.object(rosstat_tools.client, "poluchit_inflyaciyu", return_value=mock_data):
        result = await rosstat_tools.inflyaciya(god="2025")
    assert "2025-01" in result


async def test_demografiya_fallback():
    result = await rosstat_tools.demografiya(region="")
    assert "Демограф" in result
    assert "Росси" in result


async def test_demografiya_with_data():
    mock_data = [
        {"period": "2025-01", "naselenie": 146000000, "rozhdaemost": 9.0, "smertnost": 12.5},
    ]
    with patch.object(rosstat_tools.client, "poluchit_demografiyu", return_value=mock_data):
        result = await rosstat_tools.demografiya(region="")
    assert "146" in result or "2025-01" in result


async def test_demografiya_with_region():
    result = await rosstat_tools.demografiya(region="77")
    assert "77" in result


async def test_constants_subiekty_count():
    from mcp_russia.data.rosstat.constants import SUBIEKTY_RF

    assert len(SUBIEKTY_RF) >= 85


async def test_constants_emiss_kody():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY

    assert "cpi" in EMISS_KODY_POKAZATELEY
    assert "population" in EMISS_KODY_POKAZATELEY
