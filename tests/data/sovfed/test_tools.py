"""Тесты инструментов модуля Совет Федерации РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.sovfed import tools as sovfed_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_senatorov():
    ctx = _maket_konteksta()
    with patch.object(sovfed_tools.client, "poisk_senatorov", return_value=[]):
        result = await sovfed_tools.spisok_senatorov(ctx)
    assert isinstance(result, str)


async def test_spisok_senatorov_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "1",
            "familiya": "Матвиенко",
            "imya": "Валентина",
            "otchestvo": "Ивановна",
            "subiekt": "г. Санкт-Петербург",
            "dolzhnost": "Председатель Совета Федерации",
            "komitet": "",
        },
    ]
    with patch.object(sovfed_tools.client, "poisk_senatorov", return_value=mock_data):
        result = await sovfed_tools.spisok_senatorov(ctx)
    assert "Матвиенко" in result


async def test_info_senatora_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(sovfed_tools.client, "info_senatora", return_value=None):
        result = await sovfed_tools.info_senatora("nesushchestvuyushchiy", ctx)
    assert "не найден" in result


async def test_info_senatora_nayden():
    ctx = _maket_konteksta()
    mock_data = {
        "nomer": "1",
        "familiya": "Матвиенко",
        "imya": "Валентина",
        "otchestvo": "Ивановна",
        "subiekt": "г. Санкт-Петербург",
        "dolzhnost": "Председатель Совета Федерации",
        "komitet": "",
        "data_naznacheniya": "2011",
    }
    with patch.object(sovfed_tools.client, "info_senatora", return_value=mock_data):
        result = await sovfed_tools.info_senatora("1", ctx)
    assert "Матвиенко" in result


async def test_spisok_komitetov():
    ctx = _maket_konteksta()
    result = await sovfed_tools.spisok_komitetov(ctx)
    assert "Комитет" in result


async def test_spisok_komissiy():
    ctx = _maket_konteksta()
    result = await sovfed_tools.spisok_komissiy(ctx)
    assert "Комиссия" in result or "комиссия" in result.lower()


async def test_poisk_zakonoproektov_pustoy():
    ctx = _maket_konteksta()
    with patch.object(sovfed_tools.client, "poisk_zakonoproektov", return_value=[]):
        result = await sovfed_tools.poisk_zakonoproektov(ctx)
    assert isinstance(result, str)


async def test_poisk_zakonoproektov_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "СФ-001",
            "nazvanie": "О федеральном бюджете",
            "sostoyanie": "Принят",
            "data_rassmotreniya": "2026-01-15",
        },
    ]
    with patch.object(sovfed_tools.client, "poisk_zakonoproektov", return_value=mock_data):
        result = await sovfed_tools.poisk_zakonoproektov(ctx)
    assert "федеральном бюджете" in result


async def test_spisok_zasedaniy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(sovfed_tools.client, "spisok_zasedaniy", return_value=[]):
        result = await sovfed_tools.spisok_zasedaniy(ctx)
    assert isinstance(result, str)


async def test_spisok_zasedaniy_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "1",
            "data": "2026-01-15",
            "sostoyanie": "Состоялось",
            "povestka": "О бюджете",
        },
    ]
    with patch.object(sovfed_tools.client, "spisok_zasedaniy", return_value=mock_data):
        result = await sovfed_tools.spisok_zasedaniy(ctx, god=2026)
    assert "2026-01-15" in result
