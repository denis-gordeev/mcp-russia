"""Тесты инструментов модуля ЦИК РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.cekrf import tools as cekrf_tools


def _maket_konteksta():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_tipy_vyborov():
    """Проверка tipy_vyborov."""
    ctx = _maket_konteksta()
    rezultat = await cekrf_tools.tipy_vyborov(ctx)
    assert "Типы выборов" in rezultat
    assert "Президент" in rezultat


async def test_subyekty_rf():
    """Проверка subyekty_rf."""
    ctx = _maket_konteksta()
    rezultat = await cekrf_tools.subyekty_rf(ctx)
    assert "Субъекты" in rezultat
    assert "Москва" in rezultat


async def test_dolzhnosti_federal():
    """Проверка dolzhnosti_federal."""
    ctx = _maket_konteksta()
    rezultat = await cekrf_tools.dolzhnosti_federal(ctx)
    assert "должност" in rezultat.lower()


async def test_partii_rf():
    """Проверка partii_rf."""
    ctx = _maket_konteksta()
    rezultat = await cekrf_tools.partii_rf(ctx)
    assert "Единая Россия" in rezultat


async def test_gody_vyborov():
    """Проверка gody_vyborov."""
    ctx = _maket_konteksta()
    rezultat = await cekrf_tools.gody_vyborov(ctx)
    assert "2024" in rezultat


async def test_poisk_kandidata_ne_nayden():
    """Проверка poisk_kandidata при отсутствии результатов."""
    ctx = _maket_konteksta()
    with patch.object(cekrf_tools.client, "poisk_kandidata", return_value=[]):
        rezultat = await cekrf_tools.poisk_kandidata("Иванов", ctx)
    assert "не найден" in rezultat


async def test_kandidat_podrobno_ne_nayden():
    """Проверка kandidat_podrobno при отсутствии кандидата."""
    ctx = _maket_konteksta()
    with patch.object(cekrf_tools.client, "kandidat_podrobno", return_value=None):
        rezultat = await cekrf_tools.kandidat_podrobno("nesushchestvuyushchiy", ctx)
    assert "не найден" in rezultat


async def test_rezultaty_vyborov_pustoy():
    """Проверка rezultaty_vyborov при отсутствии данных."""
    ctx = _maket_konteksta()
    with patch.object(cekrf_tools.client, "rezultaty_vyborov", return_value=[]):
        rezultat = await cekrf_tools.rezultaty_vyborov(ctx, god=2024)
    assert "недоступны" in rezultat or "ГАС" in rezultat


async def test_yavka_i_itogi():
    """Проверка yavka_i_itogi."""
    ctx = _maket_konteksta()
    with patch.object(cekrf_tools.client, "yavka_i_itogi") as mock_yavka:
        mock_yavka.return_value = {
            "god": 2024,
            "vseh_izbirateley": 1000000,
            "progalosovalo": 650000,
            "yavka_procent": 65.0,
        }
        rezultat = await cekrf_tools.yavka_i_itogi(ctx, god=2024)
    assert "65" in rezultat
    assert "избирател" in rezultat
