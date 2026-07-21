"""Тесты инструментов модуля Роспотребнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rospotrebnadzor import tools as rpn_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_napravleniy():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_napravleniy(kontekst)
    assert "Санитарно-эпидемиологический надзор" in rezultat


async def test_spisok_tipov_proverok():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_tipov_proverok(kontekst)
    assert "Плановая проверка" in rezultat


async def test_spisok_kategoriy_obektov():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_kategoriy_obektov(kontekst)
    assert "Предприятия пищевой промышленности" in rezultat


async def test_spisok_regionalnyh_upravleniy():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_regionalnyh_upravleniy(kontekst)
    assert "Центральному федеральному округу" in rezultat


async def test_info_proverki_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "info_proverki", return_value=None):
        rezultat = await rpn_tools.info_proverki(kontekst, nomer_proverki="12345")
    assert "не найдена" in rezultat


async def test_info_proverki_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nomer": "12345",
        "tip_proverki": "Плановая",
        "obekt": "ООО Тест",
        "inn": "7710563663",
        "data_nachala": "2024-01-01",
        "data_okonchaniya": "2024-01-15",
        "sostoyanie": "Завершена",
        "vyavleno_narusheniy": 2,
        "rezultat": "Нарушения выявлены",
        "istochnik": "Реестр проверок (proverki.rospotrebnadzor.ru)",
    }
    with patch.object(rpn_tools.client, "info_proverki", return_value=maket_dannykh):
        rezultat = await rpn_tools.info_proverki(kontekst, nomer_proverki="12345")
    assert "ООО Тест" in rezultat
    assert "Завершена" in rezultat


async def test_poisk_proverok_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=[]):
        rezultat = await rpn_tools.poisk_proverok(kontekst, inn="7710563663")
    assert "не найдены" in rezultat


async def test_poisk_proverok_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "12345",
            "tip_proverki": "Плановая",
            "obekt": "ООО Тест",
            "data_nachala": "2024-01-01",
            "sostoyanie": "Завершена",
            "vyavleno_narusheniy": 0,
        }
    ]
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=maket_dannykh):
        rezultat = await rpn_tools.poisk_proverok(kontekst, inn="7710563663")
    assert "ООО Тест" in rezultat


async def test_plan_proverok_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "plan_proverok", return_value=[]):
        rezultat = await rpn_tools.plan_proverok(kontekst, god=2024)
    assert "не получен" in rezultat


async def test_spisok_sanpinov():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_sanpinov(kontekst)
    assert "2.1.3684-21" in rezultat


async def test_zhaloby_potrebiteley_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_zhalob", return_value=[]):
        rezultat = await rpn_tools.zhaloby_potrebiteley(kontekst)
    assert "не найдены" in rezultat


async def test_zhaloby_potrebiteley_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "tema": "Некачественный товар",
            "organizaciya": "ООО Тест",
            "data_podachi": "2024-03-01",
            "sostoyanie_rassmotreniya": "Рассматривается",
            "rezultat": "",
        }
    ]
    with patch.object(rpn_tools.client, "poisk_zhalob", return_value=maket_dannykh):
        rezultat = await rpn_tools.zhaloby_potrebiteley(kontekst, organizaciya="ООО Тест")
    assert "Некачественный товар" in rezultat


async def test_pokazateli_bezopasnosti():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.pokazateli_bezopasnosti(kontekst)
    assert "ЕМИСС" in rezultat or "rospotrebnadzor" in rezultat
