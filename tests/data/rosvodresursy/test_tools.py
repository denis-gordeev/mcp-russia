"""Тесты инструментов модуля Росводресурсы."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosvodresursy import tools as rosvodresursy_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_basseynovykh_okrugov():
    ctx = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_basseynovykh_okrugov(ctx)
    assert "Бассейновые округа" in rezultat
    assert "Волжский" in rezultat


async def test_spisok_tipov_vodnykh_obektov():
    ctx = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_tipov_vodnykh_obektov(ctx)
    assert "водных объектов" in rezultat
    assert "Река" in rezultat


async def test_spisok_vodokhranilishch():
    ctx = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_vodokhranilishch(ctx)
    assert "водохранилищ" in rezultat.lower()
    assert "Братское" in rezultat


async def test_poisk_vodnykh_obektov_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=[]):
        rezultat = await rosvodresursy_tools.poisk_vodnykh_obektov(ctx, zapros="тест")
    assert "не найдены" in rezultat


async def test_poisk_vodnykh_obektov_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {"nazvanie": "Река Волга", "tip": "Река", "basseyn": "Волжский", "subiekt": ""},
    ]
    with patch.object(rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=mock_data):
        rezultat = await rosvodresursy_tools.poisk_vodnykh_obektov(ctx, zapros="Волга")
    assert "Волга" in rezultat


async def test_info_vodnogo_obekta_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=None):
        rezultat = await rosvodresursy_tools.info_vodnogo_obekta("nesushchestvuyushchiy", ctx)
    assert "не найден" in rezultat


async def test_info_vodnogo_obekta_nayden():
    ctx = _maket_konteksta()
    mock_data = {
        "nazvanie": "Река Волга",
        "tip": "Река",
        "basseyn": "Волжский бассейновый округ",
        "dlinna_km": 3530,
        "subiekt": "Тверская область",
    }
    with patch.object(rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=mock_data):
        rezultat = await rosvodresursy_tools.info_vodnogo_obekta("volga", ctx)
    assert "Волга" in rezultat
    assert "530" in rezultat


async def test_gidro_monitoring_net_dannykh():
    ctx = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poluchit_gidro_dannye", return_value=[]):
        rezultat = await rosvodresursy_tools.gidro_monitoring(ctx, identifikator_posta="test")
    assert "не получены" in rezultat or "Мониторинг" in rezultat


async def test_gidro_monitoring_s_dannymi():
    ctx = _maket_konteksta()
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
        rezultat = await rosvodresursy_tools.gidro_monitoring(ctx, identifikator_posta="nn")
    assert "Нижний Новгород" in rezultat


async def test_info_vodokhranilishcha_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        rezultat = await rosvodresursy_tools.info_vodokhranilishcha("nesushchestvuyushchiy", ctx)
    assert "не найдено" in rezultat


async def test_info_vodokhranilishcha_static_zapasnoy():
    ctx = _maket_konteksta()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        rezultat = await rosvodresursy_tools.info_vodokhranilishcha("bratsk", ctx)
    assert "Братское" in rezultat
    assert "169" in rezultat


async def test_vodopolzovanie_regionov_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=[]):
        rezultat = await rosvodresursy_tools.vodopolzovanie_regionov(ctx, subiekt="Тест")
    assert "недоступны" in rezultat


async def test_vodopolzovanie_regionov_s_dannymi():
    ctx = _maket_konteksta()
    mock_data = [
        {"subiekt": "Москва", "god": "2024", "zabrano_vody_km3": 1.2, "ispolzovano_vody_km3": 0.9},
    ]
    with patch.object(
        rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=mock_data
    ):
        rezultat = await rosvodresursy_tools.vodopolzovanie_regionov(ctx)
    assert "Москва" in rezultat
