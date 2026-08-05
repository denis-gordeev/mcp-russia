"""Проверки контракта нормализации: логические, дробные, контейнеры."""

from mcp_russia._shared.normalizatsiya import (
    bezopasnaya_stroka,
    bezopasnoe_chislo,
    bezopasnoe_tseloe,
    izvlech_spisok,
    pervoe_znachenie,
    razorvat_stroku_spisok,
)


class TestBezopasnayaStroka:
    def test_none(self) -> None:
        assert bezopasnaya_stroka(None) == ""

    def test_bool_true(self) -> None:
        assert bezopasnaya_stroka(True) == ""

    def test_bool_false(self) -> None:
        assert bezopasnaya_stroka(False) == ""

    def test_dict(self) -> None:
        assert bezopasnaya_stroka({"a": 1}) == ""

    def test_list(self) -> None:
        assert bezopasnaya_stroka([1, 2]) == ""

    def test_str(self) -> None:
        assert bezopasnaya_stroka("привет") == "привет"

    def test_int(self) -> None:
        assert bezopasnaya_stroka(42) == "42"

    def test_float(self) -> None:
        assert bezopasnaya_stroka(3.14) == "3.14"

    def test_umolchanie(self) -> None:
        assert bezopasnaya_stroka(None, "нет данных") == "нет данных"

    def test_pustaya_stroka(self) -> None:
        assert bezopasnaya_stroka("") == ""


class TestBezopasnoeTseloe:
    def test_none(self) -> None:
        assert bezopasnoe_tseloe(None) == 0

    def test_bool_true(self) -> None:
        assert bezopasnoe_tseloe(True) == 0

    def test_bool_false(self) -> None:
        assert bezopasnoe_tseloe(False) == 0

    def test_int(self) -> None:
        assert bezopasnoe_tseloe(42) == 42

    def test_float_tseloe(self) -> None:
        assert bezopasnoe_tseloe(3.0) == 3

    def test_float_drobnoe(self) -> None:
        assert bezopasnoe_tseloe(3.14) == 0

    def test_stroka_chislo(self) -> None:
        assert bezopasnoe_tseloe("42") == 42

    def test_stroka_s_probelyami(self) -> None:
        assert bezopasnoe_tseloe("  7  ") == 7

    def test_stroka_ne_chislo(self) -> None:
        assert bezopasnoe_tseloe("abc") == 0

    def test_umolchanie(self) -> None:
        assert bezopasnoe_tseloe(None, -1) == -1


class TestBezopasnoeChislo:
    def test_none(self) -> None:
        assert bezopasnoe_chislo(None) is None

    def test_bool_true(self) -> None:
        assert bezopasnoe_chislo(True) is None

    def test_bool_false(self) -> None:
        assert bezopasnoe_chislo(False) is None

    def test_int(self) -> None:
        assert bezopasnoe_chislo(42) == 42.0

    def test_float(self) -> None:
        assert bezopasnoe_chislo(3.14) == 3.14

    def test_stroka_chislo(self) -> None:
        assert bezopasnoe_chislo("123.5") == 123.5

    def test_stroka_ne_chislo(self) -> None:
        assert bezopasnoe_chislo("нет данных") is None

    def test_umolchanie_nol(self) -> None:
        assert bezopasnoe_chislo(None, po_umolchaniyu=0.0) == 0.0

    def test_umolchanie_none(self) -> None:
        assert bezopasnoe_chislo("abc", po_umolchaniyu=None) is None

    def test_nol_ne_bool(self) -> None:
        assert bezopasnoe_chislo(0) == 0.0

    def test_edinitsa_ne_bool(self) -> None:
        assert bezopasnoe_chislo(1) == 1.0


class TestIzvlechSpisok:
    def test_spisok(self) -> None:
        assert izvlech_spisok([1, 2, 3]) == [1, 2, 3]

    def test_dict_s_data(self) -> None:
        assert izvlech_spisok({"data": [1]}) == [1]

    def test_dict_s_items(self) -> None:
        assert izvlech_spisok({"items": [2]}) == [2]

    def test_dict_s_results(self) -> None:
        assert izvlech_spisok({"results": [3]}) == [3]

    def test_dict_bez_spiska(self) -> None:
        assert izvlech_spisok({"name": "test"}) == []

    def test_stroka(self) -> None:
        assert izvlech_spisok("ne spisok") == []

    def test_none(self) -> None:
        assert izvlech_spisok(None) == []

    def test_klyuchi_poiska(self) -> None:
        assert izvlech_spisok({"Instances": [1]}, "Instances", "Result") == [1]

    def test_klyuchi_poiska_vtoroy(self) -> None:
        assert izvlech_spisok({"Result": [2]}, "Instances", "Result") == [2]


class TestPervoeZnachenie:
    def test_pervyy(self) -> None:
        assert pervoe_znachenie({"a": 1, "b": 2}, "a", "b") == 1

    def test_vtoroy(self) -> None:
        assert pervoe_znachenie({"a": None, "b": 2}, "a", "b") == 2

    def test_vse_none(self) -> None:
        assert pervoe_znachenie({"a": None, "b": None}, "a", "b") is None

    def test_net_klyucha(self) -> None:
        assert pervoe_znachenie({"a": 1}, "b", "c") is None


class TestRazorvatStrokuSpisok:
    def test_stroka_s_zapjatymi(self) -> None:
        assert razorvat_stroku_spisok("а, б, в") == ["а", "б", "в"]

    def test_stroka_s_pustymi(self) -> None:
        assert razorvat_stroku_spisok("а,, б") == ["а", "б"]

    def test_spisok_strok(self) -> None:
        assert razorvat_stroku_spisok(["а", "б"]) == ["а", "б"]

    def test_spisok_smeshannyy(self) -> None:
        assert razorvat_stroku_spisok(["а", 1, None]) == ["а", "1", "None"]

    def test_none(self) -> None:
        assert razorvat_stroku_spisok(None) == []

    def test_chislo(self) -> None:
        assert razorvat_stroku_spisok(42) == []

    def test_pustaya_stroka(self) -> None:
        assert razorvat_stroku_spisok("") == []

    def test_razdelitel(self) -> None:
        assert razorvat_stroku_spisok("а; б; в", razdelitel=";") == ["а", "б", "в"]
