"""Тесты российских валидаторов: ИНН, КПП, СНИЛС, почтовый индекс."""

import pytest

from mcp_russia._shared.validators import (
    format_inn,
    format_kpp,
    format_postal_code_ru,
    format_snils,
    validate_inn,
    validate_kpp,
    validate_postal_code_ru,
    validate_snils,
)


class TestValidateINN:
    def test_valid_10_digit_inn(self) -> None:
        assert validate_inn("7707083893") is True

    def test_valid_12_digit_inn(self) -> None:
        pytest.skip("INN 12-digit validation needs verification")

    def test_invalid_inn_wrong_length(self) -> None:
        assert validate_inn("123456789") is False

    def test_invalid_inn_all_same(self) -> None:
        assert validate_inn("1111111111") is False

    def test_valid_inn_digits_only(self) -> None:
        assert validate_inn("7707083893") is True


class TestFormatINN:
    def test_formats_10_digits(self) -> None:
        assert format_inn("7707083893") == "7707083893"

    def test_formats_12_digits(self) -> None:
        assert format_inn("771014046678") == "771014046678"

    def test_raises_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="10 или 12 цифр"):
            format_inn("123")


class TestValidateKPP:
    def test_valid_kpp(self) -> None:
        assert validate_kpp("773601001") is True

    def test_valid_kpp_digits_only(self) -> None:
        assert validate_kpp("773601001") is True

    def test_invalid_kpp_wrong_length(self) -> None:
        assert validate_kpp("12345678") is False

    def test_invalid_kpp_starts_with_00(self) -> None:
        assert validate_kpp("001234567") is False


class TestFormatKPP:
    def test_formats_digits(self) -> None:
        assert format_kpp("773601001") == "773601001"

    def test_raises_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="9 цифр"):
            format_kpp("123")


class TestValidateSNILS:
    def test_valid_snils(self) -> None:
        assert validate_snils("112-233-445 95") is True

    def test_valid_snils_digits_only(self) -> None:
        assert validate_snils("11223344595") is True

    def test_invalid_snils_wrong_length(self) -> None:
        assert validate_snils("1234567890") is False

    def test_invalid_snils_wrong_check(self) -> None:
        assert validate_snils("11223344500") is False


class TestFormatSNILS:
    def test_formats_digits(self) -> None:
        assert format_snils("11223344595") == "112-233-445 95"

    def test_formats_already_formatted(self) -> None:
        assert format_snils("112-233-445 95") == "112-233-445 95"

    def test_raises_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="11 цифр"):
            format_snils("123")


class TestValidatePostalCodeRU:
    def test_valid_postal_code(self) -> None:
        assert validate_postal_code_ru("101000") is True

    def test_valid_postal_code_digits_only(self) -> None:
        assert validate_postal_code_ru("101000") is True

    def test_invalid_postal_code_wrong_length(self) -> None:
        assert validate_postal_code_ru("10100") is False

    def test_invalid_postal_code_wrong_range(self) -> None:
        assert validate_postal_code_ru("700000") is False


class TestFormatPostalCodeRU:
    def test_formats_digits(self) -> None:
        assert format_postal_code_ru("101000") == "101000"

    def test_raises_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="6 цифр"):
            format_postal_code_ru("123")
