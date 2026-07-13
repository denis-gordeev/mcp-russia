"""Тесты инструментов модуля Официальные публикации РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.publikatsii import tools as publikatsii_tools


def _maket_konteksta():
    """Создать мок контекста."""
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_tipov_aktov():
    """Проверка spisok_tipov_aktov."""
    kontekst = _maket_konteksta()
    rezultat = await publikatsii_tools.spisok_tipov_aktov(kontekst)
    assert "нормативных актов" in rezultat
    assert "Федеральный закон" in rezultat


async def test_spisok_otrasley():
    """Проверка spisok_otrasley."""
    kontekst = _maket_konteksta()
    rezultat = await publikatsii_tools.spisok_otrasley(kontekst)
    assert "Отрасли законодательства" in rezultat
    assert "Гражданское" in rezultat


async def test_spisok_istochnikov():
    """Проверка spisok_istochnikov."""
    kontekst = _maket_konteksta()
    rezultat = await publikatsii_tools.spisok_istochnikov(kontekst)
    assert "Источники" in rezultat
    assert "pravo.gov.ru" in rezultat


async def test_spisok_statusov():
    """Проверка spisok_statusov."""
    kontekst = _maket_konteksta()
    rezultat = await publikatsii_tools.spisok_statusov(kontekst)
    assert "Статусы" in rezultat
    assert "Действующий" in rezultat


async def test_info_normativnogo_akta_ne_nayden():
    """Проверка info_normativnogo_akta при отсутствии данных."""
    kontekst = _maket_konteksta()
    with patch.object(publikatsii_tools.client, "poluchit_normativnyy_akt", return_value=None):
        rezultat = await publikatsii_tools.info_normativnogo_akta(
            nomer="nesushchestvuyushchiy", kontekst=kontekst
        )
    assert "не найден" in rezultat


async def test_info_zakonproekta_ne_nayden():
    """Проверка info_zakonproekta при отсутствии данных."""
    kontekst = _maket_konteksta()
    with patch.object(publikatsii_tools.client, "poluchit_zakon_proekt", return_value=None):
        rezultat = await publikatsii_tools.info_zakonproekta(
            nomer="nesushchestvuyushchiy", kontekst=kontekst
        )
    assert "не найден" in rezultat


async def test_poisk_aktov_pustoy():
    """Проверка poisk_aktov при отсутствии результатов."""
    kontekst = _maket_konteksta()
    with patch.object(publikatsii_tools.client, "poluchit_poisku", return_value=[]):
        rezultat = await publikatsii_tools.poisk_aktov(tekst="неверный запрос", kontekst=kontekst)
    assert "не найдены" in rezultat


async def test_publikatsii_po_datam_pustoy():
    """Проверка publikatsii_po_datam при отсутствии данных."""
    kontekst = _maket_konteksta()
    with patch.object(publikatsii_tools.client, "poluchit_publikatsii", return_value=[]):
        rezultat = await publikatsii_tools.publikatsii_po_datam(tip="fz", kontekst=kontekst)
    assert "не найдены" in rezultat


async def test_izmeneniya_akta_pustoy():
    """Проверка izmeneniya_akta при отсутствии данных."""
    kontekst = _maket_konteksta()
    with patch.object(publikatsii_tools.client, "poluchit_izmeneniya_akta", return_value=[]):
        rezultat = await publikatsii_tools.izmeneniya_akta(
            akt_nomer="nesushchestvuyushchiy", kontekst=kontekst
        )
    assert "не найдено" in rezultat
