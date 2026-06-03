"""Тесты инструментов модуля Роспотребнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rospotrebnadzor import tools as rpn_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_napravleniy(ctx)
    assert "Санитарно-эпидемиологический надзор" in result


async def test_spisok_tipov_proverok():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_tipov_proverok(ctx)
    assert "Плановая проверка" in result


async def test_spisok_kategoriy_obiektov():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_kategoriy_obiektov(ctx)
    assert "Предприятия пищевой промышленности" in result


async def test_spisok_regionalnyh_upravleniy():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_regionalnyh_upravleniy(ctx)
    assert "Центральному федеральному округу" in result


async def test_info_proverki_not_found():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "get_proverka", return_value=None):
        result = await rpn_tools.info_proverki(ctx, nomer_proverki="12345")
    assert "не найдена" in result


async def test_poisk_narusheniy_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "get_narusheniya", return_value=[]):
        result = await rpn_tools.poisk_narusheniy(ctx)
    assert "не найдены" in result


async def test_spisok_sanpinov():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_sanpinov(ctx)
    assert "2.1.3684-21" in result


async def test_zhaloby_potrebiteley_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "get_zhaloby", return_value=[]):
        result = await rpn_tools.zhaloby_potrebiteley(ctx)
    assert "не найдены" in result


async def test_pokazateli_bezopasnosti_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "get_pokazateli", return_value=[]):
        result = await rpn_tools.pokazateli_bezopasnosti(ctx)
    assert "не найдены" in result
