"""Тесты инструментов модуля Минздрав РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minzdrav import tools as minzdrav_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_poisk_med_organizatsiy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "poisk_med_organizatsiy", return_value=[]):
        rezultat = await minzdrav_tools.poisk_med_organizatsiy(kontekst=kontekst)
    assert "не найдены" in rezultat


async def test_poisk_med_organizatsiy_nayden():
    kontekst = _maket_konteksta()
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
            subiekt="Москва", tip="больница", kontekst=kontekst
        )
    assert "Городская больница" in rezultat


async def test_info_med_organizatsii_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=None):
        rezultat = await minzdrav_tools.info_med_organizatsii(kontekst, "nesushchestvuyushchiy")
    assert "не найдена" in rezultat


async def test_info_med_organizatsii_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nazvanie": "Городская больница №1",
        "tip": "Больница",
        "adres": "г. Москва, ул. Примерная, д.1",
        "subiekt": "Москва",
        "gorod": "Москва",
        "telefon": "+7 (495) 123-45-67",
        "litsenzia": "Л041-01137-77/00368123",
        "krovatey": 500,
        "vrachey": 200,
    }
    with patch.object(minzdrav_tools.client, "info_med_organizatsii", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.info_med_organizatsii(kontekst, "12345")
    assert "Городская больница" in rezultat
    assert "500" in rezultat


async def test_poisk_litsenziy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=[]):
        rezultat = await minzdrav_tools.poisk_litsenziy(kontekst, inn="1234567890")
    assert "не найдены" in rezultat


async def test_poisk_litsenziy_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "Л041-01137",
            "organizatsiya": "Городская больница №1",
            "vid_deyatelnosti": "Медицинская деятельность",
            "sostoyanie": "Действует",
            "data_okonchaniya": "2030-01-01",
        },
    ]
    with patch.object(minzdrav_tools.client, "poisk_litsenziy", return_value=maket_dannykh):
        rezultat = await minzdrav_tools.poisk_litsenziy(kontekst, inn="1234567890")
    assert "Л041" in rezultat


async def test_pokazateli_zdorovya_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "pokazateli_zdorovya", return_value=[]):
        rezultat = await minzdrav_tools.pokazateli_zdorovya(kontekst, god=2024)
    assert "Минздрав" in rezultat


async def test_pokazateli_zdorovya_nayden():
    kontekst = _maket_konteksta()
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
        rezultat = await minzdrav_tools.pokazateli_zdorovya(kontekst, god=2024)
    assert "73.5" in rezultat


async def test_statistika_zabolevaniy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minzdrav_tools.client, "statistika_zabolevaniy", return_value=[]):
        rezultat = await minzdrav_tools.statistika_zabolevaniy(kontekst)
    assert "заболеваемости" in rezultat or "Минздрав" in rezultat


async def test_statistika_zabolevaniy_nayden():
    kontekst = _maket_konteksta()
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
        rezultat = await minzdrav_tools.statistika_zabolevaniy(kontekst, kod_mkb="I00-I99")
    assert "кровообращения" in rezultat


async def test_spravochnik_mo():
    kontekst = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_mo(kontekst)
    assert "Типы медицинских организаций" in rezultat
    assert "Больница" in rezultat


async def test_spravochnik_spetsialnostey():
    kontekst = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_spetsialnostey(kontekst)
    assert "Врачебные специальности" in rezultat
    assert "Терапевт" in rezultat


async def test_spravochnik_mkb10():
    kontekst = _maket_konteksta()
    rezultat = await minzdrav_tools.spravochnik_mkb10(kontekst)
    assert "МКБ-10" in rezultat
    assert "Инфекционные" in rezultat
