"""Тесты ReyestrFunktsiy и MetaFunktsii."""

import os
from unittest.mock import patch

import pytest
from fastmcp import Client, FastMCP

from mcp_russia._shared.feature import MetaFunktsii, ReyestrFunktsiy, ZaregistrirovannayaFunktsiya

# ---------------------------------------------------------------------------
# MetaFunktsii (метаданные модуля)
# ---------------------------------------------------------------------------


class TestMetaFunktsii:
    def test_sozdat_minimalnyy(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ API")
        assert metadannye_ekz.imya == "cbrf"
        assert metadannye_ekz.opisanie == "ЦБ РФ API"
        assert metadannye_ekz.versiya == "0.1.0"
        assert metadannye_ekz.vklyuchena is True
        assert metadannye_ekz.trebuet_autentifikatsii is False

    def test_sozdat_s_autentifikatsiey(self) -> None:
        metadannye_ekz = MetaFunktsii(
            imya="zakupki",
            opisanie="ЕИС Закупки",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="ZAKUPKI_API_KEY",
        )
        assert metadannye_ekz.trebuet_autentifikatsii is True
        assert metadannye_ekz.peremennaya_avt_env == "ZAKUPKI_API_KEY"

    def test_dostupna_li_autentifikatsiya_no_auth_obyazatelen(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        assert metadannye_ekz.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_otsutstvuyushchaya_peremennaya(self) -> None:
        metadannye_ekz = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="PROVEROCHNYY_KLYUCH_NE_ZADAN",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PROVEROCHNYY_KLYUCH_NE_ZADAN", None)
            assert metadannye_ekz.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_s_peremennoy_okruzheniya(self) -> None:
        metadannye_ekz = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="PROVEROCHNYY_KLYUCH_MCP",
        )
        with patch.dict(os.environ, {"PROVEROCHNYY_KLYUCH_MCP": "taynyy_klyuch"}):
            assert metadannye_ekz.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_trebuet_aut_bez_peremennoy(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="t", opisanie="T", trebuet_autentifikatsii=True)
        assert metadannye_ekz.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_neobyazatelnaya_bez_peremennoy(self) -> None:
        metadannye_ekz = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=False,
            peremennaya_avt_env="PROVEROCHNYY_KLYUCH_NE_ZADAN",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PROVEROCHNYY_KLYUCH_NE_ZADAN", None)
            assert metadannye_ekz.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_neobyazatelnaya_s_peremennoy(self) -> None:
        metadannye_ekz = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=False,
            peremennaya_avt_env="PROVEROCHNYY_KLYUCH_NE_OBYAZ",
        )
        with patch.dict(os.environ, {"PROVEROCHNYY_KLYUCH_NE_OBYAZ": "znachenie"}):
            assert metadannye_ekz.dostupna_li_autentifikatsiya() is True

    def test_zamorozhennyy(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        with pytest.raises(AttributeError):
            metadannye_ekz.imya = "drugoy"  # type: ignore[misc]

    def test_tegi_po_umolchaniyu_pustye(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        assert metadannye_ekz.tegi == []

    def test_tegi_polzovatelskie(self) -> None:
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ", tegi=["валюта", "курсы"])
        assert metadannye_ekz.tegi == ["валюта", "курсы"]


# ---------------------------------------------------------------------------
# ReyestrFunktsiy (реестр модулей)
# ---------------------------------------------------------------------------


class TestReyestrFunktsiy:
    def test_pustoy_reestr(self) -> None:
        reyestr = ReyestrFunktsiy()
        assert reyestr.funktsii == {}
        assert reyestr.propushcheno == {}

    def test_obnaruzhenie_vozvrashchaet_self_dlya_tsepochki(self) -> None:
        """obnaruzhit() возвращает self для цепочки вызовов."""
        reyestr = ReyestrFunktsiy()
        rezultat = reyestr.obnaruzhit("mcp_russia.data")
        assert rezultat is reyestr

    def test_obnaruzhenie_nakhodit_cbrf(self) -> None:
        """Обнаружение находит функцию cbrf в пакете data."""
        reyestr = ReyestrFunktsiy()
        reyestr.obnaruzhit("mcp_russia.data")
        assert "cbrf" in reyestr.funktsii

    def test_obnaruzhenie_nakhodit_deloproizvodstvo(self) -> None:
        """Обнаружение находит функцию deloproizvodstvo в пакете agenty."""
        reyestr = ReyestrFunktsiy()
        reyestr.obnaruzhit("mcp_russia.agenty")
        assert "deloproizvodstvo" in reyestr.funktsii

    def test_svodka_pustoy(self) -> None:
        reyestr = ReyestrFunktsiy()
        svodka_testa = reyestr.svodka()
        assert "0 функция(й) активно" in svodka_testa
        assert "0 пропущено" in svodka_testa

    def test_poluchit_funktsiyu_ne_naydena(self) -> None:
        reyestr = ReyestrFunktsiy()
        assert reyestr.poluchit_funktsiyu("nesushchestvuyushchiy") is None

    def test_smontirovat_vse_pustoy(self) -> None:
        """Монтирование с пустым реестром не вызывает исключение."""
        reyestr = ReyestrFunktsiy()
        koren = FastMCP("koren-proverka")
        reyestr.smontirovat_vse(koren)  # не должен вызывать исключение

    def test_zaregistrirovat_i_smontirovat_vruchnuyu(self) -> None:
        """Регистрирует функцию вручную и монтирует в корень."""
        reyestr = ReyestrFunktsiy()

        metadannye_ekz = MetaFunktsii(imya="test_funktsiya", opisanie="Тестовая функция")
        podserver = FastMCP("podserver-proverka")

        @podserver.tool
        def instrument_proverki_svyazi() -> str:
            """Инструмент проверки связи."""
            return "отклик"

        reyestr._funktsii["test_funktsiya"] = ZaregistrirovannayaFunktsiya(
            metadannye=metadannye_ekz,
            server_funktsiya=podserver,
            put_modulya="lozhnyy.modul",
        )

        koren = FastMCP("koren-proverka")
        reyestr.smontirovat_vse(koren)

        assert reyestr.poluchit_funktsiyu("test_funktsiya") is not None
        assert "test_funktsiya" in reyestr.svodka()

    def test_svodka_s_funktsiyami(self) -> None:
        reyestr = ReyestrFunktsiy()
        metadannye_ekz = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ данные")
        podmodul = FastMCP("podmodul")
        reyestr._funktsii["cbrf"] = ZaregistrirovannayaFunktsiya(
            metadannye=metadannye_ekz, server_funktsiya=podmodul, put_modulya="m"
        )
        svodka_testa = reyestr.svodka()
        assert "1 функция(й) активно" in svodka_testa
        assert "cbrf" in svodka_testa
        assert "ЦБ РФ данные" in svodka_testa

    def test_svodka_s_propushchennymi(self) -> None:
        reyestr = ReyestrFunktsiy()
        reyestr._propushcheno["slomannyy"] = "отсутствует META_FUNKTSII"
        svodka_testa = reyestr.svodka()
        assert "1 пропущено" in svodka_testa
        assert "slomannyy" in svodka_testa

    def test_propushcheno_vozvrashchaet_kopiyu(self) -> None:
        reyestr = ReyestrFunktsiy()
        reyestr._propushcheno["x"] = "prichina"
        propushcheno = reyestr.propushcheno
        propushcheno["y"] = "drugoy"
        assert "y" not in reyestr._propushcheno

    def test_funktsii_vozvrashchaet_kopiyu(self) -> None:
        reyestr = ReyestrFunktsiy()
        funktsii = reyestr.funktsii
        funktsii["poddelnyy"] = None  # type: ignore[assignment]
        assert "poddelnyy" not in reyestr._funktsii


# ---------------------------------------------------------------------------
# Интеграция: монтирование и вызов через fastmcp.Client
# ---------------------------------------------------------------------------


class TestIntegratsiyaReestra:
    @pytest.mark.asyncio
    async def test_smontirovannyy_instrument_vyzyvaemyy(self) -> None:
        """Инструмент, подключённый через реестр, вызывается через Client."""
        podmodul = FastMCP("podmodul")

        @podmodul.tool
        def ekho(soobshcheniye: str) -> str:
            """Вернуть сообщение."""
            return f"эхо: {soobshcheniye}"

        koren = FastMCP("koren")
        koren.mount(podmodul, namespace="proverka")

        async with Client(koren) as klient:
            rezultat = await klient.call_tool("proverka_ekho", {"soobshcheniye": "privet"})
            assert rezultat.data == "эхо: privet"

    @pytest.mark.asyncio
    async def test_kornevoy_server_zapuskaetsya_pustym(self) -> None:
        """Корневой сервер без подключённых функций работает."""
        from mcp_russia.server import mcp

        async with Client(mcp) as klient:
            instrumenty = await klient.list_tools()
            imena_instrumentov = [t.name for t in instrumenty]
            assert "spisok_funktsiy" in imena_instrumentov

    @pytest.mark.asyncio
    async def test_spisok_funktsiy_instrument(self) -> None:
        """Мета-инструмент spisok_funktsiy возвращает сводку."""
        from mcp_russia.server import mcp

        async with Client(mcp) as klient:
            rezultat = await klient.call_tool("spisok_funktsiy", {})
            assert "mcp-russia" in rezultat.data
