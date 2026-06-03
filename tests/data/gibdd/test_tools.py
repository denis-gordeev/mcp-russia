"""Тесты инструментов модуля ГИБДД/МВД."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.gibdd import tools as gibdd_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_tipov_ts():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_tipov_ts(ctx=ctx)
    assert "Легковой" in result


async def test_spisok_kategoriyy_vu():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_kategoriyy_vu(ctx=ctx)
    assert "B" in result


async def test_spisok_vidov_narusheniy():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_vidov_narusheniy(ctx=ctx)
    assert "скорост" in result.lower()


async def test_spisok_statusov_shtrafov():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_statusov_shtrafov(ctx=ctx)
    assert "Оплачен" in result


async def test_spisok_tipov_dtp():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_tipov_dtp(ctx=ctx)
    assert "Столкновение" in result


async def test_spisok_regionov_registratsii():
    ctx = _mock_ctx()
    result = await gibdd_tools.spisok_regionov_registratsii(ctx=ctx)
    assert "Москва" in result


async def test_info_ts_not_found():
    ctx = _mock_ctx()
    with patch.object(gibdd_tools, "_proverka_ts_full", return_value=([], [], [], [])):
        result = await gibdd_tools.info_ts(ctx=ctx, vin="XTA21140052XXXXXX")
    assert "не найден" in result


async def test_info_vu_not_found():
    ctx = _mock_ctx()
    with patch.object(gibdd_tools.client, "proverka_vu", return_value=None):
        result = await gibdd_tools.info_vu(ctx=ctx, nomer_vu="7700000000")
    assert "не найдена" in result


async def test_shtrafy_po_ts():
    ctx = _mock_ctx()
    result = await gibdd_tools.shtrafy_po_ts(ctx=ctx, gos_nomer="А123АА77")
    assert "Госуслуги" in result


async def test_shtrafy_po_vu():
    ctx = _mock_ctx()
    result = await gibdd_tools.shtrafy_po_vu(ctx=ctx, nomer_vu="7700000000")
    assert "Госуслуги" in result


async def test_statistika_dtp_not_found():
    ctx = _mock_ctx()
    with patch.object(gibdd_tools.client, "statistika_dtp_region", return_value=None):
        result = await gibdd_tools.statistika_dtp(ctx=ctx, region="Москва", god=2024)
    assert "не найдена" in result


async def test_istoriya_registraciy_not_found():
    ctx = _mock_ctx()
    with patch.object(gibdd_tools.client, "proverka_istorii_ts", return_value=[]):
        result = await gibdd_tools.istoriya_registraciy(ctx=ctx, vin="XTA21140052XXXXXX")
    assert "не найдена" in result
