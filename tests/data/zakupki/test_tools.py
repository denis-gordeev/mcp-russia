"""Тесты инструментов модуля Закупки (ЕИС)."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.zakupki import tools as zakupki_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_poisk_zakupok():
    """Проверка poisk_zakupok."""
    ctx = _mock_ctx()
    result = await zakupki_tools.poisk_zakupok(ctx=ctx)
    assert "ЕИС" in result
    assert "zakupki.gov.ru" in result


async def test_poisk_zakupok_with_filters():
    """Проверка poisk_zakupok с фильтрами."""
    ctx = _mock_ctx()
    result = await zakupki_tools.poisk_zakupok(
        zapros="компьютеры", zakon="44-ФЗ", region="Москва", ctx=ctx
    )
    assert "компьютеры" in result
    assert "44-ФЗ" in result
    assert "Москва" in result


async def test_info_zakupki_not_found():
    """Проверка info_zakupki при отсутствии закупки."""
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "poluchit_zakupku", return_value=None):
        result = await zakupki_tools.info_zakupki("0000000001", ctx)
    assert "не найдена" in result


async def test_info_zakazchika_not_found():
    """Проверка info_zakazchika при отсутствии заказчика."""
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "info_zakazchika", return_value=None):
        result = await zakupki_tools.info_zakazchika("0000000000", ctx)
    assert "не найден" in result


async def test_info_postavshchika_not_found():
    """Проверка info_postavshchika при отсутствии поставщика."""
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "info_postavshchika", return_value=None):
        result = await zakupki_tools.info_postavshchika("0000000000", ctx)
    assert "не найден" in result


async def test_statusy_zakupok():
    """Проверка statusy_zakupok."""
    ctx = _mock_ctx()
    result = await zakupki_tools.statusy_zakupok(ctx)
    assert "Статусы" in result
    assert "Планирование" in result


async def test_sposoby_zakupok():
    """Проверка sposoby_zakupok."""
    ctx = _mock_ctx()
    result = await zakupki_tools.sposoby_zakupok(ctx)
    assert "Способы" in result
    assert "Электронный аукцион" in result


async def test_plany_zakupok():
    """Проверка plany_zakupok."""
    ctx = _mock_ctx()
    result = await zakupki_tools.plany_zakupok(god=2025, ctx=ctx)
    assert "2025" in result
    assert "Планы-графики" in result
