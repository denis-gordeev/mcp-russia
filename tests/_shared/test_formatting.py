"""Тесты вспомогательных функций форматирования."""

from mcp_russia._shared.formatting import (
    format_brl,
    format_number_br,
    format_number_ru,
    format_percent,
    format_rub,
    markdown_table,
    parse_brl_number,
    parse_rub_number,
    truncate_list,
)


class TestMarkdownTable:
    def test_basic_table(self) -> None:
        result = markdown_table(["Имя", "Регион"], [["Москва", "ЦФО"], ["Казань", "ПФО"]])
        assert "| Имя | Регион |" in result
        assert "| Москва | ЦФО |" in result
        assert "| --- | --- |" in result

    def test_empty_rows(self) -> None:
        result = markdown_table(["A"], [])
        assert result == "Результаты не найдены."

    def test_single_column(self) -> None:
        result = markdown_table(["Субъект"], [["Москва"], ["Татарстан"]])
        assert "| Субъект |" in result


class TestFormatRub:
    def test_simple_value(self) -> None:
        assert format_rub(1234.56) == "1 234,56 ₽"

    def test_zero(self) -> None:
        assert format_rub(0) == "0,00 ₽"

    def test_millions(self) -> None:
        assert format_rub(1_500_000.99) == "1 500 000,99 ₽"

    def test_negative(self) -> None:
        assert format_rub(-42.5) == "-42,50 ₽"


class TestFormatBrlDeprecated:
    def test_is_alias_for_format_rub(self) -> None:
        assert format_brl(1234.56) == format_rub(1234.56)
        assert format_brl(0) == format_rub(0)
        assert format_brl(1_500_000.99) == format_rub(1_500_000.99)
        assert format_brl(-42.5) == format_rub(-42.5)


class TestFormatNumberRu:
    def test_default_decimals(self) -> None:
        assert format_number_ru(1234.5) == "1 234,50"

    def test_zero_decimals(self) -> None:
        assert format_number_ru(1234.5, decimals=0) == "1 234"

    def test_four_decimals(self) -> None:
        assert format_number_ru(3.14159, decimals=4) == "3,1416"

    def test_large_number(self) -> None:
        assert format_number_ru(1_234_567.89) == "1 234 567,89"


class TestFormatNumberBrDeprecated:
    def test_is_alias_for_format_number_ru(self) -> None:
        assert format_number_br(1234.5) == format_number_ru(1234.5)
        assert format_number_br(1234.5, decimals=0) == format_number_ru(1234.5, decimals=0)


class TestFormatPercent:
    def test_basic(self) -> None:
        assert format_percent(0.05) == "5,00%"

    def test_zero(self) -> None:
        assert format_percent(0) == "0,00%"

    def test_custom_decimals(self) -> None:
        assert format_percent(0.1234, decimals=1) == "12,3%"


class TestTruncateList:
    def test_short_list(self) -> None:
        items = ["a", "b", "c"]
        result = truncate_list(items, max_items=5)
        assert result == "a\nb\nc"

    def test_exact_limit(self) -> None:
        items = ["a", "b"]
        result = truncate_list(items, max_items=2)
        assert result == "a\nb"

    def test_truncated(self) -> None:
        items = [f"элемент {i}" for i in range(10)]
        result = truncate_list(items, max_items=3)
        assert "элемент 0" in result
        assert "элемент 2" in result
        assert "... и ещё 7 результатов." in result


class TestParseRubNumber:
    def test_none(self) -> None:
        assert parse_rub_number(None) is None

    def test_int(self) -> None:
        assert parse_rub_number(42) == 42.0

    def test_float(self) -> None:
        assert parse_rub_number(3.14) == 3.14

    def test_simple_string(self) -> None:
        assert parse_rub_number("0,00") == 0.0

    def test_space_thousands(self) -> None:
        assert parse_rub_number("348 600,00") == 348600.0

    def test_dot_thousands(self) -> None:
        assert parse_rub_number("348.600,00") == 348600.0

    def test_millions_dot(self) -> None:
        assert parse_rub_number("1.234.567,89") == 1234567.89

    def test_english_format(self) -> None:
        assert parse_rub_number("123.45") == 123.45

    def test_invalid_string(self) -> None:
        assert parse_rub_number("abc") is None

    def test_non_string_non_number(self) -> None:
        assert parse_rub_number([]) is None


class TestParseBrlNumberDeprecated:
    def test_is_alias_for_parse_rub_number(self) -> None:
        assert parse_brl_number(None) is None
        assert parse_brl_number(42) == 42.0
        assert parse_brl_number("348.600,00") == 348600.0
        assert parse_brl_number("348 600,00") == 348600.0
        assert parse_brl_number("abc") is None
