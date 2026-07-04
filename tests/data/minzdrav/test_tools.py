"""Тесты инструментов модуля Минздрав РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minzdrav import tools as minzdrav_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_poisk_med_organizatsiy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "poisk_med_organizatsiy", return_value=[]):
        rezultat = await minzdrav_tools.poisk_med_organizatsiy(ctx=ctx)
    assert "не найдены" in rezultat


async def test_poisk_med_organizatsiy_nayden():
    ctx = _maket_konteksta()
    maket_dannykh = [
        {
            "nazvanie": "Городская больница №1",
            "tip": "Больница",
            "subiekt": "Москва",
            "gorod": "Москва",
        },
    ]
    with patch.object(minzdrav_tools.client, "poisk_med_organizatsiy", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.poisk_med_organizatsiy(
            subiekt="Москва", tip="больница", ctx=ctx
        )
    assert "Городская больница" in rezultat


async def test_info_med_organizatsii_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=None):
        rezultat = await minzdrav_tools.info_med_organizatsii(ctx, "nesushchestvuyushchiy")
    assert "не найдена" in rezultat


async def test_info_med_organizatsii_nayden():
    ctx = _maket_konteksta()
    maket_dannykh = {
        "nazvanie": "Городская больница №1",
        "tip": "Больница",
        "adres": "г. Москва, ул. Примерная, д.1",
        "subiekt": "Москва",
        "city": "Москва",
        "telefon": "+7 (495) 123-45-67",
        "litsenzia": "Л041-01137-77/00368123",
        "krovatey": 500,
        "vrachey": 200,
    }
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.info_med_organizatsii(ctx, "12345")
    assert "Городская больница" in rezultat
    assert "500" in rezultat


async def test_poisk_litsenziy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=[]):
        rezultat = await minzdrav_tools.poisk_litsenziy(ctx, inn="1234567890")
    assert "не найдены" in rezultat


async def test_poisk_litsenziy_nayden():
    ctx = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "Л041-01137",
            "organizaciya": "Городская больница №1",
            "vid_deyatelnosti": "Медицинская деятельность",
            "sostoyanie": "Действует",
            "data_okonchaniya": "2030-01-01",
        },
    ]
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.poisk_litsenziy(ctx, inn="1234567890")
    assert "Л041" in rezultat


async def test_pokazateli_zdorovya_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "pokazateli_zdorovya", return_value=[]):
        rezultat = await minzdrav_tools.pokazateli_zdorovya(ctx, god=2024)
    assert "Минздрав" in rezultat


async def test_pokazateli_zdorovya_nayden():
    ctx = _maket_konteksta()
    maket_dannykh = [
        {
            "nazvanie": "Ожидаемая продолжительность жизни",
            "znachenie": 73.5,
            "ed_izm": "лет",
            "god": 2024,
            "subiekt": "РФ",
        },
    ]
    with patch.object(minzdrav_tools.client, "pokazateli_zdorovya", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.pokazateli_zdorovya(ctx, god=2024)
    assert "73.5" in rezultat


async def test_statistika_zabolevaniy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "statistika_zabolevaniy", return_value=[]):
        rezultat = await minzdrav_tools.statistika_zabolevaniy(ctx)
    assert "заболеваемости" in rezultat or "Минздрав" in rezultat


async def test_statistika_zabolevaniy_nayden():
    ctx = _maket_konteksta()
    maket_dannykh = [
        {
            "kod_mkb": "I00-I99",
            "nazvanie": "Болезни системы кровообращения",
            "chelovek_zabolelo": 500000,
            "letalnykh_sluchaev": 10000,
            "god": 2024,
        },
    ]
    with patch.object(minzdrav_tools.client, "statistika_zabolevaniy", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.statistika_zabolevaniy(ctx, kod_mkb="I00-I99")
    assert "кровообращения" in rezultat


async def test_spravochnik_mo():
    ctx = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_mo(ctx)
    assert "Типы медицинских организаций" in rezultat
    assert "Больница" in rezultat


async def test_spravochnik_spetsialnostey():
    ctx = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_spetsialnostey(ctx)
    assert "Врачебные специальности" in rezultat
    assert "Терапевт" in rezultat


async def test_spravochnik_mkb10():
    ctx = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_mkb10(ctx)
    assert "МКБ-10" in rezultat
    assert "Инфекционные" in rezultat
