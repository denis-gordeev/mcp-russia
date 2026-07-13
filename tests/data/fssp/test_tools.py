"""Тесты инструментов модуля ФССП."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.fssp import tools as fssp_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_vidov_proizvodstv():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_vidov_proizvodstv(kontekst)
    assert "Штрафы ГИБДД" in rezultat


async def test_spisok_statusov_proizvodstva():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_statusov_proizvodstva(kontekst)
    assert "производстве" in rezultat


async def test_spisok_ogranicheniy():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_ogranicheniy(kontekst)
    assert "выезд" in rezultat.lower()


async def test_spisok_kategoriy_dolzhnikov():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_kategoriy_dolzhnikov(kontekst)
    assert "Индивидуальный предприниматель" in rezultat


async def test_spisok_osnovaniy_vozbuzhdeniya():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_osnovaniy_vozbuzhdeniya(kontekst)
    assert "Судебный акт" in rezultat


async def test_spisok_regionov():
    kontekst = _maket_konteksta()
    rezultat = await fssp_tools.spisok_regionov(kontekst)
    assert "Москва" in rezultat


async def test_info_proizvodstva_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(fssp_tools.client, "info_proizvodstva", return_value=None):
        rezultat = await fssp_tools.info_proizvodstva(kontekst, nomer="12345/23/77001-ИП")
    assert "не найдено" in rezultat


async def test_poisk_dolzhnika_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(fssp_tools.client, "poisk_proizvodstv", return_value=[]):
        rezultat = await fssp_tools.poisk_dolzhnika(kontekst, fio="Иванов Иван Иванович")
    assert "не найдены" in rezultat


async def test_ogranicheniya_dolzhnika_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(fssp_tools.client, "ogranicheniya_dolzhnika", return_value=[]):
        rezultat = await fssp_tools.ogranicheniya_dolzhnika(kontekst, fio="Иванов Иван Иванович")
    assert "не найдены" in rezultat


async def test_rozysk_dolzhnika_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(fssp_tools.client, "rozysk_dolzhnika", return_value=[]):
        rezultat = await fssp_tools.rozysk_dolzhnika(kontekst, fio="Иванов Иван Иванович")
    assert "не найдены" in rezultat
