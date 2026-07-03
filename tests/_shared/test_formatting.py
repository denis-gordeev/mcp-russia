"""Тесты вспомогательных функций форматирования."""

from mcp_russia._shared.formatting import (
    formatirovat_chislo_ru,
    formatirovat_protsent,
    formatirovat_rubli,
    razobrat_rublevoe_chislo,
    tablitsa_v_markdown,
    usech_spisok,
)


class TestTablitsaVMarkdown:
    def test_bazovaya_tablitsa(self) -> None:
        result = tablitsa_v_markdown(["Имя", "Регион"], [["Москва", "ЦФО"], ["Казань", "ПФО"]])
        assert "| Имя | Регион |" in result
        assert "| Москва | ЦФО |" in result
        assert "| --- | --- |" in result

    def test_pustye_stroki(self) -> None:
        result = tablitsa_v_markdown(["A"], [])
        assert result == "Результаты не найдены."

    def test_odna_kolonka(self) -> None:
        result = tablitsa_v_markdown(["Субъект"], [["Москва"], ["Татарстан"]])
        assert "| Субъект |" in result


class TestFormatirovatRubli:
    def test_prostoe_znachenie(self) -> None:
        assert formatirovat_rubli(1234.56) == "1 234,56 ₽"

    def test_nol(self) -> None:
        assert formatirovat_rubli(0) == "0,00 ₽"

    def test_milliony(self) -> None:
        assert formatirovat_rubli(1_500_000.99) == "1 500 000,99 ₽"

    def test_otritsatelnoe(self) -> None:
        assert formatirovat_rubli(-42.5) == "-42,50 ₽"

    def test_okruglenie_granichnyy_sluchay(self) -> None:
        assert formatirovat_rubli(1.995) == "2,00 ₽"

    def test_okruglenie_okolo_tselogo(self) -> None:
        assert formatirovat_rubli(0.999) == "1,00 ₽"


class TestFormatirovatChisloRu:
    def test_desyatye_po_umolchaniyu(self) -> None:
        assert formatirovat_chislo_ru(1234.5) == "1 234,50"

    def test_nol_desyatykh(self) -> None:
        assert formatirovat_chislo_ru(1234.5, desyatichnykh=0) == "1 234"

    def test_chetyre_desyatykh(self) -> None:
        assert formatirovat_chislo_ru(3.14159, desyatichnykh=4) == "3,1416"

    def test_bolshoe_chislo(self) -> None:
        assert formatirovat_chislo_ru(1_234_567.89) == "1 234 567,89"


class TestFormatirovatProtsent:
    def test_bazovyy(self) -> None:
        assert formatirovat_protsent(0.05) == "5,00%"

    def test_nol(self) -> None:
        assert formatirovat_protsent(0) == "0,00%"

    def test_svoi_desyatye(self) -> None:
        assert formatirovat_protsent(0.1234, desyatichnykh=1) == "12,3%"


class TestUsechSpisok:
    def test_korotkiy_spisok(self) -> None:
        items = ["a", "b", "c"]
        result = usech_spisok(items, maks_elementov=5)
        assert result == "a\nb\nc"

    def test_tochnyy_limit(self) -> None:
        items = ["a", "b"]
        result = usech_spisok(items, maks_elementov=2)
        assert result == "a\nb"

    def test_usechyonnyy(self) -> None:
        items = [f"элемент {i}" for i in range(10)]
        result = usech_spisok(items, maks_elementov=3)
        assert "элемент 0" in result
        assert "элемент 2" in result
        assert "... и ещё 7 результатов." in result


class TestRazobratRublevoeChislo:
    def test_nichego(self) -> None:
        assert razobrat_rublevoe_chislo(None) is None

    def test_tseloe(self) -> None:
        assert razobrat_rublevoe_chislo(42) == 42.0

    def test_veshchestvennoe(self) -> None:
        assert razobrat_rublevoe_chislo(3.14) == 3.14

    def test_prostaya_stroka(self) -> None:
        assert razobrat_rublevoe_chislo("0,00") == 0.0

    def test_razdelitel_probely(self) -> None:
        assert razobrat_rublevoe_chislo("348 600,00") == 348600.0

    def test_razdelitel_tochka(self) -> None:
        assert razobrat_rublevoe_chislo("348.600,00") == 348600.0

    def test_milliony_tochka(self) -> None:
        assert razobrat_rublevoe_chislo("1.234.567,89") == 1234567.89

    def test_angliyskiy_formatirovanie(self) -> None:
        assert razobrat_rublevoe_chislo("123.45") == 123.45

    def test_nekorrektnaya_stroka(self) -> None:
        assert razobrat_rublevoe_chislo("abc") is None

    def test_ne_stroka_i_ne_chislo(self) -> None:
        assert razobrat_rublevoe_chislo([]) is None
