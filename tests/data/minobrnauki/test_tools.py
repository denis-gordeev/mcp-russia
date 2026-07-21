"""Тесты инструментов модуля Минобрнауки."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minobrnauki import tools as minobrnauki_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_tipov_vuzov():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_tipov_vuzov(kontekst=kontekst)
    assert "Университет" in rezultat


async def test_spisok_form_obucheniya():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_form_obucheniya(kontekst=kontekst)
    assert "Очная" in rezultat


async def test_spisok_urovney_obrazovaniya():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_urovney_obrazovaniya(kontekst=kontekst)
    assert "Бакалавриат" in rezultat


async def test_spisok_otrasley_nauki():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_otrasley_nauki(kontekst=kontekst)
    assert "Естественные" in rezultat or "естественные" in rezultat


async def test_spisok_tipov_grantov():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_tipov_grantov(kontekst=kontekst)
    assert "РНФ" in rezultat


async def test_spisok_statusov_akkreditatsii():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_statusov_akkreditatsii(kontekst=kontekst)
    assert "Действует" in rezultat


async def test_spisok_federalnyh_okrugov():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.spisok_federalnyh_okrugov(kontekst=kontekst)
    assert "Центральный" in rezultat


async def test_info_vuza_po_nazvaniyu():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nazvanie": "МГУ имени М.В. Ломоносова",
        "inn": "7710563663",
        "tip": "университет",
        "gorod": "Москва",
        "subiekt": "г. Москва",
        "sostoyanie_akkreditatsii": "Действует",
        "data_akkreditatsii": "2020-01-01",
        "srok_deystviya": "2026-01-01",
        "nomer_svidetelstva": "1234",
        "adres": "Москва, Ленинские горы",
        "sayt": "https://msu.ru",
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }
    with patch.object(
        minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[maket_dannykh]
    ):
        rezultat = await minobrnauki_tools.info_vuza(kontekst=kontekst, nazvanie="МГУ")
    assert "МГУ" in rezultat
    assert "Действует" in rezultat


async def test_info_vuza_po_inn():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nazvanie": "МФТИ",
        "inn": "5032003607",
        "tip": "университет",
        "sostoyanie_akkreditatsii": "Действует",
    }
    with patch.object(minobrnauki_tools.client, "info_akkreditacii", return_value=maket_dannykh):
        rezultat = await minobrnauki_tools.info_vuza(kontekst=kontekst, inn="5032003607")
    assert "МФТИ" in rezultat


async def test_info_vuza_ne_nayden():
    kontekst = _maket_konteksta()
    with (
        patch.object(minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[]),
        patch.object(minobrnauki_tools.client, "info_akkreditacii", return_value=None),
    ):
        rezultat = await minobrnauki_tools.info_vuza(
            kontekst=kontekst, nazvanie="НесуществующийВУЗ"
        )
    assert "не найден" in rezultat


async def test_programmy_vuza_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[]):
        rezultat = await minobrnauki_tools.programmy_vuza(
            kontekst=kontekst, vuz="НесуществующийВУЗ"
        )
    assert "не найден" in rezultat


async def test_granty_i_isledovaniya():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.granty_i_isledovaniya(kontekst=kontekst)
    assert "РНФ" in rezultat


async def test_reyting_vuzov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poluchit_reyting", return_value=[]):
        rezultat = await minobrnauki_tools.reyting_vuzov(kontekst=kontekst, god=2024)
    assert "не получен" in rezultat or "vuz.minobrnauki" in rezultat


async def test_aspirantura():
    kontekst = _maket_konteksta()
    rezultat = await minobrnauki_tools.aspirantura(kontekst=kontekst)
    assert "аспирант" in rezultat.lower()


async def test_poisk_litsenziy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poisk_litsenziy", return_value=[]):
        rezultat = await minobrnauki_tools.poisk_litsenziy(kontekst=kontekst, inn="1234567890")
    assert "не найдены" in rezultat


async def test_poisk_litsenziy_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer_litsenzii": "1234",
            "nazvanie": "МГУ",
            "sostoyanie_litsenzii": "Действует",
            "srok_deystviya": "2026-01-01",
        }
    ]
    with patch.object(minobrnauki_tools.client, "poisk_litsenziy", return_value=maket_dannykh):
        rezultat = await minobrnauki_tools.poisk_litsenziy(kontekst=kontekst, inn="7710563663")
    assert "МГУ" in rezultat
    assert "1234" in rezultat
