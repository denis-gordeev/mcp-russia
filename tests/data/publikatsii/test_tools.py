"""Тесты инструментов модуля Официальные публикации РФ."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.publikatsii import tools as publikatsii_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_tipov_aktov():
    """Проверка spisok_tipov_aktov."""
    ctx = _mock_ctx()
    result = await publikatsii_tools.spisok_tipov_aktov(ctx)
    assert "нормативных актов" in result
    assert "Федеральный закон" in result


async def test_spisok_otrasley():
    """Проверка spisok_otrasley."""
    ctx = _mock_ctx()
    result = await publikatsii_tools.spisok_otrasley(ctx)
    assert "Отрасли законодательства" in result
    assert "Гражданское" in result


async def test_spisok_istochnikov():
    """Проверка spisok_istochnikov."""
    ctx = _mock_ctx()
    result = await publikatsii_tools.spisok_istochnikov(ctx)
    assert "Источники" in result
    assert "pravo.gov.ru" in result


async def test_spisok_statusov():
    """Проверка spisok_statusov."""
    ctx = _mock_ctx()
    result = await publikatsii_tools.spisok_statusov(ctx)
    assert "Статусы" in result
    assert "Действующий" in result


async def test_info_normativnogo_akta_not_found():
    """Проверка info_normativnogo_akta при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(publikatsii_tools.client, "poluchit_normativnyy_akt", return_value=None):
        result = await publikatsii_tools.info_normativnogo_akta(nomer="nonexistent", ctx=ctx)
    assert "не найден" in result


async def test_info_zakonproekta_not_found():
    """Проверка info_zakonproekta при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(publikatsii_tools.client, "poluchit_zakon_proekt", return_value=None):
        result = await publikatsii_tools.info_zakonproekta(nomer="nonexistent", ctx=ctx)
    assert "не найден" in result


async def test_poisk_aktov_empty():
    """Проверка poisk_aktov при отсутствии результатов."""
    ctx = _mock_ctx()
    with patch.object(publikatsii_tools.client, "poluchit_poisku", return_value=[]):
        result = await publikatsii_tools.poisk_aktov(tekst="неверный запрос", ctx=ctx)
    assert "не найдены" in result


async def test_publikatsii_po_datam_empty():
    """Проверка publikatsii_po_datam при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(publikatsii_tools.client, "poluchit_publikatsii", return_value=[]):
        result = await publikatsii_tools.publikatsii_po_datam(tip="fz", ctx=ctx)
    assert "не найдены" in result


async def test_izmeneniya_akta_empty():
    """Проверка izmeneniya_akta при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(publikatsii_tools.client, "poluchit_izmeneniya_akta", return_value=[]):
        result = await publikatsii_tools.izmeneniya_akta(akt_nomer="nonexistent", ctx=ctx)
    assert "не найдено" in result
