"""Тесты инструментов модуля Счётная палата РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosaudit import tools as rosaudit_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    """Проверка spisok_napravleniy."""
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_napravleniy(ctx)
    assert "Направления контрольной деятельности" in result
    assert "бюджет" in result.lower()


async def test_spisok_tipov_meropriyatiy():
    """Проверка spisok_tipov_meropriyatiy."""
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_tipov_meropriyatiy(ctx)
    assert "Типы контрольных мероприятий" in result
    assert "Проверка" in result


async def test_spisok_subiektov_audita():
    """Проверка spisok_subiektov_audita."""
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_subiektov_audita(ctx)
    assert "Субъекты" in result
    assert "Федеральные" in result


async def test_info_kontrolnogo_meropriyatiya_not_found():
    """Проверка info_kontrolnogo_meropriyatiya при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(
        rosaudit_tools.client, "poluchit_kontrolnoe_meropriyatie", return_value=None
    ):
        result = await rosaudit_tools.info_kontrolnogo_meropriyatiya("nonexistent", ctx)
    assert "не найдено" in result


async def test_info_auditorskogo_zaklyucheniya_not_found():
    """Проверка info_auditorskogo_zaklyucheniya при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(
        rosaudit_tools.client, "poluchit_auditorskoe_zaklyuchenie", return_value=None
    ):
        result = await rosaudit_tools.info_auditorskogo_zaklyucheniya("nonexistent", ctx)
    assert "не найдено" in result


async def test_ispolnenie_byudzheta_unavailable():
    """Проверка ispolnenie_byudzheta при отсутствии данных."""
    with patch.object(rosaudit_tools.client, "poluchit_byudzhet_ispolnenie", return_value=None):
        result = await rosaudit_tools.ispolnenie_byudzheta(period="2024")
    assert "недоступны" in result


async def test_poisk_narusheniy_empty():
    """Проверка poisk_narusheniy при отсутствии результатов."""
    with patch.object(rosaudit_tools.client, "poluchit_narusheniya", return_value=[]):
        result = await rosaudit_tools.poisk_narusheniy(organizaciya="Тест")
    assert "не найдены" in result
