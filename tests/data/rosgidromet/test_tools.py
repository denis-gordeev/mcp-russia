"""Тесты инструментов модуля Росгидромет."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.rosgidromet import tools as rosgidromet_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_stanciy():
    """Проверка spisok_stanciy."""
    ctx = _mock_ctx()
    result = await rosgidromet_tools.spisok_stanciy(ctx)
    assert "Станции мониторинга" in result
    assert "Москва" in result


async def test_spisok_tipov_dannykh():
    """Проверка spisok_tipov_dannykh."""
    ctx = _mock_ctx()
    result = await rosgidromet_tools.spisok_tipov_dannykh(ctx)
    assert "метеорологических данных" in result
    assert "экологических данных" in result


async def test_pogoda_seychas_unavailable():
    """Проверка pogoda_seychas при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "buscar_pogoda", return_value=None):
        result = await rosgidromet_tools.pogoda_seychas(stanciya="99", ctx=ctx)
    assert "недоступны" in result


async def test_prognoz_pogody_unavailable():
    """Проверка prognoz_pogody при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "buscar_prognoz", return_value=[]):
        result = await rosgidromet_tools.prognoz_pogody(stanciya="99", ctx=ctx)
    assert "недоступен" in result


async def test_ekologiya_regiona_empty():
    """Проверка ekologiya_regiona при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "buscar_ekologiya", return_value=[]):
        result = await rosgidromet_tools.ekologiya_regiona(gorod="Тест", ctx=ctx)
    assert "недоступны" in result


async def test_preduprezhdeniya_empty():
    """Проверка preduprezhdeniya при отсутствии предупреждений."""
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "buscar_preduprezhdeniya", return_value=[]):
        result = await rosgidromet_tools.preduprezhdeniya(region="Тест", ctx=ctx)
    assert "отсутствуют" in result


async def test_sputnik_monitoring_empty():
    """Проверка sputnik_monitoring при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(rosgidromet_tools.client, "buscar_sputnik_dannye", return_value=[]):
        result = await rosgidromet_tools.sputnik_monitoring(region="Тест", ctx=ctx)
    assert "недоступны" in result
