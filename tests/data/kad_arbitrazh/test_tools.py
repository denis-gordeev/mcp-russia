"""Тесты инструментов модуля Картотека арбитражных дел."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.kad_arbitrazh import tools as kad_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_poisk_del():
    """Проверка poisk_del."""
    ctx = _mock_ctx()
    result = await kad_tools.poisk_del(ctx=ctx)
    assert "Картотека арбитражных дел" in result
    assert "kad.arbitr.ru" in result


async def test_poisk_del_with_filters():
    """Проверка poisk_del с фильтрами."""
    ctx = _mock_ctx()
    result = await kad_tools.poisk_del(
        nomer="А40-12345/2024", istorcz="ООО Ромашка", ctx=ctx
    )
    assert "А40-12345/2024" in result
    assert "Ромашка" in result


async def test_info_dela_not_found():
    """Проверка info_dela при отсутствии дела."""
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "info_dela", return_value=None):
        result = await kad_tools.info_dela("А40-00000/2024", ctx)
    assert "не найдено" in result


async def test_akty_po_delu_not_found():
    """Проверка akty_po_delu при отсутствии актов."""
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "akty_po_delu", return_value=[]):
        result = await kad_tools.akty_po_delu("А40-00000/2024", ctx)
    assert "не найдены" in result


async def test_storony_dela_not_found():
    """Проверка storony_dela при отсутствии сторон."""
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "storony_dela", return_value=[]):
        result = await kad_tools.storony_dela("А40-00000/2024", ctx)
    assert "не найдены" in result


async def test_spravochnik_kategoriy():
    """Проверка spravochnik_kategoriy."""
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_kategoriy(ctx)
    assert "Категории" in result
    assert "Банкротство" in result


async def test_spravochnik_instantsiy():
    """Проверка spravochnik_instantsiy."""
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_instantsiy(ctx)
    assert "Инстанции" in result
    assert "первая инстанция" in result


async def test_spravochnik_statusov():
    """Проверка spravochnik_statusov."""
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_statusov(ctx)
    assert "Статусы" in result
    assert "Новое" in result


async def test_spravochnik_aktov():
    """Проверка spravochnik_aktov."""
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_aktov(ctx)
    assert "Типы судебных актов" in result
    assert "Решение" in result
