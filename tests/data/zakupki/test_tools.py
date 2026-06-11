"""Тесты инструментов модуля Закупки (ЕИС)."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.zakupki import client as zakupki_client
from mcp_russia.data.zakupki import tools as zakupki_tools
from mcp_russia.data.zakupki.schemas import Kontrakt, Zakupka


def _mock_ctx():
    """Создать мок контекста."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# --- Parser tests ---


def test_parse_zakupki_search():
    data = {
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
    result = zakupki_client._parse_zakupki_search(data)
    assert len(result) == 1
    assert result[0].number == "0123400000125000001"
    assert result[0].initial_price == 1500000.0


def test_parse_zakupki_search_empty():
    assert zakupki_client._parse_zakupki_search(None) == []
    assert zakupki_client._parse_zakupki_search("not a list") == []


def test_parse_kontrakty():
    data = {
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
    result = zakupki_client._parse_kontrakty(data)
    assert len(result) == 1
    assert result[0].contractor_name == "ООО Ромашка"
    assert result[0].price == 500000.0


def test_determine_zakon():
    assert zakupki_client._determine_zakon({"fz": "44"}) == "44-ФЗ"
    assert zakupki_client._determine_zakon({"fz": "223"}) == "223-ФЗ"
    assert zakupki_client._determine_zakon({"fz": ""}) == ""


def test_safe_float():
    assert zakupki_client._safe_float(None) == 0.0
    assert zakupki_client._safe_float("abc") == 0.0
    assert zakupki_client._safe_float(100) == 100.0
    assert zakupki_client._safe_float("200.5") == 200.5


# --- Tool tests (all HTTP calls mocked) ---


async def test_poisk_zakupok_empty():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=[]):
        result = await zakupki_tools.poisk_zakupok(ctx=ctx)
    assert "ЕИС" in result or "zakupki.gov.ru" in result


async def test_poisk_zakupok_with_data():
    ctx = _mock_ctx()
    zakupki = [
        Zakupka(
            id="1",
            number="0123400000125000001",
            title="Поставка компьютеров",
            zakon="44-ФЗ",
            sposob="Электронный аукцион",
            status="Подача заявок",
            initial_price=1500000.0,
            publish_date="2025-01-15",
            organizer_name="Минобразования",
            organizer_inn="7700000000",
        )
    ]
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=zakupki):
        result = await zakupki_tools.poisk_zakupok(zapros="компьютеры", ctx=ctx)
    assert "0123400000125000001" in result
    assert "44-ФЗ" in result


async def test_poisk_zakupok_with_filters():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "poisk_zakupok", return_value=[]):
        result = await zakupki_tools.poisk_zakupok(
            zapros="компьютеры", zakon="44-ФЗ", region="Москва", ctx=ctx
        )
    assert "компьютеры" in result
    assert "44-ФЗ" in result
    assert "Москва" in result


async def test_info_zakupki_not_found():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "poluchit_zakupku", return_value=None):
        result = await zakupki_tools.info_zakupki("0000000001", ctx)
    assert "не найдена" in result


async def test_info_zakupki_found():
    ctx = _mock_ctx()
    zakupka = Zakupka(
        id="1",
        number="0123400000125000001",
        title="Поставка компьютеров",
        zakon="44-ФЗ",
        sposob="Электронный аукцион",
        status="Подача заявок",
        initial_price=1500000.0,
        publish_date="2025-01-15",
        deadline="2025-02-01",
        organizer_name="Минобразования",
        organizer_inn="7700000000",
    )
    with patch.object(zakupki_tools.client, "poluchit_zakupku", return_value=zakupka):
        result = await zakupki_tools.info_zakupki("0123400000125000001", ctx)
    assert "0123400000125000001" in result
    assert "44-ФЗ" in result
    assert "Срок подачи" in result


async def test_poisk_kontraktov_empty():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "poisk_kontraktov", return_value=[]):
        result = await zakupki_tools.poisk_kontraktov(ctx=ctx)
    assert "контракт" in result.lower() or "ЕИС" in result


async def test_poisk_kontraktov_with_data():
    ctx = _mock_ctx()
    kontrakty = [
        Kontrakt(
            id="1",
            number="12345678901",
            zakupka_number="0123400000125000001",
            contractor_name="ООО Ромашка",
            contractor_inn="7700000001",
            price=500000.0,
            sign_date="2025-02-01",
            status="Исполнение",
        )
    ]
    with patch.object(zakupki_tools.client, "poisk_kontraktov", return_value=kontrakty):
        result = await zakupki_tools.poisk_kontraktov(inn_postavshchika="7700000001", ctx=ctx)
    assert "ООО Ромашка" in result


async def test_info_zakazchika_not_found():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "info_zakazchika", return_value=None):
        result = await zakupki_tools.info_zakazchika("0000000000", ctx)
    assert "не найден" in result


async def test_info_postavshchika_not_found():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "info_postavshchika", return_value=None):
        result = await zakupki_tools.info_postavshchika("0000000000", ctx)
    assert "не найден" in result


async def test_statusy_zakupok():
    ctx = _mock_ctx()
    result = await zakupki_tools.statusy_zakupok(ctx)
    assert "Статусы" in result
    assert "Планирование" in result


async def test_sposoby_zakupok():
    ctx = _mock_ctx()
    result = await zakupki_tools.sposoby_zakupok(ctx)
    assert "Способы" in result
    assert "Электронный аукцион" in result


async def test_plany_zakupok_empty():
    ctx = _mock_ctx()
    with patch.object(zakupki_tools.client, "plany_zakupok", return_value=[]):
        result = await zakupki_tools.plany_zakupok(god=2025, ctx=ctx)
    assert "2025" in result
    assert "Планы-графики" in result


async def test_auth_note_without_token():
    with patch.object(zakupki_tools.client, "_get_api_token", return_value=""):
        assert "MCP_RUSSIA_ZAKUPKI_API_TOKEN" in zakupki_tools._auth_note()


async def test_auth_note_with_token():
    with patch.object(zakupki_tools.client, "_get_api_token", return_value="secret"):
        assert zakupki_tools._auth_note() == ""
