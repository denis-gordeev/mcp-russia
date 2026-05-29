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


async def test_spisok_okrugov():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_okrugov(ctx)
    assert "Федеральн" in result
    assert "Центральн" in result


async def test_region_info():
    ctx = _mock_ctx()
    region = RegionData(code="77", name="г. Москва")
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=region):
        result = await rosstat_tools.region_info("77", ctx)
    assert "Москва" in result


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
        return_value={"code": "CFO", "name": "Центральный федеральный округ", "note": "test"},
    ):
        result = await rosstat_tools.okrug_info("CFO", ctx)
    assert "Центральн" in result


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


async def test_inflyaciya():
    result = await rosstat_tools.inflyaciya(god="2025")
    assert "Инфляц" in result or "ИПЦ" in result
    assert "2025" in result


async def test_demografiya():
    result = await rosstat_tools.demografiya(region="")
    assert "Демограф" in result
    assert "Росси" in result


async def test_demografiya_with_region():
    result = await rosstat_tools.demografiya(region="77")
    assert "77" in result
