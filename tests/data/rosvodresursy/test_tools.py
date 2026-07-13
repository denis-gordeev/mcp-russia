"""Тесты инструментов модуля Росводресурсы."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosvodresursy import tools as rosvodresursy_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_basseynovykh_okrugov():
    kontekst = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_basseynovykh_okrugov(kontekst)
    assert "Бассейновые округа" in rezultat
    assert "Волжский" in rezultat


async def test_spisok_tipov_vodnykh_obektov():
    kontekst = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_tipov_vodnykh_obektov(kontekst)
    assert "водных объектов" in rezultat
    assert "Река" in rezultat


async def test_spisok_vodokhranilishch():
    kontekst = _maket_konteksta()
    rezultat = await rosvodresursy_tools.spisok_vodokhranilishch(kontekst)
    assert "водохранилищ" in rezultat.lower()
    assert "Братское" in rezultat


async def test_poisk_vodnykh_obektov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=[]):
        rezultat = await rosvodresursy_tools.poisk_vodnykh_obektov(kontekst, zapros="тест")
    assert "не найдены" in rezultat


async def test_poisk_vodnykh_obektov_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {"nazvanie": "Река Волга", "tip": "Река", "basseyn": "Волжский", "subiekt": ""},
    ]
    with patch.object(
        rosvodresursy_tools.client, "poisk_vodnykh_obektov", return_value=maket_dannykh
    ):
        rezultat = await rosvodresursy_tools.poisk_vodnykh_obektov(kontekst, zapros="Волга")
    assert "Волга" in rezultat


async def test_info_vodnogo_obekta_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=None):
        rezultat = await rosvodresursy_tools.info_vodnogo_obekta("nesushchestvuyushchiy", kontekst)
    assert "не найден" in rezultat


async def test_info_vodnogo_obekta_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nazvanie": "Река Волга",
        "tip": "Река",
        "basseyn": "Волжский бассейновый округ",
        "dlinna_km": 3530,
        "subiekt": "Тверская область",
    }
    with patch.object(
        rosvodresursy_tools.client, "info_vodnogo_obekta", return_value=maket_dannykh
    ):
        rezultat = await rosvodresursy_tools.info_vodnogo_obekta("volga", kontekst)
    assert "Волга" in rezultat
    assert "530" in rezultat


async def test_gidro_monitoring_net_dannykh():
    kontekst = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poluchit_gidro_dannye", return_value=[]):
        rezultat = await rosvodresursy_tools.gidro_monitoring(
            kontekst, identifikator_posta="proverka"
        )
    assert "не получены" in rezultat or "Мониторинг" in rezultat


async def test_gidro_monitoring_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "post": "Нижний Новгород",
            "vodnyy_obekt": "Река Волга",
            "data_izmereniya": "2026-06-01",
            "uroven": 5.2,
            "raskhod": 8500,
        },
    ]
    with patch.object(
        rosvodresursy_tools.client, "poluchit_gidro_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosvodresursy_tools.gidro_monitoring(kontekst, identifikator_posta="nn")
    assert "Нижний Новгород" in rezultat


async def test_info_vodokhranilishcha_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        rezultat = await rosvodresursy_tools.info_vodokhranilishcha(
            "nesushchestvuyushchiy", kontekst
        )
    assert "не найдено" in rezultat


async def test_info_vodokhranilishcha_static_zapasnoy():
    kontekst = _maket_konteksta()
    with patch.object(
        rosvodresursy_tools.client, "poluchit_dannye_vodokhranilishcha", return_value=None
    ):
        rezultat = await rosvodresursy_tools.info_vodokhranilishcha("bratsk", kontekst)
    assert "Братское" in rezultat
    assert "169" in rezultat


async def test_vodopolzovanie_regionov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=[]):
        rezultat = await rosvodresursy_tools.vodopolzovanie_regionov(kontekst, subiekt="Тест")
    assert "недоступны" in rezultat


async def test_vodopolzovanie_regionov_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {"subiekt": "Москва", "god": "2024", "zabrano_vody_km3": 1.2, "ispolzovano_vody_km3": 0.9},
    ]
    with patch.object(
        rosvodresursy_tools.client, "poluchit_vodopolzovanie", return_value=maket_dannykh
    ):
        rezultat = await rosvodresursy_tools.vodopolzovanie_regionov(kontekst)
    assert "Москва" in rezultat
