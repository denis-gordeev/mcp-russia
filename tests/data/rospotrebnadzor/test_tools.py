"""Тесты инструментов модуля Роспотребнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rospotrebnadzor import tools as rpn_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_napravleniy(ctx)
    assert "Санитарно-эпидемиологический надзор" in result


async def test_spisok_tipov_proverok():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_tipov_proverok(ctx)
    assert "Плановая проверка" in result


async def test_spisok_kategoriy_obiektov():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_kategoriy_obiektov(ctx)
    assert "Предприятия пищевой промышленности" in result


async def test_spisok_regionalnyh_upravleniy():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_regionalnyh_upravleniy(ctx)
    assert "Центральному федеральному округу" in result


async def test_info_proverki_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "info_proverki", return_value=None):
        result = await rpn_tools.info_proverki(ctx, nomer_proverki="12345")
    assert "не найдена" in result


async def test_info_proverki_nayden():
    ctx = _maket_konteksta()
    mock_data = {
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
    with patch.object(rpn_tools.client, "info_proverki", return_value=mock_data):
        result = await rpn_tools.info_proverki(ctx, nomer_proverki="12345")
    assert "ООО Тест" in result
    assert "Завершена" in result


async def test_poisk_proverok_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=[]):
        result = await rpn_tools.poisk_proverok(ctx, inn="7710563663")
    assert "не найдены" in result


async def test_poisk_proverok_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "12345",
            "tip_proverki": "Плановая",
            "obekt": "ООО Тест",
            "data_nachala": "2024-01-01",
            "sostoyanie": "Завершена",
            "vyavleno_narusheniy": 0,
        }
    ]
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=mock_data):
        result = await rpn_tools.poisk_proverok(ctx, inn="7710563663")
    assert "ООО Тест" in result


async def test_plan_proverok_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "plan_proverok", return_value=[]):
        result = await rpn_tools.plan_proverok(ctx, god=2024)
    assert "не получен" in result


async def test_spisok_sanpinov():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_sanpinov(ctx)
    assert "2.1.3684-21" in result


async def test_zhaloby_potrebiteley_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_zhalob", return_value=[]):
        result = await rpn_tools.zhaloby_potrebiteley(ctx)
    assert "не найдены" in result


async def test_zhaloby_potrebiteley_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "tema": "Некачественный товар",
            "organizaciya": "ООО Тест",
            "data_podachi": "2024-03-01",
            "status_rassmotreniya": "Рассматривается",
            "rezultat": "",
        }
    ]
    with patch.object(rpn_tools.client, "poisk_zhalob", return_value=mock_data):
        result = await rpn_tools.zhaloby_potrebiteley(ctx, organizaciya="ООО Тест")
    assert "Некачественный товар" in result


async def test_pokazateli_bezopasnosti():
    ctx = _maket_konteksta()
    result = await rpn_tools.pokazateli_bezopasnosti(ctx)
    assert "ЕМИСС" in result or "rospotrebnadzor" in result
