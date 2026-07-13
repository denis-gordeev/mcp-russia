"""Тесты инструментов модуля ГИБДД/МВД."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.gibdd import tools as gibdd_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_tipov_ts():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_tipov_ts(kontekst=kontekst)
    assert "Легковой" in rezultat


async def test_spisok_kategoriyy_vu():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_kategoriyy_vu(kontekst=kontekst)
    assert "B" in rezultat


async def test_spisok_vidov_narusheniy():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_vidov_narusheniy(kontekst=kontekst)
    assert "скорост" in rezultat.lower()


async def test_spisok_statusov_shtrafov():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_statusov_shtrafov(kontekst=kontekst)
    assert "Оплачен" in rezultat


async def test_spisok_tipov_dtp():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_tipov_dtp(kontekst=kontekst)
    assert "Столкновение" in rezultat


async def test_spisok_regionov_registratsii():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.spisok_regionov_registratsii(kontekst=kontekst)
    assert "Москва" in rezultat


async def test_info_ts_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(gibdd_tools, "_polnaya_proverka_ts", return_value=([], [], [], [])):
        rezultat = await gibdd_tools.info_ts(kontekst=kontekst, vin="XTA21140052XXXXXX")
    assert "не найден" in rezultat


async def test_info_vu_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(gibdd_tools.client, "proverka_vu", return_value=None):
        rezultat = await gibdd_tools.info_vu(kontekst=kontekst, nomer_vu="7700000000")
    assert "не найдена" in rezultat


async def test_shtrafy_po_ts():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.shtrafy_po_ts(kontekst=kontekst, gos_nomer="А123АА77")
    assert "Госуслуги" in rezultat


async def test_shtrafy_po_vu():
    kontekst = _maket_konteksta()
    rezultat = await gibdd_tools.shtrafy_po_vu(kontekst=kontekst, nomer_vu="7700000000")
    assert "Госуслуги" in rezultat


async def test_statistika_dtp_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(gibdd_tools.client, "statistika_dtp_region", return_value=None):
        rezultat = await gibdd_tools.statistika_dtp(kontekst=kontekst, subiekt="Москва", god=2024)
    assert "не найдена" in rezultat


async def test_istoriya_registraciy_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(gibdd_tools.client, "proverka_istorii_ts", return_value=[]):
        rezultat = await gibdd_tools.istoriya_registraciy(
            kontekst=kontekst, vin="XTA21140052XXXXXX"
        )
    assert "не найдена" in rezultat
