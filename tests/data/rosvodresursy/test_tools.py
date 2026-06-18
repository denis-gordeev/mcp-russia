"""Тесты инструментов модуля Росводресурсы."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosvodresursy import tools as rosvodresursy_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_basseynovykh_okrugov():
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_basseynovykh_okrugov(ctx)
    assert "Бассейновые округа" in result
    assert "Волжский" in result


async def test_spisok_tipov_vodnykh_obektov():
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_tipov_vodnykh_obektov(ctx)
    assert "водных объектов" in result
    assert "Река" in result


async def test_spisok_vodokhranilishch():
    ctx = _mock_ctx()
    result = await rosvodresursy_tools.spisok_vodokhranilishch(ctx)
    assert "водохранилищ" in result.lower()
    assert "Братское" in result


async def test_poisk_vodnykh_obektov_empty():
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=[]):
        result = await rosvodresursy_tools.poisk_vodnykh_obektov(ctx, zapros="тест")
    assert "не найдены" in result


async def test_poisk_vodnykh_obektov_found():
    ctx = _mock_ctx()
    mock_data = [
        {"nazvanie": "Река Волга", "tip": "Река", "basseyn": "Волжский", "region": ""},
    ]
    with patch.object(rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=mock_data):
        result = await rosvodresursy_tools.poisk_vodnykh_obektov(ctx, zapros="Волга")
    assert "Волга" in result


async def test_info_vodnogo_obekta_not_found():
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=None):
        result = await rosvodresursy_tools.info_vodnogo_obekta("nonexistent", ctx)
    assert "не найден" in result


async def test_info_vodnogo_obekta_found():
    ctx = _mock_ctx()
    mock_data = {
        "nazvanie": "Река Волга",
        "tip": "Река",
        "basseyn": "Волжский бассейновый округ",
        "dlinna_km": 3530,
        "region": "Тверская область",
    }
    with patch.object(rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=mock_data):
        result = await rosvodresursy_tools.info_vodnogo_obekta("volga", ctx)
    assert "Волга" in result
    assert "530" in result


async def test_gidro_monitoring_no_data():
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "poluchit_gidro_dannye", return_value=[]):
        result = await rosvodresursy_tools.gidro_monitoring(ctx, post_id="test")
    assert "не получены" in result or "Мониторинг" in result


async def test_gidro_monitoring_with_data():
    ctx = _mock_ctx()
    mock_data = [
        {
            "post": "Нижний Новгород",
            "vodnyy_obekt": "Река Волга",
            "data_izmereniya": "2026-06-01",
            "uroven": 5.2,
            "raskhod": 8500,
        },
    ]
    with patch.object(rosvodresursy_tools.client, "poluchit_gidro_dannye", return_value=mock_data):
        result = await rosvodresursy_tools.gidro_monitoring(ctx, post_id="nn")
    assert "Нижний Новгород" in result


async def test_info_vodokhranilishcha_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        result = await rosvodresursy_tools.info_vodokhranilishcha("nonexistent", ctx)
    assert "не найдено" in result


async def test_info_vodokhranilishcha_static_fallback():
    ctx = _mock_ctx()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        result = await rosvodresursy_tools.info_vodokhranilishcha("bratsk", ctx)
    assert "Братское" in result
    assert "169" in result


async def test_vodopolzovanie_regionov_empty():
    ctx = _mock_ctx()
    with patch.object(rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=[]):
        result = await rosvodresursy_tools.vodopolzovanie_regionov(ctx, region="Тест")
    assert "недоступны" in result


async def test_vodopolzovanie_regionov_with_data():
    ctx = _mock_ctx()
    mock_data = [
        {"region": "Москва", "god": "2024", "zabrano_vody_km3": 1.2, "ispolzovano_vody_km3": 0.9},
    ]
    with patch.object(
        rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=mock_data
    ):
        result = await rosvodresursy_tools.vodopolzovanie_regionov(ctx)
    assert "Москва" in result
