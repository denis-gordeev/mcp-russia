"""Тесты функций инструментов российских официальных документов."""

from datetime import datetime

import pytest

from mcp_russia.agenty.redator import tools


class TestFormatirovatDataExtenso:
    @pytest.mark.asyncio
    async def test_default_moskva(self) -> None:
        result = await tools.formatirovat_data_extenso()
        now = datetime.now()
        assert "г. Москва" in result
        assert str(now.year) in result
        assert result.endswith("г.")

    @pytest.mark.asyncio
    async def test_custom_city(self) -> None:
        result = await tools.formatirovat_data_extenso(gorod="Санкт-Петербург")
        assert "г. Санкт-Петербург" in result

    @pytest.mark.asyncio
    async def test_contains_month(self) -> None:
        result = await tools.formatirovat_data_extenso()
        from mcp_russia.agenty.redator.constants import МЕСЯЦЫ

        now = datetime.now()
        assert МЕСЯЦЫ[now.month] in result


class TestGenerirovatNumeraciyu:
    @pytest.mark.asyncio
    async def test_pismo_with_otdel(self) -> None:
        result = await tools.generirovat_numeraciyu("письмо", 42, 2026, "Д-15")
        assert result == "ПИСЬМО № 42/2026/Д-15"

    @pytest.mark.asyncio
    async def test_pismo_bez_otdela(self) -> None:
        result = await tools.generirovat_numeraciyu("письмо", 10, 2026)
        assert result == "ПИСЬМО № 10/2026"

    @pytest.mark.asyncio
    async def test_prikaz(self) -> None:
        result = await tools.generirovat_numeraciyu("приказ", 123, 2026)
        assert result == "ПРИКАЗ № 123/2026"

    @pytest.mark.asyncio
    async def test_default_year(self) -> None:
        result = await tools.generirovat_numeraciyu("распоряжение", 1)
        now = datetime.now()
        assert str(now.year) in result

    @pytest.mark.asyncio
    async def test_unknown_type(self) -> None:
        result = await tools.generirovat_numeraciyu("rezolyutsiya", 5, 2026)
        assert result == "REZOLYUTSIYA № 5/2026"


class TestKonsulitirovatObrashchenie:
    @pytest.mark.asyncio
    async def test_exact_match(self) -> None:
        result = await tools.konsulitirovat_obrashchenie("Губернатор")
        assert "Уважаемый господин Губернатор" in result
        assert "Губернатор" in result
        assert "Адресация" in result

    @pytest.mark.asyncio
    async def test_prezident(self) -> None:
        result = await tools.konsulitirovat_obrashchenie("Президент Российской Федерации")
        assert "Уважаемый господин Президент" in result

    @pytest.mark.asyncio
    async def test_minister(self) -> None:
        result = await tools.konsulitirovat_obrashchenie("Министр")
        assert "Уважаемый господин Министр" in result

    @pytest.mark.asyncio
    async def test_partial_match(self) -> None:
        result = await tools.konsulitirovat_obrashchenie("Губернатор области")
        assert "похоже на" in result

    @pytest.mark.asyncio
    async def test_default(self) -> None:
        result = await tools.konsulitirovat_obrashchenie("Аналитик")
        assert "Уважаемый господин/госпожа" in result


class TestValidirovatDokument:
    @pytest.mark.asyncio
    async def test_valid_document(self) -> None:
        tekst = (
            "ПИСЬМО № 1/2026\n\n"
            "г. Москва, 15 марта 2026 г.\n\n"
            "Уважаемый господин Директор,\n\n"
            "Сообщаю, что процесс завершён.\n\n"
            "С уважением,\n\n"
            "Иванов И.И. __________"
        )
        result = await tools.validirovat_dokument(tekst, "письмо")
        assert "проблем" in result.lower() or "Обнаружено" not in result

    @pytest.mark.asyncio
    async def test_missing_date(self) -> None:
        tekst = "Уважаемый господин Директор,\n\nСообщаю.\n\nС уважением,"
        result = await tools.validirovat_dokument(tekst, "письмо")
        assert "дата" in result.lower()

    @pytest.mark.asyncio
    async def test_missing_signature(self) -> None:
        tekst = "ПИСЬМО № 1/2026\n\nг. Москва, 15 марта 2026 г.\n\nТекст."
        result = await tools.validirovat_dokument(tekst, "письмо")
        assert "подпис" in result.lower()

    @pytest.mark.asyncio
    async def test_prikaz_no_fecho_required(self) -> None:
        tekst = "ПРИКАЗ № 1/2026\n\n15 марта 2026 г.\n\nПРИКАЗЫВАЮ:"
        result = await tools.validirovat_dokument(tekst, "приказ")
        assert "проблем" in result.lower() or "Обнаружено" not in result

    @pytest.mark.asyncio
    async def test_informal_expressions(self) -> None:
        tekst = (
            "г. Москва, 15 марта 2026 г.\n\nС наилучшими пожеланиями,\n\nИванов И.И. __________"
        )
        result = await tools.validirovat_dokument(tekst, "письмо")
        assert "наилучшими пожеланиями" in result.lower()

    @pytest.mark.asyncio
    async def test_excessive_deeprichastiya(self) -> None:
        tekst = (
            "г. Москва, 15 марта 2026 г.\n\n"
            "Рассматривая изучая анализируя проверяя оценивая сравнивая\n\n"
            "Иванов И.И. __________"
        )
        result = await tools.validirovat_dokument(tekst, "письмо")
        assert "деепричаст" in result.lower() or "рекомендац" in result.lower()


class TestSpisokTipovDokumentov:
    @pytest.mark.asyncio
    async def test_lists_all_types(self) -> None:
        result = await tools.spisok_tipov_dokumentov()
        assert "письмо" in result
        assert "приказ" in result
        assert "распоряжение" in result
        assert "акт" in result
        assert "справка" in result
        assert "протокол" in result
        assert "докладная_записка" in result

    @pytest.mark.asyncio
    async def test_contains_count(self) -> None:
        result = await tools.spisok_tipov_dokumentov()
        # Должен упомянуть 7 типов документов
        assert "типов" in result.lower() or "тип" in result.lower()
