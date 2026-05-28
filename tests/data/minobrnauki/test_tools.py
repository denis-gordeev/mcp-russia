"""Тесты инструментов модуля Минобрнауки."""

from unittest.mock import AsyncMock

from mcp_brasil.data.minobrnauki import tools as minobrnauki_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_tipov_vuzov():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_tipov_vuzov(ctx=ctx)
    assert "Университет" in result


async def test_spisok_form_obucheniya():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_form_obucheniya(ctx=ctx)
    assert "Очная" in result


async def test_spisok_urovney_obrazovaniya():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_urovney_obrazovaniya(ctx=ctx)
    assert "Бакалавриат" in result


async def test_spisok_otrasley_nauki():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_otrasley_nauki(ctx=ctx)
    assert "Естественные" in result or "естественные" in result


async def test_spisok_tipov_grantov():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_tipov_grantov(ctx=ctx)
    assert "РНФ" in result


async def test_spisok_statusov_akkreditatsii():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_statusov_akkreditatsii(ctx=ctx)
    assert "Действует" in result


async def test_spisok_federalnyh_okrugov():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.spisok_federalnyh_okrugov(ctx=ctx)
    assert "Центральный" in result


async def test_info_vuza_placeholder():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.info_vuza(ctx=ctx, nazvanie="МГУ")
    assert "не найдена" in result or "placeholder" in result.lower()


async def test_programmy_vuza_placeholder():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.programmy_vuza(ctx=ctx, vuz="МГУ")
    assert "не найдены" in result or "placeholder" in result.lower()


async def test_granty_i_isledovaniya_placeholder():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.granty_i_isledovaniya(ctx=ctx)
    assert "не найдены" in result or "placeholder" in result.lower()


async def test_reyting_vuzov_placeholder():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.reyting_vuzov(ctx=ctx, god=2024)
    assert "не найден" in result or "placeholder" in result.lower()


async def test_aspirantura_placeholder():
    ctx = _mock_ctx()
    result = await minobrnauki_tools.aspirantura(ctx=ctx)
    assert "не найдены" in result or "placeholder" in result.lower()
