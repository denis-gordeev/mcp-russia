"""Тесты инструментов модуля Минздрав РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minzdrav import tools as minzdrav_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_poisk_med_organizatsiy():
    """Проверка poisk_med_organizatsiy."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.poisk_med_organizatsiy(ctx=ctx)
    assert "Медицинские организации" in result
    assert "minzdrav.gov.ru" in result


async def test_poisk_med_organizatsiy_with_filters():
    """Проверка poisk_med_organizatsiy с фильтрами."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.poisk_med_organizatsiy(
        region="Москва", tip="больница", gorod="Москва", ctx=ctx
    )
    assert "Москва" in result
    assert "больница" in result


async def test_info_med_organizatsii_not_found():
    """Проверка info_med_organizatsii при отсутствии организации."""
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=None):
        result = await minzdrav_tools.info_med_organizatsii("nonexistent", ctx)
    assert "не найдена" in result


async def test_pokazateli_zdorovya():
    """Проверка pokazateli_zdorovya."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.pokazateli_zdorovya(god=2024, ctx=ctx)
    assert "2024" in result
    assert "продолжительность жизни" in result


async def test_pokazateli_zdorovya_with_region():
    """Проверка pokazateli_zdorovya с регионом."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.pokazateli_zdorovya(region="Москва", god=2025, ctx=ctx)
    assert "Москва" in result
    assert "2025" in result


async def test_statistika_zabolevaniy():
    """Проверка statistika_zabolevaniy."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.statistika_zabolevaniy(ctx=ctx)
    assert "Статистика заболеваний" in result
    assert "МКБ-10" in result


async def test_statistika_zabolevaniy_with_mkb():
    """Проверка statistika_zabolevaniy с кодом МКБ."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.statistika_zabolevaniy(
        mkb_code="I00-I99", region="Москва", ctx=ctx
    )
    assert "I00-I99" in result
    assert "кровообращения" in result


async def test_spravochnik_mo():
    """Проверка spravochnik_mo."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_mo(ctx)
    assert "Типы медицинских организаций" in result
    assert "Больница" in result


async def test_spravochnik_spetsialnostey():
    """Проверка spravochnik_spetsialnostey."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_spetsialnostey(ctx)
    assert "Врачебные специальности" in result
    assert "Терапевт" in result


async def test_spravochnik_mkb10():
    """Проверка spravochnik_mkb10."""
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_mkb10(ctx)
    assert "МКБ-10" in result
    assert "Инфекционные" in result
