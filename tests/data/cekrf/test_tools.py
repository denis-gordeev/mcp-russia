"""Тесты инструментов модуля ЦИК РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.cekrf import tools as cekrf_tools


def _maket_konteksta():
    """Создать мок контекста."""
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_tipy_vyborov():
    """Проверка tipy_vyborov."""
    kontekst = _maket_konteksta()
    rezultat = await cekrf_tools.tipy_vyborov(kontekst)
    assert "Типы выборов" in rezultat
    assert "Президент" in rezultat


async def test_subyekty_rf():
    """Проверка subyekty_rf."""
    kontekst = _maket_konteksta()
    rezultat = await cekrf_tools.subyekty_rf(kontekst)
    assert "Субъекты" in rezultat
    assert "Москва" in rezultat


async def test_dolzhnosti_federal():
    """Проверка dolzhnosti_federal."""
    kontekst = _maket_konteksta()
    rezultat = await cekrf_tools.dolzhnosti_federal(kontekst)
    assert "должност" in rezultat.lower()


async def test_partii_rf():
    """Проверка partii_rf."""
    kontekst = _maket_konteksta()
    rezultat = await cekrf_tools.partii_rf(kontekst)
    assert "Единая Россия" in rezultat


async def test_gody_vyborov():
    """Проверка gody_vyborov."""
    kontekst = _maket_konteksta()
    rezultat = await cekrf_tools.gody_vyborov(kontekst)
    assert "2024" in rezultat


async def test_poisk_kandidata_ne_nayden():
    """Проверка poisk_kandidata при отсутствии результатов."""
    kontekst = _maket_konteksta()
    with patch.object(cekrf_tools.client, "poisk_kandidata", return_value=[]):
        rezultat = await cekrf_tools.poisk_kandidata("Иванов", kontekst)
    assert "не найден" in rezultat


async def test_kandidat_podrobno_ne_nayden():
    """Проверка kandidat_podrobno при отсутствии кандидата."""
    kontekst = _maket_konteksta()
    with patch.object(cekrf_tools.client, "kandidat_podrobno", return_value=None):
        rezultat = await cekrf_tools.kandidat_podrobno("nesushchestvuyushchiy", kontekst)
    assert "не найден" in rezultat


async def test_rezultaty_vyborov_pustoy():
    """Проверка rezultaty_vyborov при отсутствии данных."""
    kontekst = _maket_konteksta()
    with patch.object(cekrf_tools.client, "rezultaty_vyborov", return_value=[]):
        rezultat = await cekrf_tools.rezultaty_vyborov(kontekst, god=2024)
    assert "недоступны" in rezultat or "ГАС" in rezultat


async def test_yavka_i_itogi():
    """Проверка yavka_i_itogi."""
    kontekst = _maket_konteksta()
    with patch.object(cekrf_tools.client, "yavka_i_itogi") as maket_yavka:
        maket_yavka.return_value = {
            "god": 2024,
            "vseh_izbirateley": 1000000,
            "progalosovalo": 650000,
            "yavka_procent": 65.0,
        }
        rezultat = await cekrf_tools.yavka_i_itogi(kontekst, god=2024)
    assert "65" in rezultat
    assert "избирател" in rezultat
