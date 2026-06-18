"""Тесты инструментов модуля Минздрав РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minzdrav import tools as minzdrav_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_poisk_med_organizatsiy_empty():
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "poisk_med_organizatsiy", return_value=[]):
        result = await minzdrav_tools.poisk_med_organizatsiy(ctx=ctx)
    assert "не найдены" in result


async def test_poisk_med_organizatsiy_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nazvanie": "Городская больница №1",
            "tip": "Больница",
            "region": "Москва",
            "city": "Москва",
        },
    ]
    with patch.object(minzdrav_tools.client, "poisk_med_organizatsiy", return_value=mock_data):
        result = await minzdrav_tools.poisk_med_organizatsiy(
            region="Москва", tip="больница", ctx=ctx
        )
    assert "Городская больница" in result


async def test_info_med_organizatsii_not_found():
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=None):
        result = await minzdrav_tools.info_med_organizatsii(ctx, "nonexistent")
    assert "не найдена" in result


async def test_info_med_organizatsii_found():
    ctx = _mock_ctx()
    mock_data = {
        "nazvanie": "Городская больница №1",
        "tip": "Больница",
        "adres": "г. Москва, ул. Примерная, д.1",
        "region": "Москва",
        "city": "Москва",
        "telefon": "+7 (495) 123-45-67",
        "litsenzia": "Л041-01137-77/00368123",
        "krovatey": 500,
        "vrachey": 200,
    }
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=mock_data):
        result = await minzdrav_tools.info_med_organizatsii(ctx, "12345")
    assert "Городская больница" in result
    assert "500" in result


async def test_poisk_litsenziy_empty():
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=[]):
        result = await minzdrav_tools.poisk_litsenziy(ctx, inn="1234567890")
    assert "не найдены" in result


async def test_poisk_litsenziy_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "Л041-01137",
            "organizaciya": "Городская больница №1",
            "vid_deyatelnosti": "Медицинская деятельность",
            "status": "Действует",
            "data_okonchaniya": "2030-01-01",
        },
    ]
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=mock_data):
        result = await minzdrav_tools.poisk_litsenziy(ctx, inn="1234567890")
    assert "Л041" in result


async def test_pokazateli_zdorovya_empty():
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "pokazateli_zdorovya", return_value=[]):
        result = await minzdrav_tools.pokazateli_zdorovya(ctx, god=2024)
    assert "Минздрав" in result


async def test_pokazateli_zdorovya_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nazvanie": "Ожидаемая продолжительность жизни",
            "znachenie": 73.5,
            "ed_izm": "лет",
            "god": 2024,
            "region": "РФ",
        },
    ]
    with patch.object(minzdrav_tools.client, "pokazateli_zdorovya", return_value=mock_data):
        result = await minzdrav_tools.pokazateli_zdorovya(ctx, god=2024)
    assert "73.5" in result


async def test_statistika_zabolevaniy_empty():
    ctx = _mock_ctx()
    with patch.object(minzdrav_tools.client, "statistika_zabolevaniy", return_value=[]):
        result = await minzdrav_tools.statistika_zabolevaniy(ctx)
    assert "заболеваемости" in result or "Минздрав" in result


async def test_statistika_zabolevaniy_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "kod_mkb": "I00-I99",
            "nazvanie": "Болезни системы кровообращения",
            "chelovek_zabolelo": 500000,
            "letalnykh_sluchaev": 10000,
            "god": 2024,
        },
    ]
    with patch.object(minzdrav_tools.client, "statistika_zabolevaniy", return_value=mock_data):
        result = await minzdrav_tools.statistika_zabolevaniy(ctx, mkb_code="I00-I99")
    assert "кровообращения" in result


async def test_spravochnik_mo():
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_mo(ctx)
    assert "Типы медицинских организаций" in result
    assert "Больница" in result


async def test_spravochnik_spetsialnostey():
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_spetsialnostey(ctx)
    assert "Врачебные специальности" in result
    assert "Терапевт" in result


async def test_spravochnik_mkb10():
    ctx = _mock_ctx()
    result = await minzdrav_tools.spravochnik_mkb10(ctx)
    assert "МКБ-10" in result
    assert "Инфекционные" in result
