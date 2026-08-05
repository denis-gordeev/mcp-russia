"""Проверки нормализации и разбора клиента Картотеки арбитражных дел."""

from mcp_russia.data.kad_arbitrazh import client


class TestRazborRezultatovPoiskaNull:
    def test_null_status(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "Status": None,
                "Judge": "Иванов И.И.",
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert len(rezultaty) == 1
        assert rezultaty[0].sostoyanie == ""

    def test_null_sudya(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "Status": "Рассмотрение",
                "Judge": None,
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].sudya == ""

    def test_null_claim_sum(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "ClaimSum": None,
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].summa_iska == 0.0

    def test_nulevaya_claim_sum(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "ClaimSum": 0,
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].summa_iska == 0.0

    def test_nechislovaya_claim_sum(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "ClaimSum": "не указана",
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].summa_iska == 0.0

    def test_strokovaya_claim_sum(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "ClaimSum": "5000000.00",
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].summa_iska == 5000000.0

    def test_null_istorcy(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "Plaintiffs": None,
                "Defendants": None,
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert rezultaty[0].istorcy == []
        assert rezultaty[0].otvetchiki == []

    def test_chislovye_istorcy(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "Plaintiffs": [1, 2],
                "Defendants": "ООО Бета",
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert "1" in rezultaty[0].istorcy
        assert "ООО Бета" in rezultaty[0].otvetchiki

    def test_pustye_stroki_v_istorczakh(self) -> None:
        dannye = [
            {
                "CaseNumber": "А40-12345/2024",
                "Plaintiffs": "ООО Альфа,,  ООО Бета",
            }
        ]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert "ООО Альфа" in rezultaty[0].istorcy
        assert "ООО Бета" in rezultaty[0].istorcy
        assert len(rezultaty[0].istorcy) == 2

    def test_net_dict_v_spiske(self) -> None:
        dannye = ["ne_dict", {"CaseNumber": "А40-1/2024"}]
        rezultaty = client._razobrat_rezultaty_poiska(dannye)
        assert len(rezultaty) == 1


class TestRazborKartochkiDelaNull:
    def test_null_nomer(self) -> None:
        dannye = {
            "CaseInfo": {
                "CaseNumber": None,
            }
        }
        rezultat = client._razobrat_kartochka_dela(dannye)
        assert rezultat is None

    def test_null_status_i_sudya(self) -> None:
        dannye = {
            "CaseInfo": {
                "CaseNumber": "А40-12345/2024",
                "Status": None,
                "Judge": None,
            }
        }
        rezultat = client._razobrat_kartochka_dela(dannye)
        assert rezultat is not None
        assert rezultat.sostoyanie == ""
        assert rezultat.sudya == ""

    def test_case_info_ne_dict(self) -> None:
        dannye = {"CaseInfo": "ne_dict"}
        rezultat = client._razobrat_kartochka_dela(dannye)
        assert rezultat is None


class TestRazborAktovNull:
    def test_null_polya_dokumenta(self) -> None:
        dannye = {
            "Documents": [
                {
                    "Document": {
                        "Id": 12345,
                        "DocumentType": None,
                        "CourtName": None,
                        "Judge": None,
                    }
                }
            ]
        }
        rezultaty = client._razobrat_akty(dannye, "А40-12345/2024")
        assert len(rezultaty) == 1
        assert rezultaty[0].tip_akta == ""
        assert rezultaty[0].sud == ""
        assert rezultaty[0].sudya == ""

    def test_ploskaya_struktura_bez_document(self) -> None:
        dannye = {
            "Documents": [
                {
                    "Id": 12345,
                    "DocumentType": "Решение",
                    "DocumentDate": "2025-01-01",
                }
            ]
        }
        rezultaty = client._razobrat_akty(dannye, "А40-1/2024")
        assert len(rezultaty) == 1
        assert rezultaty[0].tip_akta == "Решение"

    def test_chislovoy_id(self) -> None:
        dannye = [
            {
                "Document": {
                    "Id": 99999,
                    "DocumentType": "Определение",
                }
            }
        ]
        rezultaty = client._razobrat_akty(dannye, "А40-1/2024")
        assert rezultaty[0].identifikator == "99999"


class TestRazborStoronNull:
    def test_istorcz_s_inn(self) -> None:
        dannye = {
            "Plaintiffs": ["ООО Альфа ИНН 7700000001"],
            "Defendants": ["ООО Бета"],
        }
        rezultaty = client._razobrat_storony(dannye, "А40-12345/2024")
        assert len(rezultaty) == 2
        istorcy = [s for s in rezultaty if s.tip == "истец"]
        assert len(istorcy) == 1
        assert istorcy[0].inn == "7700000001"
        assert istorcy[0].nazvanie == "ООО Альфа"

    def test_dannye_ne_dict(self) -> None:
        assert client._razobrat_storony(None, "А40-1/2024") == []
        assert client._razobrat_storony("stroka", "А40-1/2024") == []

    def test_pustye_storony(self) -> None:
        dannye = {
            "Plaintiffs": [],
            "Defendants": "",
        }
        rezultaty = client._razobrat_storony(dannye, "А40-1/2024")
        assert rezultaty == []


class TestOpredelitSud:
    def test_nomer_bez_tire(self) -> None:
        rezultat = client._opredelit_sud_po_nomeru("А4012345/2024")
        assert isinstance(rezultat, str)

    def test_pustoy_nomer(self) -> None:
        assert client._opredelit_sud_po_nomeru("") == ""
