"""Тесты инструментов модуля Госдума."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.gosduma import client as gosduma_client
from mcp_russia.data.gosduma import tools as gosduma_tools
from mcp_russia.data.gosduma.schemas import Deputat, Golosovanie, Zakonoproekt


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# --- Тесты парсера ---


def test_razobrat_deputatov_list():
    dannye = [
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
    rezultat = gosduma_client._razobrat_deputatov(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].фамилия == "Иванов"
    assert rezultat[0].фракция == "Единая Россия"


def test_razobrat_deputatov_dict():
    dannye = {
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
    rezultat = gosduma_client._razobrat_deputatov(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].фамилия == "Петров"
    assert rezultat[0].фракция == "КПРФ"


def test_razobrat_deputatov_pustoy():
    assert gosduma_client._razobrat_deputatov(None) == []
    assert gosduma_client._razobrat_deputatov("ne spisok") == []


def test_razobrat_zakonoproekty():
    dannye = {
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
    rezultat = gosduma_client._razobrat_zakonoproekty(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].nomer == "12345-8"
    assert rezultat[0].sostoyanie == "Рассматривается"


def test_razobrat_golosovaniya():
    dannye = {
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
    rezultat = gosduma_client._razobrat_golosovaniya(dannye)
    assert len(rezultat) == 1
    assert rezultat[0].za == 300
    assert rezultat[0].protiv == 50


def test_razobrat_odnogo_deputata():
    dannye = {
        "id": 1,
        "surname": "Сидоров",
        "name": "Сидор",
        "patronymic": "Сидорович",
        "factionName": "ЛДПР",
    }
    rezultat = gosduma_client._razobrat_odnogo_deputata(dannye)
    assert rezultat is not None
    assert rezultat.фамилия == "Сидоров"


def test_razobrat_odnogo_deputata_nichego():
    assert gosduma_client._razobrat_odnogo_deputata(None) is None
    assert gosduma_client._razobrat_odnogo_deputata("string") is None


# --- Тесты инструментов (все HTTP-вызовы замоканы) ---


async def test_spisok_deputatov_pustoy():
    with patch.object(gosduma_tools.client, "poluchit_deputatov", return_value=[]):
        rezultat = await gosduma_tools.spisok_deputatov(sozyv="8")
    assert "API" in rezultat or "duma" in rezultat.lower()


async def test_spisok_deputatov_s_dannymi():
    deputats = [
        Deputat(
            identifikator=1,
            фамилия="Иванов",
            имя="Иван",
            отчество="Иванович",
            фракция="Единая Россия",
            комитет="Бюджет",
            регион="Москва",
            созыв="8",
        ),
        Deputat(
            identifikator=2,
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
        rezultat = await gosduma_tools.spisok_deputatov(sozyv="8")
    assert "Иванов" in rezultat
    assert "Единая Россия" in rezultat


async def test_info_deputata_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(gosduma_tools.client, "poluchit_deputata", return_value=None):
        rezultat = await gosduma_tools.info_deputata(99999, ctx)
    assert "не найден" in rezultat


async def test_info_deputata_nayden():
    ctx = _maket_konteksta()
    deputat = Deputat(
        identifikator=1,
        фамилия="Иванов",
        имя="Иван",
        отчество="Иванович",
        фракция="Единая Россия",
        комитет="Бюджет",
        регион="Москва",
        созыв="8",
    )
    with patch.object(gosduma_tools.client, "poluchit_deputata", return_value=deputat):
        rezultat = await gosduma_tools.info_deputata(1, ctx)
    assert "Иванов" in rezultat
    assert "Единая Россия" in rezultat


async def test_spisok_frakcii():
    ctx = _maket_konteksta()
    rezultat = await gosduma_tools.spisok_frakcii(ctx)
    assert "Единая Россия" in rezultat
    assert "КПРФ" in rezultat
    assert "ЛДПР" in rezultat


async def test_spisok_komitetov():
    ctx = _maket_konteksta()
    rezultat = await gosduma_tools.spisok_komitetov(ctx)
    assert "Комитет" in rezultat
    assert "бюджет" in rezultat.lower() or "обороне" in rezultat.lower()


async def test_spisok_sozyvov():
    ctx = _maket_konteksta()
    rezultat = await gosduma_tools.spisok_sozyvov(ctx)
    assert "Созыв" in rezultat
    assert "VIII" in rezultat or "1993" in rezultat


async def test_zakonoproekty_pustoy():
    with patch.object(gosduma_tools.client, "poluchit_zakonoproekty", return_value=[]):
        rezultat = await gosduma_tools.zakonoproekty(sostoyanie="принят")
    assert "Законопроект" in rezultat or "СОЗД" in rezultat


async def test_zakonoproekty_s_dannymi():
    bills = [
        Zakonoproekt(
            identifikator="1",
            nomer="12345-8",
            nazvanie="О внесении изменений",
            sostoyanie="Рассматривается",
            data_vneseniya="2025-01-15",
            avtor="Депутаты ГД",
            chteniya=1,
        )
    ]
    with patch.object(gosduma_tools.client, "poluchit_zakonoproekty", return_value=bills):
        rezultat = await gosduma_tools.zakonoproekty(sostoyanie="рассматривается")
    assert "12345-8" in rezultat
    assert "Рассматривается" in rezultat


async def test_golosovaniya_pustoy():
    with patch.object(gosduma_tools.client, "poluchit_golosovaniya", return_value=[]):
        rezultat = await gosduma_tools.golosovaniya(sozyv="8")
    assert "Голосован" in rezultat or "API" in rezultat or "duma" in rezultat.lower()


async def test_golosovaniya_s_dannymi():
    votes = [
        Golosovanie(
            zakonoproekt_identifikator="1",
            nazvanie="О бюджете",
            data="2025-12-01",
            za=300,
            protiv=50,
            vozhderzhalsya=10,
            ne_golosoval=90,
        )
    ]
    with patch.object(gosduma_tools.client, "poluchit_golosovaniya", return_value=votes):
        rezultat = await gosduma_tools.golosovaniya(sozyv="8")
    assert "О бюджете" in rezultat
    assert "300" in rezultat


async def test_zametka_ob_aut_bez_tokena():
    with patch.object(gosduma_tools.client, "_poluchit_api_token", return_value=""):
        assert "MCP_RUSSIA_DUMA_API_TOKEN" in gosduma_tools._zametka_ob_avtorizatsii()


async def test_zametka_ob_aut_s_tokenom():
    with patch.object(gosduma_tools.client, "_poluchit_api_token", return_value="secret"):
        assert gosduma_tools._zametka_ob_avtorizatsii() == ""
