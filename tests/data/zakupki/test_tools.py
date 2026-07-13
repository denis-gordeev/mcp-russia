"""Тесты инструментов модуля Закупки (ЕИС)."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.zakupki import client as zakupki_client
from mcp_russia.data.zakupki import tools as zakupki_tools
from mcp_russia.data.zakupki.schemas import Kontrakt, Zakupka


def _maket_konteksta():
    """Создать мок контекста."""
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


# --- Тесты парсера ---


def test_razobrat_poisk_zakupok():
    dannye = {
        "results": [
            {
                "id": 1,
                "regNumber": "0123400000125000001",
                "name": "Поставка компьютерного оборудования",
                "purchaseMethod": "Электронный аукцион",
                "commonStatus": "Подача заявок",
                "price": 1500000.0,
                "customerName": "Министерство образования",
                "customerInn": "7700000000",
                "docPublishDate": "2025-01-15",
            }
        ]
    }
    rezultat = zakupki_client._razobrat_poisk_zakupok(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].nomer == "0123400000125000001"
    assert rezultat[0].nachalnaya_tsena == 1500000.0


def test_razobrat_poisk_zakupok_pustoy():
    assert zakupki_client._razobrat_poisk_zakupok(None) == []
    assert zakupki_client._razobrat_poisk_zakupok("ne spisok") == []


def test_razobrat_kontrakty():
    dannye = {
        "results": [
            {
                "id": 100,
                "regNum": "12345678901",
                "supplierName": "ООО Ромашка",
                "supplierInn": "7700000001",
                "price": 500000.0,
                "signDate": "2025-02-01",
                "contractStatus": "Исполнение",
            }
        ]
    }
    rezultat = zakupki_client._razobrat_kontrakty(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].nazvanie_podryadchika == "ООО Ромашка"
    assert rezultat[0].tsena == 500000.0


def test_opredelit_zakon():
    assert zakupki_client._opredelit_zakon({"fz": "44"}) == "44-ФЗ"
    assert zakupki_client._opredelit_zakon({"fz": "223"}) == "223-ФЗ"
    assert zakupki_client._opredelit_zakon({"fz": ""}) == ""


def test_bezopasnoe_veshchestvennoe():
    assert zakupki_client._bezopasnoe_veshchestvennoe(None) == 0.0
    assert zakupki_client._bezopasnoe_veshchestvennoe("abc") == 0.0
    assert zakupki_client._bezopasnoe_veshchestvennoe(100) == 100.0
    assert zakupki_client._bezopasnoe_veshchestvennoe("200.5") == 200.5


# --- Тесты инструментов (все HTTP-вызовы замоканы) ---


async def test_poisk_zakupok_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=[]):
        rezultat = await zakupki_tools.poisk_zakupok(kontekst=kontekst)
    assert "ЕИС" in rezultat or "zakupki.gov.ru" in rezultat


async def test_poisk_zakupok_s_dannymi():
    kontekst = _maket_konteksta()
    zakupki = [
        Zakupka(
            identifikator="1",
            nomer="0123400000125000001",
            nazvanie="Поставка компьютеров",
            zakon="44-ФЗ",
            sposob="Электронный аукцион",
            sostoyanie="Подача заявок",
            nachalnaya_tsena=1500000.0,
            data_publikatsii="2025-01-15",
            nazvanie_organizatora="Минобразования",
            organizator_inn="7700000000",
        )
    ]
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=zakupki):
        rezultat = await zakupki_tools.poisk_zakupok(zapros="компьютеры", kontekst=kontekst)
    assert "0123400000125000001" in rezultat
    assert "44-ФЗ" in rezultat


async def test_poisk_zakupok_s_filtrami():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=[]):
        rezultat = await zakupki_tools.poisk_zakupok(
            zapros="компьютеры", zakon="44-ФЗ", subiekt="Москва", kontekst=kontekst
        )
    assert "компьютеры" in rezultat
    assert "44-ФЗ" in rezultat
    assert "Москва" in rezultat


async def test_info_zakupki_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "poluchit_zakupku", return_value=None):
        rezultat = await zakupki_tools.info_zakupki("0000000001", kontekst)
    assert "не найдена" in rezultat


async def test_info_zakupki_nayden():
    kontekst = _maket_konteksta()
    zakupka = Zakupka(
        identifikator="1",
        nomer="0123400000125000001",
        nazvanie="Поставка компьютеров",
        zakon="44-ФЗ",
        sposob="Электронный аукцион",
        sostoyanie="Подача заявок",
        nachalnaya_tsena=1500000.0,
        data_publikatsii="2025-01-15",
        srok_podachi="2025-02-01",
        nazvanie_organizatora="Минобразования",
        organizator_inn="7700000000",
    )
    with patch.object(zakupki_tools.client, "poluchit_zakupku", return_value=zakupka):
        rezultat = await zakupki_tools.info_zakupki("0123400000125000001", kontekst)
    assert "0123400000125000001" in rezultat
    assert "44-ФЗ" in rezultat
    assert "Срок подачи" in rezultat


async def test_poisk_kontraktov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "poisk_kontraktov", return_value=[]):
        rezultat = await zakupki_tools.poisk_kontraktov(kontekst=kontekst)
    assert "контракт" in rezultat.lower() or "ЕИС" in rezultat


async def test_poisk_kontraktov_s_dannymi():
    kontekst = _maket_konteksta()
    kontrakty = [
        Kontrakt(
            identifikator="1",
            nomer="12345678901",
            zakupka_nomer="0123400000125000001",
            nazvanie_podryadchika="ООО Ромашка",
            podryadchik_inn="7700000001",
            tsena=500000.0,
            data_podpisaniya="2025-02-01",
            sostoyanie="Исполнение",
        )
    ]
    with patch.object(zakupki_tools.client, "poisk_kontraktov", return_value=kontrakty):
        rezultat = await zakupki_tools.poisk_kontraktov(
            inn_postavshchika="7700000001", kontekst=kontekst
        )
    assert "ООО Ромашка" in rezultat


async def test_info_zakazchika_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "info_zakazchika", return_value=None):
        rezultat = await zakupki_tools.info_zakazchika("0000000000", kontekst)
    assert "не найден" in rezultat


async def test_info_postavshchika_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "info_postavshchika", return_value=None):
        rezultat = await zakupki_tools.info_postavshchika("0000000000", kontekst)
    assert "не найден" in rezultat


async def test_statusy_zakupok():
    kontekst = _maket_konteksta()
    rezultat = await zakupki_tools.statusy_zakupok(kontekst)
    assert "Статусы" in rezultat
    assert "Планирование" in rezultat


async def test_sposoby_zakupok():
    kontekst = _maket_konteksta()
    rezultat = await zakupki_tools.sposoby_zakupok(kontekst)
    assert "Способы" in rezultat
    assert "Электронный аукцион" in rezultat


async def test_plany_zakupok_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(zakupki_tools.client, "plany_zakupok", return_value=[]):
        rezultat = await zakupki_tools.plany_zakupok(god=2025, kontekst=kontekst)
    assert "2025" in rezultat
    assert "Планы-графики" in rezultat


async def test_zametka_ob_aut_bez_tokena():
    with patch.object(zakupki_tools.client, "_poluchit_api_token", return_value=""):
        assert "MCP_RUSSIA_ZAKUPKI_API_TOKEN" in zakupki_tools._zametka_ob_avtorizatsii()


async def test_zametka_ob_aut_s_tokenom():
    with patch.object(zakupki_tools.client, "_poluchit_api_token", return_value="taynyy_klyuch"):
        assert zakupki_tools._zametka_ob_avtorizatsii() == ""
