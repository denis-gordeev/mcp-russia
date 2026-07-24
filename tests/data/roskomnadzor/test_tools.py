"""Тесты инструментов модуля Роскомнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.roskomnadzor import tools as rkn_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_napravleniy():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_napravleniy(kontekst)
    assert "Надзор в сфере СМИ" in rezultat


async def test_spisok_tipov_litsenziy():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_tipov_litsenziy(kontekst)
    assert "Интернет-доступ" in rezultat


async def test_spisok_kategoriy_narusheniy():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_kategoriy_narusheniy(kontekst)
    assert "Утечка персональных данных" in rezultat


async def test_spisok_reestrov():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_reestrov(kontekst)
    assert "запрещённых сайтов" in rezultat


async def test_spisok_tipov_smi():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_tipov_smi(kontekst)
    assert "Сетевое издание" in rezultat


async def test_spisok_kategoriy_pd_operatorov():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.spisok_kategoriy_pd_operatorov(kontekst)
    assert isinstance(rezultat, str)
    assert len(rezultat) > 0


async def test_info_litsenzii_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rkn_tools.client, "poisk_litsenziy", return_value=[]):
        rezultat = await rkn_tools.info_litsenzii(kontekst, nomer_litsenzii="LIC-001")
    assert "не найдена" in rezultat


async def test_info_litsenzii_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "LIC-001",
            "organizatsiya": "ООО Тест",
            "tip_litsenzii": "Интернет-доступ",
            "data_vydachi": "2023-01-01",
            "data_okonchaniya": "2028-01-01",
            "sostoyanie": "Действует",
            "territoriya": "Российская Федерация",
            "istochnik": "Реестр лицензий (rkn.gov.ru)",
        }
    ]
    with patch.object(rkn_tools.client, "poisk_litsenziy", return_value=maket_dannykh):
        rezultat = await rkn_tools.info_litsenzii(kontekst, nomer_litsenzii="LIC-001")
    assert "LIC-001" in rezultat
    assert "ООО Тест" in rezultat


async def test_poisk_smi_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rkn_tools.client, "poisk_smi", return_value=[]):
        rezultat = await rkn_tools.poisk_smi(kontekst)
    assert "не найдены" in rezultat


async def test_info_operatora_pd_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rkn_tools.client, "poisk_operatora_pd", return_value=[]):
        rezultat = await rkn_tools.info_operatora_pd(kontekst)
    assert "не найдены" in rezultat


async def test_info_operatora_pd_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "naimenovanie": "ООО Тест",
            "inn": "7710563663",
            "kategoriya": "Коммерческие организации",
            "tsel_obrabotki": "Кадровый учёт",
            "sostoyanie": "Зарегистрирован",
        }
    ]
    with patch.object(rkn_tools.client, "poisk_operatora_pd", return_value=maket_dannykh):
        rezultat = await rkn_tools.info_operatora_pd(kontekst, inn="7710563663")
    assert "ООО Тест" in rezultat


async def test_proverka_blokirovki_ne_zablokirovan():
    kontekst = _maket_konteksta()
    with patch.object(
        rkn_tools.client,
        "proverka_blokirovki",
        return_value={"domen": "primer.ru", "blokirovka": False, "istochnik": "ЕАИС"},
    ):
        rezultat = await rkn_tools.proverka_blokirovki(kontekst, domen="primer.ru")
    assert "НЕ найден" in rezultat


async def test_proverka_blokirovki_zablokirovan():
    kontekst = _maket_konteksta()
    with patch.object(
        rkn_tools.client,
        "proverka_blokirovki",
        return_value={
            "domen": "zapreshcheno.ru",
            "blokirovka": True,
            "osnovanie": "Экстремистские материалы",
            "data_vklyucheniya": "2024-01-01",
            "organy": "Роскомнадзор",
        },
    ):
        rezultat = await rkn_tools.proverka_blokirovki(kontekst, domen="zapreshcheno.ru")
    assert "ЗАБЛОКИРОВАН" in rezultat


async def test_poisk_ori_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rkn_tools.client, "poisk_ori", return_value=[]):
        rezultat = await rkn_tools.poisk_ori(kontekst)
    assert "не найдены" in rezultat


async def test_zapisi_reestra_nayden():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.zapisi_reestra(kontekst, kod_reestra="zapreshchennye_sayty")
    assert "запрещённых сайтов" in rezultat


async def test_zapisi_reestra_ne_nayden():
    kontekst = _maket_konteksta()
    rezultat = await rkn_tools.zapisi_reestra(kontekst, kod_reestra="nesushchestvuyushchiy")
    assert "не найден" in rezultat
