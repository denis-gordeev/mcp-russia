"""Тесты инструментов модуля Картотека арбитражных дел."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.kad_arbitrazh import client as kad_client
from mcp_russia.data.kad_arbitrazh import tools as kad_tools
from mcp_russia.data.kad_arbitrazh.schemas import SudebnoeDelo


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


class TestParserRezultatyPoiska:
    def test_parse_list(self) -> None:
        data = [
            {
                "CaseNumber": "А40-12345/2024",
                "Court": "АС г. Москвы",
                "Status": "Рассмотрение",
                "Judge": "Иванов И.И.",
                "Plaintiffs": "ООО Альфа",
                "Defendants": "ООО Бета",
                "ClaimSum": 1000000,
            }
        ]
        results = kad_client._parse_rezultaty_poiska(data)
        assert len(results) == 1
        assert results[0].nomer == "А40-12345/2024"
        assert results[0].nazvanie_suda == "АС г. Москвы"
        assert results[0].summa_iska == 1000000.0
        assert "ООО Альфа" in results[0].istorcy

    def test_parse_dict_with_instances(self) -> None:
        data = {
            "Instances": [
                {
                    "CaseInfo": {
                        "CaseNumber": "А77-5678/2023",
                        "Court": "АС г. Санкт-Петербурга",
                        "Status": "Завершено",
                        "Judge": "Петров П.П.",
                        "Plaintiffs": "Иванов А.Б.",
                        "Defendants": "Минфин РФ",
                    }
                }
            ]
        }
        results = kad_client._parse_rezultaty_poiska(data)
        assert len(results) == 1
        assert results[0].nomer == "А77-5678/2023"

    def test_parse_empty(self) -> None:
        assert kad_client._parse_rezultaty_poiska(None) == []
        assert kad_client._parse_rezultaty_poiska([]) == []

    def test_opredelit_sud(self) -> None:
        assert kad_client._opredelit_sud_po_nomeru("А40-12345/2024") == "АС г. Москвы"
        assert (
            kad_client._opredelit_sud_po_nomeru("А77-999/2024")
            == "АС г. Санкт-Петербурга и Ленинградской области"
        )
        assert kad_client._opredelit_sud_po_nomeru("А99-1/2024") == ""

    def test_opredelit_kategoriyu(self) -> None:
        assert kad_client._opredelit_kategoriyu("А40Б-12345/2024") == "Банкротство"
        assert kad_client._opredelit_kategoriyu("А40А-12345/2024") == "Административные дела"
        assert kad_client._opredelit_kategoriyu("А40-12345/2024") == ""


class TestParserKartochkaDela:
    def test_parse_full(self) -> None:
        data = {
            "CaseInfo": {
                "CaseNumber": "А40-11111/2025",
                "Court": "АС г. Москвы",
                "Category": "Банкротство",
                "Status": "На рассмотрении",
                "Judge": "Сидоров С.С.",
                "RegistrationDate": "2025-01-15",
                "LastDocumentDate": "2025-03-20",
                "Plaintiffs": "Кредитор ООО",
                "Defendants": "Должник ООО",
                "ClaimSum": 5000000,
            }
        }
        result = kad_client._parse_kartochka_dela(data)
        assert result is not None
        assert result.nomer == "А40-11111/2025"
        assert result.kategoriya == "Банкротство"
        assert result.summa_iska == 5000000.0

    def test_parse_none(self) -> None:
        assert kad_client._parse_kartochka_dela(None) is None
        assert kad_client._parse_kartochka_dela({}) is None


class TestParserAkty:
    def test_parse_documents(self) -> None:
        data = {
            "Documents": [
                {
                    "Document": {
                        "Id": 12345,
                        "DocumentType": "Решение",
                        "DocumentDate": "2025-02-10",
                        "CourtName": "АС г. Москвы",
                        "Judge": "Иванов И.И.",
                        "ShortContent": "Иск удовлетворён",
                        "Resolution": "Удовлетворить",
                    }
                }
            ]
        }
        results = kad_client._parse_akty(data, "А40-12345/2024")
        assert len(results) == 1
        assert results[0].tip_akta == "Решение"
        assert results[0].delo_nomer == "А40-12345/2024"

    def test_parse_empty(self) -> None:
        assert kad_client._parse_akty(None, "А40-1/2024") == []


class TestParserStorony:
    def test_parse_sides(self) -> None:
        data = {
            "Plaintiffs": ["ООО Альфа", "Иванов И.И."],
            "Defendants": ["ООО Бета", "Минфин РФ"],
        }
        results = kad_client._parse_storony(data, "А40-12345/2024")
        assert len(results) == 4
        istorcy = [s for s in results if s.tip == "истец"]
        otvetchiki = [s for s in results if s.tip == "ответчик"]
        assert len(istorcy) == 2
        assert len(otvetchiki) == 2

    def test_parse_string_sides(self) -> None:
        data = {
            "Plaintiffs": "ООО Альфа, ООО Гамма",
            "Defendants": "ООО Бета",
        }
        results = kad_client._parse_storony(data, "А40-12345/2024")
        assert len(results) == 3


async def test_poisk_del_empty():
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "poisk_del", return_value=[]):
        result = await kad_tools.poisk_del(ctx=ctx)
    assert "Картотека арбитражных дел" in result
    assert "не найдены" in result


async def test_poisk_del_with_results():
    ctx = _mock_ctx()
    mock_dela = [
        SudebnoeDelo(
            nomer="А40-12345/2024",
            kategoriya="Банкротство",
            sostoyanie="На рассмотрении",
            sudya="Иванов И.И.",
            nazvanie_suda="АС г. Москвы",
            summa_iska=1000000,
            istorcy=["ООО Альфа"],
            otvetchiki=["ООО Бета"],
        )
    ]
    with patch.object(kad_tools.client, "poisk_del", return_value=mock_dela):
        result = await kad_tools.poisk_del(nomer="А40-12345/2024", ctx=ctx)
    assert "А40-12345/2024" in result
    assert "1 000 000" in result or "1000000" in result or "₽" in result


async def test_poisk_del_with_filters():
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "poisk_del", return_value=[]):
        result = await kad_tools.poisk_del(nomer="А40-12345/2024", istorcz="ООО Ромашка", ctx=ctx)
    assert "А40-12345/2024" in result
    assert "Ромашка" in result


async def test_info_dela_not_found():
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "info_dela", return_value=None):
        result = await kad_tools.info_dela("А40-00000/2024", ctx)
    assert "не найдено" in result


async def test_info_dela_found():
    ctx = _mock_ctx()
    mock_delo = SudebnoeDelo(
        nomer="А40-12345/2024",
        kategoriya="Банкротство",
        sostoyanie="На рассмотрении",
        sudya="Иванов И.И.",
        sud_name="АС г. Москвы",
        data_vozbuzhdeniya="2024-01-15",
        istorcy=["ООО Альфа"],
        otvetchiki=["ООО Бета"],
        summa_iska=500000,
    )
    with patch.object(kad_tools.client, "info_dela", return_value=mock_delo):
        result = await kad_tools.info_dela("А40-12345/2024", ctx)
    assert "А40-12345/2024" in result
    assert "Банкротство" in result


async def test_akty_po_delu_not_found():
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "akty_po_delu", return_value=[]):
        result = await kad_tools.akty_po_delu("А40-00000/2024", ctx)
    assert "не найдены" in result


async def test_storony_dela_not_found():
    ctx = _mock_ctx()
    with patch.object(kad_tools.client, "storony_dela", return_value=[]):
        result = await kad_tools.storony_dela("А40-00000/2024", ctx)
    assert "не найдены" in result


async def test_spravochnik_kategoriy():
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_kategoriy(ctx)
    assert "Категории" in result
    assert "Банкротство" in result


async def test_spravochnik_instantsiy():
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_instantsiy(ctx)
    assert "Инстанции" in result
    assert "первая инстанция" in result


async def test_spravochnik_statusov():
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_statusov(ctx)
    assert "Статусы" in result
    assert "Новое" in result


async def test_spravochnik_aktov():
    ctx = _mock_ctx()
    result = await kad_tools.spravochnik_aktov(ctx)
    assert "Типы судебных актов" in result
    assert "Решение" in result
