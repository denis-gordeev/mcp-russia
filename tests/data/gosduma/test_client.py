"""Защитные тесты разбора внешних ответов API Госдумы."""

from mcp_russia.data.gosduma import client


def test_deputaty_prinimayut_null_i_zapasnye_polya():
    rezultat = client._razobrat_deputatov(
        {
            "deputies": [
                {
                    "id": "17",
                    "surname": None,
                    "lastName": "Иванов",
                    "name": None,
                    "firstName": "Иван",
                    "patronymic": None,
                    "convocation": 8,
                    "photoUrl": None,
                }
            ]
        }
    )

    assert len(rezultat) == 1
    assert rezultat[0].identifikator == 17
    assert rezultat[0].familiya == "Иванов"
    assert rezultat[0].imya == "Иван"
    assert rezultat[0].otchestvo == ""
    assert rezultat[0].sozyv == "8"
    assert rezultat[0].foto_ssylka == ""


def test_deputaty_ignoriruyut_neozhidannuyu_strukturu():
    assert client._razobrat_deputatov({"deputies": None}) == []
    assert client._razobrat_deputatov({"deputies": {"id": 1}}) == []
    assert client._razobrat_deputatov({"items": [None, "deputat"]}) == []


def test_zakonoproekty_normalizuyut_pustye_i_chislovye_polya():
    rezultat = client._razobrat_zakonoproekty(
        {
            "bills": [
                {
                    "id": 101,
                    "number": None,
                    "name": None,
                    "title": "О тестировании API",
                    "statusName": None,
                    "readingsCount": "2",
                },
                {
                    "id": None,
                    "name": ["неожиданный", "список"],
                    "readingsCount": "не число",
                },
            ]
        }
    )

    assert rezultat[0].identifikator == "101"
    assert rezultat[0].nomer == ""
    assert rezultat[0].nazvanie == "О тестировании API"
    assert rezultat[0].chteniya == 2
    assert rezultat[1].identifikator == ""
    assert rezultat[1].nazvanie == ""
    assert rezultat[1].chteniya == 0


def test_golosovaniya_normalizuyut_null_i_neozhidannye_tipy():
    rezultat = client._razobrat_golosovaniya(
        {
            "votes": [
                {
                    "billId": 42,
                    "subject": None,
                    "title": "По проекту закона",
                    "date": None,
                    "voteDate": "2026-08-02",
                    "totalFor": "300",
                    "totalAgainst": None,
                    "against": 25.0,
                    "totalAbstain": True,
                    "totalNotVoting": {"count": 10},
                }
            ]
        }
    )

    assert len(rezultat) == 1
    assert rezultat[0].zakonoproekt_identifikator == "42"
    assert rezultat[0].nazvanie == "По проекту закона"
    assert rezultat[0].data == "2026-08-02"
    assert rezultat[0].za == 300
    assert rezultat[0].protiv == 25
    assert rezultat[0].vozhderzhalsya == 0
    assert rezultat[0].ne_golosoval == 0
