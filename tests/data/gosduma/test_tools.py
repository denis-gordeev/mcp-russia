"""Тесты инструментов модуля Госдума."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.gosduma import client as gosduma_client
from mcp_russia.data.gosduma import tools as gosduma_tools
from mcp_russia.data.gosduma.schemas import Deputat, Golosovanie, Zakonoproekt


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# --- Тесты парсера ---


def test_parse_deputats_list():
    data = [
        {
            "id": 1,
            "surname": "Иванов",
            "name": "Иван",
            "patronymic": "Иванович",
            "factionName": "Единая Россия",
            "committeeName": "Комитет по бюджету",
            "districtName": "Москва",
            "convocation": 8,
        }
    ]
    result = gosduma_client._parse_deputats(data)
    assert len(result) == 1
    assert result[0].фамилия == "Иванов"
    assert result[0].фракция == "Единая Россия"


def test_parse_deputats_dict():
    data = {
        "deputies": [
            {
                "id": 2,
                "lastName": "Петров",
                "firstName": "Пётр",
                "middleName": "Петрович",
                "faction": "КПРФ",
                "committee": "Комитет по обороне",
                "region": "Краснодар",
                "sozyv": "8",
            }
        ]
    }
    result = gosduma_client._parse_deputats(data)
    assert len(result) == 1
    assert result[0].фамилия == "Петров"
    assert result[0].фракция == "КПРФ"


def test_parse_deputats_empty():
    assert gosduma_client._parse_deputats(None) == []
    assert gosduma_client._parse_deputats("not a list") == []


def test_parse_zakonoproekty():
    data = {
        "bills": [
            {
                "id": 100,
                "number": "12345-8",
                "name": "О внесении изменений",
                "statusName": "Рассматривается",
                "dateIntroduction": "2025-01-15",
                "subjectName": "Депутаты ГД",
                "readingsCount": 1,
            }
        ]
    }
    result = gosduma_client._parse_zakonoproekty(data)
    assert len(result) == 1
    assert result[0].number == "12345-8"
    assert result[0].status == "Рассматривается"


def test_parse_golosovaniya():
    data = {
        "votes": [
            {
                "billId": 200,
                "subject": "О бюджете",
                "date": "2025-12-01",
                "totalFor": 300,
                "totalAgainst": 50,
                "totalAbstain": 10,
                "totalNotVoting": 90,
            }
        ]
    }
    result = gosduma_client._parse_golosovaniya(data)
    assert len(result) == 1
    assert result[0].za == 300
    assert result[0].protiv == 50


def test_parse_one_deputat():
    data = {
        "id": 1,
        "surname": "Сидоров",
        "name": "Сидор",
        "patronymic": "Сидорович",
        "factionName": "ЛДПР",
    }
    result = gosduma_client._parse_one_deputat(data)
    assert result is not None
    assert result.фамилия == "Сидоров"


def test_parse_one_deputat_none():
    assert gosduma_client._parse_one_deputat(None) is None
    assert gosduma_client._parse_one_deputat("string") is None


# --- Тесты инструментов (все HTTP-вызовы замоканы) ---


async def test_spisok_deputatov_empty():
    with patch.object(gosduma_tools.client, "poluchit_deputatov", return_value=[]):
        result = await gosduma_tools.spisok_deputatov(sozyv="8")
    assert "API" in result or "duma" in result.lower()


async def test_spisok_deputatov_with_data():
    deputats = [
        Deputat(
            id=1,
            фамилия="Иванов",
            имя="Иван",
            отчество="Иванович",
            фракция="Единая Россия",
            комитет="Бюджет",
            регион="Москва",
            созыв="8",
        ),
        Deputat(
            id=2,
            фамилия="Петров",
            имя="Пётр",
            отчество="Петрович",
            фракция="КПРФ",
            комитет="Оборона",
            регион="Краснодар",
            созыв="8",
        ),
    ]
    with patch.object(gosduma_tools.client, "poluchit_deputatov", return_value=deputats):
        result = await gosduma_tools.spisok_deputatov(sozyv="8")
    assert "Иванов" in result
    assert "Единая Россия" in result


async def test_info_deputata_not_found():
    ctx = _mock_ctx()
    with patch.object(gosduma_tools.client, "poluchit_deputata", return_value=None):
        result = await gosduma_tools.info_deputata(99999, ctx)
    assert "не найден" in result


async def test_info_deputata_found():
    ctx = _mock_ctx()
    deputat = Deputat(
        id=1,
        фамилия="Иванов",
        имя="Иван",
        отчество="Иванович",
        фракция="Единая Россия",
        комитет="Бюджет",
        регион="Москва",
        созыв="8",
    )
    with patch.object(gosduma_tools.client, "poluchit_deputata", return_value=deputat):
        result = await gosduma_tools.info_deputata(1, ctx)
    assert "Иванов" in result
    assert "Единая Россия" in result


async def test_spisok_frakcii():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_frakcii(ctx)
    assert "Единая Россия" in result
    assert "КПРФ" in result
    assert "ЛДПР" in result


async def test_spisok_komitetov():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_komitetov(ctx)
    assert "Комитет" in result
    assert "бюджет" in result.lower() or "обороне" in result.lower()


async def test_spisok_sozyvov():
    ctx = _mock_ctx()
    result = await gosduma_tools.spisok_sozyvov(ctx)
    assert "Созыв" in result
    assert "VIII" in result or "1993" in result


async def test_zakonoproekty_empty():
    with patch.object(gosduma_tools.client, "poluchit_zakonoproekty", return_value=[]):
        result = await gosduma_tools.zakonoproekty(status="принят")
    assert "Законопроект" in result or "СОЗД" in result


async def test_zakonoproekty_with_data():
    bills = [
        Zakonoproekt(
            id="1",
            number="12345-8",
            title="О внесении изменений",
            status="Рассматривается",
            data_vneseniya="2025-01-15",
            author="Депутаты ГД",
            readings=1,
        )
    ]
    with patch.object(gosduma_tools.client, "poluchit_zakonoproekty", return_value=bills):
        result = await gosduma_tools.zakonoproekty(status="рассматривается")
    assert "12345-8" in result
    assert "Рассматривается" in result


async def test_golosovaniya_empty():
    with patch.object(gosduma_tools.client, "poluchit_golosovaniya", return_value=[]):
        result = await gosduma_tools.golosovaniya(sozyv="8")
    assert "Голосован" in result or "API" in result or "duma" in result.lower()


async def test_golosovaniya_with_data():
    votes = [
        Golosovanie(
            zakonoproekt_id="1",
            title="О бюджете",
            data="2025-12-01",
            za=300,
            protiv=50,
            vozhderzhalsya=10,
            ne_golosoval=90,
        )
    ]
    with patch.object(gosduma_tools.client, "poluchit_golosovaniya", return_value=votes):
        result = await gosduma_tools.golosovaniya(sozyv="8")
    assert "О бюджете" in result
    assert "300" in result


async def test_auth_note_without_token():
    with patch.object(gosduma_tools.client, "_get_api_token", return_value=""):
        assert "MCP_RUSSIA_DUMA_API_TOKEN" in gosduma_tools._auth_note()


async def test_auth_note_with_token():
    with patch.object(gosduma_tools.client, "_get_api_token", return_value="secret"):
        assert gosduma_tools._auth_note() == ""
