"""Тесты инструментов модуля Федеральное казначейство."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.kaznacheistvo import tools as kaznacheistvo_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_vidov_byudzhetov():
    ctx = _mock_ctx()
    result = await kaznacheistvo_tools.spisok_vidov_byudzhetov(ctx)
    assert "бюджет" in result.lower()


async def test_spisok_kategoriy_raskhodov():
    ctx = _mock_ctx()
    result = await kaznacheistvo_tools.spisok_kategoriy_raskhodov(ctx)
    assert "Образование" in result or "Расходы" in result


async def test_ispolnenie_byudzheta_unavailable():
    ctx = _mock_ctx()
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_ispolnenie_byudzheta", return_value=None
    ):
        result = await kaznacheistvo_tools.ispolnenie_byudzheta(ctx)
    assert isinstance(result, str)


async def test_ispolnenie_byudzheta_found():
    ctx = _mock_ctx()
    mock_data = {
        "period": "2025",
        "tip": "Федеральный бюджет",
        "dohody": 28000.5,
        "raskhody": 31000.2,
        "deficit": -2999.7,
    }
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_ispolnenie_byudzheta", return_value=mock_data
    ):
        result = await kaznacheistvo_tools.ispolnenie_byudzheta(ctx, god=2025)
    assert "2025" in result


async def test_poisk_uchastnikov_bp_empty():
    ctx = _mock_ctx()
    with patch.object(kaznacheistvo_tools.client, "poisk_uchastnikov_bp", return_value=[]):
        result = await kaznacheistvo_tools.poisk_uchastnikov_bp(ctx)
    assert isinstance(result, str)


async def test_poisk_uchastnikov_bp_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "inn": "7707083893",
            "nazvanie": "Минфин России",
            "tip_uchastnika": "ГРБС",
            "byudzhet": "Федеральный",
        },
    ]
    with patch.object(kaznacheistvo_tools.client, "poisk_uchastnikov_bp", return_value=mock_data):
        result = await kaznacheistvo_tools.poisk_uchastnikov_bp(ctx, inn="7707083893")
    assert "Минфин" in result


async def test_poisk_uchrezhdeniy_empty():
    ctx = _mock_ctx()
    with patch.object(kaznacheistvo_tools.client, "poisk_uchrezhdeniy", return_value=[]):
        result = await kaznacheistvo_tools.poisk_uchrezhdeniy(ctx)
    assert isinstance(result, str)


async def test_mezhbyudzhetnye_transferty_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "vid": "Дотация",
            "otpravitel": "Федеральный центр",
            "poluchatel": "Республика Татарстан",
            "summa": 15000.0,
            "god": "2025",
        },
    ]
    with patch.object(
        kaznacheistvo_tools.client, "poluchit_mezhbyudzhetnye", return_value=mock_data
    ):
        result = await kaznacheistvo_tools.mezhbyudzhetnye_transferty(ctx, god=2025)
    assert "Татарстан" in result
