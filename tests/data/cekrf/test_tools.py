"""Тесты инструментов модуля ЦИК РФ."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.cekrf import tools as cekrf_tools


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_tipy_vyborov():
    """Проверка tipy_vyborov."""
    ctx = _mock_ctx()
    result = await cekrf_tools.tipy_vyborov(ctx)
    assert "Типы выборов" in result
    assert "Президент" in result


async def test_subyekty_rf():
    """Проверка subyekty_rf."""
    ctx = _mock_ctx()
    result = await cekrf_tools.subyekty_rf(ctx)
    assert "Субъекты" in result
    assert "Москва" in result


async def test_dolzhnosti_federal():
    """Проверка dolzhnosti_federal."""
    ctx = _mock_ctx()
    result = await cekrf_tools.dolzhnosti_federal(ctx)
    assert "должност" in result.lower()


async def test_partii_rf():
    """Проверка partii_rf."""
    ctx = _mock_ctx()
    result = await cekrf_tools.partii_rf(ctx)
    assert "Единая Россия" in result


async def test_gody_vyborov():
    """Проверка gody_vyborov."""
    ctx = _mock_ctx()
    result = await cekrf_tools.gody_vyborov(ctx)
    assert "2024" in result


async def test_poisk_kandidata_not_found():
    """Проверка poisk_kandidata при отсутствии результатов."""
    ctx = _mock_ctx()
    with patch.object(cekrf_tools.client, "poisk_kandidata", return_value=[]):
        result = await cekrf_tools.poisk_kandidata("Иванов", ctx)
    assert "не найден" in result


async def test_kandidat_podrobno_not_found():
    """Проверка kandidat_podrobno при отсутствии кандидата."""
    ctx = _mock_ctx()
    with patch.object(cekrf_tools.client, "kandidat_podrobno", return_value=None):
        result = await cekrf_tools.kandidat_podrobno("nonexistent", ctx)
    assert "не найден" in result


async def test_rezultaty_vyborov_empty():
    """Проверка rezultaty_vyborov при отсутствии данных."""
    ctx = _mock_ctx()
    with patch.object(cekrf_tools.client, "rezultaty_vyborov", return_value=[]):
        result = await cekrf_tools.rezultaty_vyborov(ctx, god=2024)
    assert "недоступны" in result or "ГАС" in result


async def test_yavka_i_itogi():
    """Проверка yavka_i_itogi."""
    ctx = _mock_ctx()
    with patch.object(cekrf_tools.client, "yavka_i_itogi") as mock_yavka:
        mock_yavka.return_value = {
            "god": 2024,
            "vseh_izbirateley": 1000000,
            "progalosovalo": 650000,
            "yavka_procent": 65.0,
        }
        result = await cekrf_tools.yavka_i_itogi(ctx, god=2024)
    assert "65" in result
    assert "избирател" in result
