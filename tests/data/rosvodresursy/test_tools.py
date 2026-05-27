"""Тесты инструментов модуля Росводресурсы."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.rosvodresursy import tools as rosvodresursy_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_basseynovykh_okrugov():
    """Проверка spisok_basseynovykh_okrugov."""
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_basseynovykh_okrugov(ctx)
    assert "Бассейновые округа" in result
    assert "Волжский" in result


async def test_spisok_tipov_vodnykh_obektov():
    """Проверка spisok_tipov_vodnykh_obektov."""
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_tipov_vodnykh_obektov(ctx)
    assert "водных объектов" in result
    assert "Река" in result


async def test_spisok_vodokhranilishch():
    """Проверка spisok_vodokhranilishch."""
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_vodokhranilishch(ctx)
    assert "водохранилищ" in result.lower()
    assert "Братское" in result


async def test_info_vodnogo_obekta_not_found():
    """Проверка info_vodnogo_obekta при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "poluchit_vodnyy_obekt", return_value=None):
        result = await rosvodresursy_tools.info_vodnogo_obekta("nonexistent", ctx)
    assert "не найден" in result


async def test_gidro_monitoring_no_post():
    """Проверка gidro_monitoring без указания поста."""
    result = await rosvodresursy_tools.gidro_monitoring(post="")
    assert "укажите код" in result


async def test_info_vodokhranilishcha_not_found():
    """Проверка info_vodokhranilishcha при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "poluchit_vodokhranilishche", return_value=None):
        result = await rosvodresursy_tools.info_vodokhranilishcha("nonexistent", ctx)
    assert "не найдено" in result


async def test_vodopolzovanie_regionov_empty():
    """Проверка vodopolzovanie_regionov при отсутствии данных."""
    with patch.object(rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=[]):
        result = await rosvodresursy_tools.vodopolzovanie_regionov(region="Тест")
    assert "недоступны" in result
