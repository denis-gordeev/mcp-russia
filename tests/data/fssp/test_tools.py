"""Тесты инструментов модуля ФССП."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.fssp import tools as fssp_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_vidov_proizvodstv():
    ctx = _maket_konteksta()
    result = await fssp_tools.spisok_vidov_proizvodstv(ctx)
    assert "Штрафы ГИБДД" in result


async def test_spisok_statusov_proizvodstva():
    ctx = _maket_konteksta()
    result = await fssp_tools.spisok_statusov_proizvodstva(ctx)
    assert "производстве" in result


async def test_spisok_ogranicheniy():
    ctx = _maket_konteksta()
    result = await fssp_tools.spisok_ogranicheniy(ctx)
    assert "выезд" in result.lower()


async def test_spisok_kategoriy_dolzhnikov():
    ctx = _maket_konteksta()
    result = await fssp_tools.spisok_kategoriy_dolzhnikov(ctx)
    assert "Индивидуальный предприниматель" in result


async def test_spisok_osnovaniy_vozbuzhdeniya():
    ctx = _maket_konteksta()
    result = await fssp_tools.spisok_osnovaniy_vozbuzhdeniya(ctx)
    assert "Судебный акт" in result


async def test_info_proizvodstva_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(fssp_tools.client, "info_proizvodstva", return_value=None):
        result = await fssp_tools.info_proizvodstva(ctx, nomer="12345/23/77001-ИП")
    assert "не найдено" in result


async def test_poisk_dolzhnika_pustoy():
    ctx = _maket_konteksta()
    with patch.object(fssp_tools.client, "poisk_proizvodstv", return_value=[]):
        result = await fssp_tools.poisk_dolzhnika(ctx, fio="Иванов Иван Иванович")
    assert "не найдены" in result


async def test_ogranicheniya_dolzhnika_pustoy():
    ctx = _maket_konteksta()
    with patch.object(fssp_tools.client, "ogranicheniya_dolzhnika", return_value=[]):
        result = await fssp_tools.ogranicheniya_dolzhnika(ctx, fio="Иванов Иван Иванович")
    assert "не найдены" in result


async def test_rozysk_dolzhnika_pustoy():
    ctx = _maket_konteksta()
    with patch.object(fssp_tools.client, "rozysk_dolzhnika", return_value=[]):
        result = await fssp_tools.rozysk_dolzhnika(ctx, fio="Иванов Иван Иванович")
    assert "не найдены" in result
