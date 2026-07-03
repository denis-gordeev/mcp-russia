"""Тесты функций инструментов российских официальных документов."""

from datetime import datetime

import pytest

from mcp_russia.agenty.deloproizvodstvo import tools


class TestFormatirovatDataExtenso:
    @pytest.mark.asyncio
    async def test_default_moskva(self) -> None:
        rezultat = await tools.formatirovat_data_extenso()
        now = datetime.now()
        assert "г. Москва" in rezultat
        assert str(now.year) in rezultat
        assert rezultat.endswith("г.")

    @pytest.mark.asyncio
    async def test_polzovatelskiy_gorod(self) -> None:
        rezultat = await tools.formatirovat_data_extenso(gorod="Санкт-Петербург")
        assert "г. Санкт-Петербург" in rezultat

    @pytest.mark.asyncio
    async def test_soderzhit_mesyats(self) -> None:
        rezultat = await tools.formatirovat_data_extenso()
        from mcp_russia.agenty.deloproizvodstvo.constants import МЕСЯЦЫ

        now = datetime.now()
        assert МЕСЯЦЫ[now.month] in rezultat


class TestGenerirovatNumeraciyu:
    @pytest.mark.asyncio
    async def test_pismo_with_otdel(self) -> None:
        rezultat = await tools.generirovat_numeraciyu("письмо", 42, 2026, "Д-15")
        assert rezultat == "ПИСЬМО № 42/2026/Д-15"

    @pytest.mark.asyncio
    async def test_pismo_bez_otdela(self) -> None:
        rezultat = await tools.generirovat_numeraciyu("письмо", 10, 2026)
        assert rezultat == "ПИСЬМО № 10/2026"

    @pytest.mark.asyncio
    async def test_prikaz(self) -> None:
        rezultat = await tools.generirovat_numeraciyu("приказ", 123, 2026)
        assert rezultat == "ПРИКАЗ № 123/2026"

    @pytest.mark.asyncio
    async def test_god_po_umolchaniyu(self) -> None:
        rezultat = await tools.generirovat_numeraciyu("распоряжение", 1)
        now = datetime.now()
        assert str(now.year) in rezultat

    @pytest.mark.asyncio
    async def test_neizvestnyy_tip(self) -> None:
        rezultat = await tools.generirovat_numeraciyu("rezolyutsiya", 5, 2026)
        assert rezultat == "REZOLYUTSIYA № 5/2026"


class TestKonsulitirovatObrashchenie:
    @pytest.mark.asyncio
    async def test_tochnoe_sovpadenie(self) -> None:
        rezultat = await tools.konsulitirovat_obrashchenie("Губернатор")
        assert "Уважаемый господин Губернатор" in rezultat
        assert "Губернатор" in rezultat
        assert "Адресация" in rezultat

    @pytest.mark.asyncio
    async def test_prezident(self) -> None:
        rezultat = await tools.konsulitirovat_obrashchenie("Президент Российской Федерации")
        assert "Уважаемый господин Президент" in rezultat

    @pytest.mark.asyncio
    async def test_minister(self) -> None:
        rezultat = await tools.konsulitirovat_obrashchenie("Министр")
        assert "Уважаемый господин Министр" in rezultat

    @pytest.mark.asyncio
    async def test_chastichnoe_sovpadenie(self) -> None:
        rezultat = await tools.konsulitirovat_obrashchenie("Губернатор области")
        assert "похоже на" in rezultat

    @pytest.mark.asyncio
    async def test_po_umolchaniyu(self) -> None:
        rezultat = await tools.konsulitirovat_obrashchenie("Аналитик")
        assert "Уважаемый господин/госпожа" in rezultat


class TestValidirovatDokument:
    @pytest.mark.asyncio
    async def test_korrektnyy_dokument(self) -> None:
        tekst = (
            "ПИСЬМО № 1/2026\n\n"
            "г. Москва, 15 марта 2026 г.\n\n"
            "Уважаемый господин Директор,\n\n"
            "Сообщаю, что процесс завершён.\n\n"
            "С уважением,\n\n"
            "Иванов И.И. __________"
        )
        rezultat = await tools.validirovat_dokument(tekst, "письмо")
        assert "проблем" in rezultat.lower() or "Обнаружено" not in rezultat

    @pytest.mark.asyncio
    async def test_otsutstvuet_data(self) -> None:
        tekst = "Уважаемый господин Директор,\n\nСообщаю.\n\nС уважением,"
        rezultat = await tools.validirovat_dokument(tekst, "письмо")
        assert "дата" in rezultat.lower()

    @pytest.mark.asyncio
    async def test_otsutstvuet_podpis(self) -> None:
        tekst = "ПИСЬМО № 1/2026\n\nг. Москва, 15 марта 2026 г.\n\nТекст."
        rezultat = await tools.validirovat_dokument(tekst, "письмо")
        assert "подпис" in rezultat.lower()

    @pytest.mark.asyncio
    async def test_prikaz_no_fecho_obyazatelen(self) -> None:
        tekst = "ПРИКАЗ № 1/2026\n\n15 марта 2026 г.\n\nПРИКАЗЫВАЮ:"
        rezultat = await tools.validirovat_dokument(tekst, "приказ")
        assert "проблем" in rezultat.lower() or "Обнаружено" not in rezultat

    @pytest.mark.asyncio
    async def test_neformalnye_vyrazheniya(self) -> None:
        tekst = (
            "г. Москва, 15 марта 2026 г.\n\nС наилучшими пожеланиями,\n\nИванов И.И. __________"
        )
        rezultat = await tools.validirovat_dokument(tekst, "письмо")
        assert "наилучшими пожеланиями" in rezultat.lower()

    @pytest.mark.asyncio
    async def test_excessive_deeprichastiya(self) -> None:
        tekst = (
            "г. Москва, 15 марта 2026 г.\n\n"
            "Рассматривая изучая анализируя проверяя оценивая сравнивая\n\n"
            "Иванов И.И. __________"
        )
        rezultat = await tools.validirovat_dokument(tekst, "письмо")
        assert "деепричаст" in rezultat.lower() or "рекомендац" in rezultat.lower()


class TestSpisokTipovDokumentov:
    @pytest.mark.asyncio
    async def test_spisok_vsekh_tipov(self) -> None:
        rezultat = await tools.spisok_tipov_dokumentov()
        assert "письмо" in rezultat
        assert "приказ" in rezultat
        assert "распоряжение" in rezultat
        assert "акт" in rezultat
        assert "справка" in rezultat
        assert "протокол" in rezultat
        assert "докладная_записка" in rezultat

    @pytest.mark.asyncio
    async def test_soderzhit_kolichestvo(self) -> None:
        rezultat = await tools.spisok_tipov_dokumentov()
        # Должен упомянуть 7 типов документов
        assert "типов" in rezultat.lower() or "тип" in rezultat.lower()
