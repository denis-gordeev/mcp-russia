"""Тесты инструментов модуля Картотека арбитражных дел."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.kad_arbitrazh import client as kad_client
from mcp_russia.data.kad_arbitrazh import tools as kad_tools
from mcp_russia.data.kad_arbitrazh.schemas import SudebnoeDelo


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


class TestRazborRezultatovPoiska:
    def test_razbor_spiska(self) -> None:
        dannye = [
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
        rezultaty = kad_client._razobrat_rezultaty_poiska(dannye)
        assert len(rezultaty) == 1
        assert rezultaty[0].nomer == "А40-12345/2024"
        assert rezultaty[0].nazvanie_suda == "АС г. Москвы"
        assert rezultaty[0].summa_iska == 1000000.0
        assert "ООО Альфа" in rezultaty[0].istorcy

    def test_razbor_slovarya_s_ekzemplyarami(self) -> None:
        dannye = {
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
        rezultaty = kad_client._razobrat_rezultaty_poiska(dannye)
        assert len(rezultaty) == 1
        assert rezultaty[0].nomer == "А77-5678/2023"

    def test_razbor_pustogo(self) -> None:
        assert kad_client._razobrat_rezultaty_poiska(None) == []
        assert kad_client._razobrat_rezultaty_poiska([]) == []

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


class TestRazborKartochkiDela:
    def test_razbor_polnyy(self) -> None:
        dannye = {
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
        rezultat = kad_client._razobrat_kartochka_dela(dannye)
        assert rezultat is not None
        assert rezultat.nomer == "А40-11111/2025"
        assert rezultat.kategoriya == "Банкротство"
        assert rezultat.summa_iska == 5000000.0

    def test_razbor_nichego(self) -> None:
        assert kad_client._razobrat_kartochka_dela(None) is None
        assert kad_client._razobrat_kartochka_dela({}) is None


class TestRazborAktov:
    def test_razbor_dokumentov(self) -> None:
        dannye = {
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
        rezultaty = kad_client._razobrat_akty(dannye, "А40-12345/2024")
        assert len(rezultaty) == 1
        assert rezultaty[0].tip_akta == "Решение"
        assert rezultaty[0].delo_nomer == "А40-12345/2024"

    def test_razbor_pustogo(self) -> None:
        assert kad_client._razobrat_akty(None, "А40-1/2024") == []


class TestRazborStoron:
    def test_razbor_storon(self) -> None:
        dannye = {
            "Plaintiffs": ["ООО Альфа", "Иванов И.И."],
            "Defendants": ["ООО Бета", "Минфин РФ"],
        }
        rezultaty = kad_client._razobrat_storony(dannye, "А40-12345/2024")
        assert len(rezultaty) == 4
        istorcy = [s for s in rezultaty if s.tip == "истец"]
        otvetchiki = [s for s in rezultaty if s.tip == "ответчик"]
        assert len(istorcy) == 2
        assert len(otvetchiki) == 2

    def test_razbor_strokovykh_storon(self) -> None:
        dannye = {
            "Plaintiffs": "ООО Альфа, ООО Гамма",
            "Defendants": "ООО Бета",
        }
        rezultaty = kad_client._razobrat_storony(dannye, "А40-12345/2024")
        assert len(rezultaty) == 3


async def test_poisk_del_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(kad_tools.client, "poisk_del", return_value=[]):
        rezultat = await kad_tools.poisk_del(kontekst=kontekst)
    assert "Картотека арбитражных дел" in rezultat
    assert "не найдены" in rezultat


async def test_poisk_del_s_rezultatami():
    kontekst = _maket_konteksta()
    maket_dela = [
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
    with patch.object(kad_tools.client, "poisk_del", return_value=maket_dela):
        rezultat = await kad_tools.poisk_del(nomer="А40-12345/2024", kontekst=kontekst)
    assert "А40-12345/2024" in rezultat
    assert "1 000 000" in rezultat or "1000000" in rezultat or "₽" in rezultat


async def test_poisk_del_s_filtrami():
    kontekst = _maket_konteksta()
    with patch.object(kad_tools.client, "poisk_del", return_value=[]):
        rezultat = await kad_tools.poisk_del(
            nomer="А40-12345/2024", istorcz="ООО Ромашка", kontekst=kontekst
        )
    assert "А40-12345/2024" in rezultat
    assert "Ромашка" in rezultat


async def test_info_dela_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(kad_tools.client, "info_dela", return_value=None):
        rezultat = await kad_tools.info_dela("А40-00000/2024", kontekst)
    assert "не найдено" in rezultat


async def test_info_dela_nayden():
    kontekst = _maket_konteksta()
    maket_delo = SudebnoeDelo(
        nomer="А40-12345/2024",
        kategoriya="Банкротство",
        sostoyanie="На рассмотрении",
        sudya="Иванов И.И.",
        nazvanie_suda="АС г. Москвы",
        data_vozbuzhdeniya="2024-01-15",
        istorcy=["ООО Альфа"],
        otvetchiki=["ООО Бета"],
        summa_iska=500000,
    )
    with patch.object(kad_tools.client, "info_dela", return_value=maket_delo):
        rezultat = await kad_tools.info_dela("А40-12345/2024", kontekst)
    assert "А40-12345/2024" in rezultat
    assert "Банкротство" in rezultat


async def test_akty_po_delu_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(kad_tools.client, "akty_po_delu", return_value=[]):
        rezultat = await kad_tools.akty_po_delu("А40-00000/2024", kontekst)
    assert "не найдены" in rezultat


async def test_storony_dela_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(kad_tools.client, "storony_dela", return_value=[]):
        rezultat = await kad_tools.storony_dela("А40-00000/2024", kontekst)
    assert "не найдены" in rezultat


async def test_spravochnik_kategoriy():
    kontekst = _maket_konteksta()
    rezultat = await kad_tools.spravochnik_kategoriy(kontekst)
    assert "Категории" in rezultat
    assert "Банкротство" in rezultat


async def test_spravochnik_instantsiy():
    kontekst = _maket_konteksta()
    rezultat = await kad_tools.spravochnik_instantsiy(kontekst)
    assert "Инстанции" in rezultat
    assert "первая инстанция" in rezultat


async def test_spravochnik_statusov():
    kontekst = _maket_konteksta()
    rezultat = await kad_tools.spravochnik_statusov(kontekst)
    assert "Статусы" in rezultat
    assert "Новое" in rezultat


async def test_spravochnik_aktov():
    kontekst = _maket_konteksta()
    rezultat = await kad_tools.spravochnik_aktov(kontekst)
    assert "Типы судебных актов" in rezultat
    assert "Решение" in rezultat
