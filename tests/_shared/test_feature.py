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

    def test_dostupna_li_autentifikatsiya_missing_env_var(self) -> None:
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

    def test_dostupna_li_autentifikatsiya_optional_auth_with_env(self) -> None:
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
        registry = ReyestrFunktsiy()
        assert registry.funktsii == {}
        assert registry.propushcheno == {}

    def test_obnaruzhenie_vozvrashchaet_self_dlya_tsepochki(self) -> None:
        """obnaruzhit() возвращает self для цепочки вызовов."""
        registry = ReyestrFunktsiy()
        rezultat = registry.obnaruzhit("mcp_russia.data")
        assert rezultat is registry

    def test_obnaruzhenie_nakhodit_cbrf(self) -> None:
        """Discovery находит feature cbrf в пакете data."""
        registry = ReyestrFunktsiy()
        registry.obnaruzhit("mcp_russia.data")
        assert "cbrf" in registry.funktsii

    def test_obnaruzhenie_nakhodit_deloproizvodstvo(self) -> None:
        """Discovery находит feature deloproizvodstvo в пакете agenty."""
        registry = ReyestrFunktsiy()
        registry.obnaruzhit("mcp_russia.agenty")
        assert "deloproizvodstvo" in registry.funktsii

    def test_svodka_pustoy(self) -> None:
        registry = ReyestrFunktsiy()
        summary = registry.svodka()
        assert "0 функция(й) активно" in summary
        assert "0 пропущено" in summary

    def test_poluchit_funktsiyu_ne_naydena(self) -> None:
        registry = ReyestrFunktsiy()
        assert registry.poluchit_funktsiyu("nesushchestvuyushchiy") is None

    def test_smontirovat_vse_pustoy(self) -> None:
        """Mount с пустым registry не вызывает исключение."""
        registry = ReyestrFunktsiy()
        root = FastMCP("test-root")
        registry.smontirovat_vse(root)  # не должен вызывать исключение

    def test_zaregistrirovat_i_smontirovat_vruchnuyu(self) -> None:
        """Регистрирует feature вручную и монтирует в root."""
        registry = ReyestrFunktsiy()

        meta = MetaFunktsii(imya="test_feat", opisanie="Тестовая функция")
        sub_server = FastMCP("test-sub")

        @sub_server.tool
        def ping() -> str:
            """Инструмент проверки связи."""
            return "pong"

        registry._features["test_feat"] = ZaregistrirovannayaFunktsiya(
            metadannye=meta,
            server_fn=sub_server,
            put_modulya="fake.module",
        )

        root = FastMCP("test-root")
        registry.smontirovat_vse(root)

        assert registry.poluchit_funktsiyu("test_feat") is not None
        assert "test_feat" in registry.svodka()

    def test_svodka_s_funktsiyami(self) -> None:
        registry = ReyestrFunktsiy()
        meta = MetaFunktsii(imya="cbrf", opisanie="ЦБ РФ данные")
        sub = FastMCP("sub")
        registry._features["cbrf"] = ZaregistrirovannayaFunktsiya(
            metadannye=meta, server_fn=sub, put_modulya="m"
        )
        summary = registry.svodka()
        assert "1 функция(й) активно" in summary
        assert "cbrf" in summary
        assert "ЦБ РФ данные" in summary

    def test_svodka_s_propushchennymi(self) -> None:
        registry = ReyestrFunktsiy()
        registry._skipped["broken"] = "отсутствует META_FUNKTSII"
        summary = registry.svodka()
        assert "1 пропущено" in summary
        assert "broken" in summary

    def test_propushcheno_vozvrashchaet_kopiyu(self) -> None:
        registry = ReyestrFunktsiy()
        registry._skipped["x"] = "reason"
        skipped = registry.propushcheno
        skipped["y"] = "other"
        assert "y" not in registry._skipped

    def test_funktsii_vozvrashchaet_kopiyu(self) -> None:
        registry = ReyestrFunktsiy()
        features = registry.funktsii
        features["poddelnyy"] = None  # type: ignore[assignment]
        assert "poddelnyy" not in registry._features


# ---------------------------------------------------------------------------
# Интеграция: монтирование и вызов через fastmcp.Client
# ---------------------------------------------------------------------------


class TestIntegratsiyaReestra:
    @pytest.mark.asyncio
    async def test_smontirovannyy_instrument_vyzyvaemyy(self) -> None:
        """Инструмент, подключённый через registry, вызывается через Client."""
        sub = FastMCP("sub")

        @sub.tool
        def echo(msg: str) -> str:
            """Вернуть сообщение."""
            return f"echo: {msg}"

        root = FastMCP("root")
        root.mount(sub, namespace="test")

        async with Client(root) as client:
            rezultat = await client.call_tool("test_echo", {"msg": "hello"})
            assert rezultat.data == "echo: hello"

    @pytest.mark.asyncio
    async def test_kornevoy_server_zapuskaetsya_pustym(self) -> None:
        """Root-сервер без подключённых features работает."""
        from mcp_russia.server import mcp

        async with Client(mcp) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]
            assert "spisok_funktsiy" in tool_names

    @pytest.mark.asyncio
    async def test_spisok_funktsiy_tool(self) -> None:
        """Мета-инструмент spisok_funktsiy возвращает сводку."""
        from mcp_russia.server import mcp

        async with Client(mcp) as client:
            rezultat = await client.call_tool("spisok_funktsiy", {})
            assert "mcp-russia" in rezultat.data
