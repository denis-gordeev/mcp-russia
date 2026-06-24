"""Тесты вспомогательных функций форматирования."""

from mcp_russia._shared.formatting import (
    formatirovat_chislo_ru,
    formatirovat_protsent,
    formatirovat_rubli,
    razobrat_rublevoe_chislo,
    tablitsa_v_markdown,
    usech_spisok,
)


class TestMarkdownTable:
    def test_basic_table(self) -> None:
        result = tablitsa_v_markdown(["Имя", "Регион"], [["Москва", "ЦФО"], ["Казань", "ПФО"]])
        assert "| Имя | Регион |" in result
        assert "| Москва | ЦФО |" in result
        assert "| --- | --- |" in result

    def test_empty_rows(self) -> None:
        result = tablitsa_v_markdown(["A"], [])
        assert result == "Результаты не найдены."

    def test_single_column(self) -> None:
        result = tablitsa_v_markdown(["Субъект"], [["Москва"], ["Татарстан"]])
        assert "| Субъект |" in result


class TestFormatRub:
    def test_simple_value(self) -> None:
        assert formatirovat_rubli(1234.56) == "1 234,56 ₽"

    def test_zero(self) -> None:
        assert formatirovat_rubli(0) == "0,00 ₽"

    def test_millions(self) -> None:
        assert formatirovat_rubli(1_500_000.99) == "1 500 000,99 ₽"

    def test_negative(self) -> None:
        assert formatirovat_rubli(-42.5) == "-42,50 ₽"

    def test_rounding_edge_case(self) -> None:
        assert formatirovat_rubli(1.995) == "2,00 ₽"

    def test_rounding_near_integer(self) -> None:
        assert formatirovat_rubli(0.999) == "1,00 ₽"


class TestFormatNumberRu:
    def test_default_decimals(self) -> None:
        assert formatirovat_chislo_ru(1234.5) == "1 234,50"

    def test_zero_decimals(self) -> None:
        assert formatirovat_chislo_ru(1234.5, decimals=0) == "1 234"

    def test_four_decimals(self) -> None:
        assert formatirovat_chislo_ru(3.14159, decimals=4) == "3,1416"

    def test_large_number(self) -> None:
        assert formatirovat_chislo_ru(1_234_567.89) == "1 234 567,89"


class TestFormatPercent:
    def test_basic(self) -> None:
        assert formatirovat_protsent(0.05) == "5,00%"

    def test_zero(self) -> None:
        assert formatirovat_protsent(0) == "0,00%"

    def test_custom_decimals(self) -> None:
        assert formatirovat_protsent(0.1234, decimals=1) == "12,3%"


class TestTruncateList:
    def test_short_list(self) -> None:
        items = ["a", "b", "c"]
        result = usech_spisok(items, max_items=5)
        assert result == "a\nb\nc"

    def test_exact_limit(self) -> None:
        items = ["a", "b"]
        result = usech_spisok(items, max_items=2)
        assert result == "a\nb"

    def test_truncated(self) -> None:
        items = [f"элемент {i}" for i in range(10)]
        result = usech_spisok(items, max_items=3)
        assert "элемент 0" in result
        assert "элемент 2" in result
        assert "... и ещё 7 результатов." in result


class TestParseRubNumber:
    def test_none(self) -> None:
        assert razobrat_rublevoe_chislo(None) is None

    def test_int(self) -> None:
        assert razobrat_rublevoe_chislo(42) == 42.0

    def test_float(self) -> None:
        assert razobrat_rublevoe_chislo(3.14) == 3.14

    def test_simple_string(self) -> None:
        assert razobrat_rublevoe_chislo("0,00") == 0.0

    def test_space_thousands(self) -> None:
        assert razobrat_rublevoe_chislo("348 600,00") == 348600.0

    def test_dot_thousands(self) -> None:
        assert razobrat_rublevoe_chislo("348.600,00") == 348600.0

    def test_millions_dot(self) -> None:
        assert razobrat_rublevoe_chislo("1.234.567,89") == 1234567.89

    def test_english_format(self) -> None:
        assert razobrat_rublevoe_chislo("123.45") == 123.45

    def test_invalid_string(self) -> None:
        assert razobrat_rublevoe_chislo("abc") is None

    def test_non_string_non_number(self) -> None:
        assert razobrat_rublevoe_chislo([]) is None
