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
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ API")
        assert meta.imya == "cbrf"
        assert meta.opisanie == "ЦБ РФ API"
        assert meta.versiya == "0.1.0"
        assert meta.vklyuchena is True
        assert meta.trebuet_autentifikatsii is False

    def test_sozdat_s_autentifikatsiey(self) -> None:
        meta = MetaFunktsii(
            imya="zakupki",
            opisanie="ЕИС Закупки",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="ZAKUPKI_API_KEY",
        )
        assert meta.trebuet_autentifikatsii is True
        assert meta.peremennaya_avt_env == "ZAKUPKI_API_KEY"

    def test_dostupna_li_autentifikatsiya_no_auth_obyazatelen(self) -> None:
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_otsutstvuyushchaya_peremennaya(self) -> None:
        meta = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_env_var_set(self) -> None:
        meta = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=True,
            peremennaya_avt_env="TEST_MCP_KEY",
        )
        with patch.dict(os.environ, {"TEST_MCP_KEY": "secret"}):
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_requires_auth_no_env_var(self) -> None:
        meta = MetaFunktsii(imya="t", opisanie="T", trebuet_autentifikatsii=True)
        assert meta.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_optional_auth_no_env(self) -> None:
        meta = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=False,
            peremennaya_avt_env="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_neobyazatelnaya_s_peremennoy(self) -> None:
        meta = MetaFunktsii(
            imya="t",
            opisanie="T",
            trebuet_autentifikatsii=False,
            peremennaya_avt_env="TEST_OPT_KEY",
        )
        with patch.dict(os.environ, {"TEST_OPT_KEY": "val"}):
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_zamorozhennyy(self) -> None:
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        with pytest.raises(AttributeError):
            meta.imya = "other"  # type: ignore[misc]

    def test_tegi_po_umolchaniyu_pustye(self) -> None:
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ")
        assert meta.tegi == []

    def test_tegi_polzovatelskie(self) -> None:
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ", tegi=["валюта", "курсы"])
        assert meta.tegi == ["валюта", "курсы"]


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
        """Discovery находит feature cbrf в пакете data."""
        reyestr = ReyestrFunktsiy()
        reyestr.obnaruzhit("mcp_russia.data")
        assert "cbrf" in reyestr.funktsii

    def test_obnaruzhenie_nakhodit_deloproizvodstvo(self) -> None:
        """Discovery находит feature deloproizvodstvo в пакете agenty."""
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
        """Mount с пустым registry не вызывает исключение."""
        reyestr = ReyestrFunktsiy()
        koren = FastMCP("test-root")
        reyestr.smontirovat_vse(koren)  # не должен вызывать исключение

    def test_zaregistrirovat_i_smontirovat_vruchnuyu(self) -> None:
        """Регистрирует feature вручную и монтирует в root."""
        reyestr = ReyestrFunktsiy()

        meta = MetaFunktsii(imya="test_feat", opisanie="Тестовая функция")
        podserver = FastMCP("test-sub")

        @podserver.tool
        def ping_fn() -> str:
            """Инструмент проверки связи."""
            return "pong"

        reyestr._features["test_feat"] = ZaregistrirovannayaFunktsiya(
            metadannye=meta,
            server_fn=podserver,
            put_modulya="fake.module",
        )

        koren = FastMCP("test-root")
        reyestr.smontirovat_vse(koren)

        assert reyestr.poluchit_funktsiyu("test_feat") is not None
        assert "test_feat" in reyestr.svodka()

    def test_svodka_s_funktsiyami(self) -> None:
        reyestr = ReyestrFunktsiy()
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ данные")
        podmodul = FastMCP("sub")
        reyestr._features["cbrf"] = ZaregistrirovannayaFunktsiya(
            metadannye=meta, server_fn=podmodul, put_modulya="m"
        )
        svodka_testa = reyestr.svodka()
        assert "1 функция(й) активно" in svodka_testa
        assert "cbrf" in svodka_testa
        assert "ЦБ РФ данные" in svodka_testa

    def test_svodka_s_propushchennymi(self) -> None:
        reyestr = ReyestrFunktsiy()
        reyestr._skipped["broken"] = "отсутствует META_FUNKTSII"
        svodka_testa = reyestr.svodka()
        assert "1 пропущено" in svodka_testa
        assert "broken" in svodka_testa

    def test_propushcheno_vozvrashchaet_kopiyu(self) -> None:
        reyestr = ReyestrFunktsiy()
        reyestr._skipped["x"] = "reason"
        propushcheno = reyestr.propushcheno
        propushcheno["y"] = "other"
        assert "y" not in reyestr._skipped

    def test_funktsii_vozvrashchaet_kopiyu(self) -> None:
        reyestr = ReyestrFunktsiy()
        funktsii = reyestr.funktsii
        funktsii["poddelnyy"] = None  # type: ignore[assignment]
        assert "poddelnyy" not in reyestr._features


# ---------------------------------------------------------------------------
# Интеграция: монтирование и вызов через fastmcp.Client
# ---------------------------------------------------------------------------


class TestIntegratsiyaReestra:
    @pytest.mark.asyncio
    async def test_smontirovannyy_instrument_vyzyvaemyy(self) -> None:
        """Инструмент, подключённый через registry, вызывается через Client."""
        podmodul = FastMCP("sub")

        @podmodul.tool
        def ekho(soobshcheniye: str) -> str:
            """Вернуть сообщение."""
            return f"echo: {soobshcheniye}"

        koren = FastMCP("root")
        koren.mount(podmodul, namespace="test")

        async with Client(koren) as klient:
            rezultat = await klient.call_tool("test_ekho", {"soobshcheniye": "hello"})
            assert rezultat.data == "echo: hello"

    @pytest.mark.asyncio
    async def test_kornevoy_server_zapuskaetsya_pustym(self) -> None:
        """Root-сервер без подключённых features работает."""
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
