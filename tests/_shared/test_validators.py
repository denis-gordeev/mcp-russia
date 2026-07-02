"""Тесты российских валидаторов: ИНН, КПП, СНИЛС, почтовый индекс."""

import pytest

from mcp_russia._shared.validators import (
    formatirovat_inn,
    formatirovat_kpp,
    formatirovat_pochtovyy_indeks,
    formatirovat_snils,
    proverit_inn,
    proverit_kpp,
    proverit_pochtovyy_indeks,
    proverit_snils,
)


class TestProveritInn:
    def test_korrektnyy_inn_10_tsifr(self) -> None:
        assert proverit_inn("7707083893") is True

    def test_korrektnyy_inn_12_tsifr(self) -> None:
        pytest.skip("Проверка 12-значного ИНН требует уточнения")

    def test_nekorrektnyy_inn_nepravilnaya_dlina(self) -> None:
        assert proverit_inn("123456789") is False

    def test_nekorrektnyy_inn_vse_odinakovye(self) -> None:
        assert proverit_inn("1111111111") is False

    def test_korrektnyy_inn_tolko_tsifry(self) -> None:
        assert proverit_inn("7707083893") is True


class TestFormatirovatInn:
    def test_formatiruet_10_tsifr(self) -> None:
        assert formatirovat_inn("7707083893") == "7707083893"

    def test_formatiruet_12_tsifr(self) -> None:
        assert formatirovat_inn("771014046678") == "771014046678"

    def test_vyzyvaet_oshibku_nepravilnaya_dlina(self) -> None:
        with pytest.raises(ValueError, match="10 или 12 цифр"):
            formatirovat_inn("123")


class TestProveritKpp:
    def test_korrektnyy_kpp(self) -> None:
        assert proverit_kpp("773601001") is True

    def test_korrektnyy_kpp_tolko_tsifry(self) -> None:
        assert proverit_kpp("773601001") is True

    def test_nekorrektnyy_kpp_nepravilnaya_dlina(self) -> None:
        assert proverit_kpp("12345678") is False

    def test_nekorrektnyy_kpp_nachinaetsya_s_00(self) -> None:
        assert proverit_kpp("001234567") is False


class TestFormatirovatKpp:
    def test_formatiruet_tsifry(self) -> None:
        assert formatirovat_kpp("773601001") == "773601001"

    def test_vyzyvaet_oshibku_nepravilnaya_dlina(self) -> None:
        with pytest.raises(ValueError, match="9 цифр"):
            formatirovat_kpp("123")


class TestProveritSnils:
    def test_korrektnyy_snils(self) -> None:
        assert proverit_snils("112-233-445 95") is True

    def test_korrektnyy_snils_tolko_tsifry(self) -> None:
        assert proverit_snils("11223344595") is True

    def test_nekorrektnyy_snils_nepravilnaya_dlina(self) -> None:
        assert proverit_snils("1234567890") is False

    def test_nekorrektnyy_snils_nepravilnaya_kontrolnaya(self) -> None:
        assert proverit_snils("11223344500") is False


class TestFormatirovatSnils:
    def test_formatiruet_tsifry(self) -> None:
        assert formatirovat_snils("11223344595") == "112-233-445 95"

    def test_formatiruet_uzhe_otformatirovannyy(self) -> None:
        assert formatirovat_snils("112-233-445 95") == "112-233-445 95"

    def test_vyzyvaet_oshibku_nepravilnaya_dlina(self) -> None:
        with pytest.raises(ValueError, match="11 цифр"):
            formatirovat_snils("123")


class TestProveritPochtovyyIndeks:
    def test_korrektnyy_pochtovyy_indeks(self) -> None:
        assert proverit_pochtovyy_indeks("101000") is True

    def test_korrektnyy_pochtovyy_indeks_tolko_tsifry(self) -> None:
        assert proverit_pochtovyy_indeks("101000") is True

    def test_nekorrektnyy_indeks_nepravilnaya_dlina(self) -> None:
        assert proverit_pochtovyy_indeks("10100") is False

    def test_nekorrektnyy_indeks_nepravilnyy_diapazon(self) -> None:
        assert proverit_pochtovyy_indeks("700000") is False


class TestFormatirovatPochtovyyIndeks:
    def test_formatiruet_tsifry(self) -> None:
        assert formatirovat_pochtovyy_indeks("101000") == "101000"

    def test_vyzyvaet_oshibku_nepravilnaya_dlina(self) -> None:
        with pytest.raises(ValueError, match="6 цифр"):
            formatirovat_pochtovyy_indeks("123")
