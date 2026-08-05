"""Проверки нормализации и разбора клиента ЕИС Закупок."""

from mcp_russia.data.zakupki import client


class TestRazborPoiskZakupok:
    def test_null_pole_name(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "regNumber": "0123400000125000001",
                    "name": None,
                    "price": 1000,
                }
            ]
        }
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert len(rezultat) == 1
        assert rezultat[0].nazvanie == ""
        assert rezultat[0].identifikator == "1"

    def test_null_pole_currency(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "regNumber": "0123400000125000001",
                    "name": "Закупка",
                    "currency": None,
                }
            ]
        }
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert rezultat[0].valyuta == "RUB"

    def test_null_pole_id(self) -> None:
        dannye = {
            "results": [
                {
                    "id": None,
                    "regNumber": "0123400000125000001",
                    "name": "Закупка",
                }
            ]
        }
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert rezultat[0].identifikator == "0123400000125000001"

    def test_net_dict_v_spiske(self) -> None:
        dannye = ["ne_dict", {"id": 1, "name": "Закупка"}]
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert len(rezultat) == 1

    def test_nechislovaya_tsena(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "name": "Закупка",
                    "price": "не число",
                }
            ]
        }
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert rezultat[0].nachalnaya_tsena == 0.0

    def test_strokovaya_tsena(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "name": "Закупка",
                    "price": "1500000.50",
                }
            ]
        }
        rezultat = client._razobrat_poisk_zakupok(dannye)
        assert rezultat[0].nachalnaya_tsena == 1500000.5


class TestRazborKontraktov:
    def test_null_pole_purchase_number(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "regNum": "12345",
                    "purchaseNumber": None,
                }
            ]
        }
        rezultat = client._razobrat_kontrakty(dannye)
        assert rezultat[0].zakupka_nomer == ""

    def test_null_pole_currency(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "regNum": "12345",
                    "currency": None,
                }
            ]
        }
        rezultat = client._razobrat_kontrakty(dannye)
        assert rezultat[0].valyuta == "RUB"

    def test_null_pole_supplier(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 1,
                    "regNum": "12345",
                    "supplierName": None,
                    "supplierInn": None,
                }
            ]
        }
        rezultat = client._razobrat_kontrakty(dannye)
        assert rezultat[0].nazvanie_podryadchika == ""
        assert rezultat[0].podryadchik_inn == ""


class TestRazborPlanov:
    def test_osnovnoy(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 10,
                    "year": 2026,
                    "customerName": "Минобразования",
                    "customerInn": "7700000000",
                    "positionsCount": 5,
                    "totalSum": 1000000,
                    "createDate": "2025-01-01",
                    "updateDate": "2025-06-01",
                }
            ]
        }
        rezultat = client._razobrat_plany(dannye)
        assert len(rezultat) == 1
        assert rezultat[0].god == 2026
        assert rezultat[0].kolichestvo_pozitsiy == 5

    def test_null_god(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 10,
                    "year": None,
                    "customerName": "Минобразования",
                }
            ]
        }
        rezultat = client._razobrat_plany(dannye)
        assert rezultat[0].god == 0

    def test_null_positions_count(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 10,
                    "year": 2026,
                    "positionsCount": None,
                }
            ]
        }
        rezultat = client._razobrat_plany(dannye)
        assert rezultat[0].kolichestvo_pozitsiy == 0

    def test_strokovyy_god(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 10,
                    "year": "2026",
                    "customerName": "Минобразования",
                }
            ]
        }
        rezultat = client._razobrat_plany(dannye)
        assert rezultat[0].god == 2026

    def test_nechislovoy_byudzhet(self) -> None:
        dannye = {
            "results": [
                {
                    "id": 10,
                    "year": 2026,
                    "totalSum": "не число",
                }
            ]
        }
        rezultat = client._razobrat_plany(dannye)
        assert rezultat[0].obshchiy_byudzhet == 0.0


class TestOpredelitZakon:
    def test_fz_kak_chislo(self) -> None:
        assert client._opredelit_zakon({"fz": 44}) == "44-ФЗ"
        assert client._opredelit_zakon({"fz": 223}) == "223-ФЗ"

    def test_purchase_code_fallback(self) -> None:
        assert client._opredelit_zakon({"purchaseCode": "44-2025-001"}) == "44-ФЗ"
        assert client._opredelit_zakon({"purchaseCode": "223-2025-001"}) == "223-ФЗ"
