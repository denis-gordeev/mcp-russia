"""Тесты инструментов модуля Госдума."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.gosduma import tools as gosduma_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_deputatov():
    result = await gosduma_tools.spisok_deputatov(sozyv="8")
    assert "Депутат" in result
    assert "Государственн" in result


async def test_spisok_deputatov_default():
    result = await gosduma_tools.spisok_deputatov()
    assert "Депутат" in result


async def test_info_deputata_not_found():
    ctx = _mock_ctx()
    with patch.object(gosduma_tools.client, "poluchit_deputata", return_value=None):
        result = await gosduma_tools.info_deputata(99999, ctx)
    assert "не найден" in result


async def test_spisok_frakcii():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_frakcii(ctx)
    assert "Единая Россия" in result
    assert "КПРФ" in result
    assert "ЛДПР" in result


async def test_spisok_komitetov():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_komitetov(ctx)
    assert "Комитет" in result
    assert "бюджет" in result.lower() or "обороне" in result.lower()


async def test_spisok_sozyvov():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_sozyvov(ctx)
    assert "Созыв" in result
    assert "VIII" in result or "1993" in result


async def test_zakonoproekty():
    result = await gosduma_tools.zakonoproekty(status="принят")
    assert "Законопроект" in result
    assert "СОЗД" in result or "duma" in result.lower()


async def test_zakonoproekty_default():
    result = await gosduma_tools.zakonoproekty()
    assert "Законопроект" in result
