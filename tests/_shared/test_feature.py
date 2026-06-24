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
    def test_create_minimal(self) -> None:
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ API")
        assert meta.name == "cbrf"
        assert meta.description == "ЦБ РФ API"
        assert meta.version == "0.1.0"
        assert meta.enabled is True
        assert meta.requires_auth is False

    def test_create_with_auth(self) -> None:
        meta = MetaFunktsii(
            name="zakupki",
            description="ЕИС Закупки",
            requires_auth=True,
            auth_env_var="ZAKUPKI_API_KEY",
        )
        assert meta.requires_auth is True
        assert meta.auth_env_var == "ZAKUPKI_API_KEY"

    def test_dostupna_li_autentifikatsiya_no_auth_required(self) -> None:
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ")
        assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_missing_env_var(self) -> None:
        meta = MetaFunktsii(
            name="t",
            description="T",
            requires_auth=True,
            auth_env_var="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_env_var_set(self) -> None:
        meta = MetaFunktsii(
            name="t",
            description="T",
            requires_auth=True,
            auth_env_var="TEST_MCP_KEY",
        )
        with patch.dict(os.environ, {"TEST_MCP_KEY": "secret"}):
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_requires_auth_no_env_var(self) -> None:
        meta = MetaFunktsii(name="t", description="T", requires_auth=True)
        assert meta.dostupna_li_autentifikatsiya() is False

    def test_dostupna_li_autentifikatsiya_optional_auth_no_env(self) -> None:
        meta = MetaFunktsii(
            name="t",
            description="T",
            requires_auth=False,
            auth_env_var="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_dostupna_li_autentifikatsiya_optional_auth_with_env(self) -> None:
        meta = MetaFunktsii(
            name="t",
            description="T",
            requires_auth=False,
            auth_env_var="TEST_OPT_KEY",
        )
        with patch.dict(os.environ, {"TEST_OPT_KEY": "val"}):
            assert meta.dostupna_li_autentifikatsiya() is True

    def test_frozen(self) -> None:
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ")
        with pytest.raises(AttributeError):
            meta.name = "other"  # type: ignore[misc]

    def test_tags_default_empty(self) -> None:
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ")
        assert meta.tags == []

    def test_tags_custom(self) -> None:
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ", tags=["валюта", "курсы"])
        assert meta.tags == ["валюта", "курсы"]


# ---------------------------------------------------------------------------
# ReyestrFunktsiy (реестр модулей)
# ---------------------------------------------------------------------------


class TestReyestrFunktsiy:
    def test_empty_registry(self) -> None:
        registry = ReyestrFunktsiy()
        assert registry.funktsii == {}
        assert registry.propushcheno == {}

    def test_discover_returns_self_for_chaining(self) -> None:
        """obnaruzhit() возвращает self для цепочки вызовов."""
        registry = ReyestrFunktsiy()
        result = registry.obnaruzhit("mcp_russia.data")
        assert result is registry

    def test_discover_finds_cbrf(self) -> None:
        """Discovery находит feature cbrf в пакете data."""
        registry = ReyestrFunktsiy()
        registry.obnaruzhit("mcp_russia.data")
        assert "cbrf" in registry.funktsii

    def test_discover_finds_redator(self) -> None:
        """Discovery находит feature redator в пакете agenty."""
        registry = ReyestrFunktsiy()
        registry.obnaruzhit("mcp_russia.agenty")
        assert "redator" in registry.funktsii

    def test_summary_empty(self) -> None:
        registry = ReyestrFunktsiy()
        summary = registry.svodka()
        assert "0 функция(й) активно" in summary
        assert "0 пропущено" in summary

    def test_get_feature_not_found(self) -> None:
        registry = ReyestrFunktsiy()
        assert registry.poluchit_funktsiyu("nonexistent") is None

    def test_mount_all_empty(self) -> None:
        """Mount с пустым registry не вызывает исключение."""
        registry = ReyestrFunktsiy()
        root = FastMCP("test-root")
        registry.smontirovat_vse(root)  # не должен вызывать исключение

    def test_register_and_mount_manual(self) -> None:
        """Регистрирует feature вручную и монтирует в root."""
        registry = ReyestrFunktsiy()

        meta = MetaFunktsii(name="test_feat", description="Тестовая функция")
        sub_server = FastMCP("test-sub")

        @sub_server.tool
        def ping() -> str:
            """Инструмент проверки связи."""
            return "pong"

        registry._features["test_feat"] = ZaregistrirovannayaFunktsiya(
            meta=meta,
            server=sub_server,
            module_path="fake.module",
        )

        root = FastMCP("test-root")
        registry.smontirovat_vse(root)

        assert registry.poluchit_funktsiyu("test_feat") is not None
        assert "test_feat" in registry.svodka()

    def test_summary_with_features(self) -> None:
        registry = ReyestrFunktsiy()
        meta = MetaFunktsii(name="cbrf", description="ЦБ РФ данные")
        sub = FastMCP("sub")
        registry._features["cbrf"] = ZaregistrirovannayaFunktsiya(
            meta=meta, server=sub, module_path="m"
        )
        summary = registry.svodka()
        assert "1 функция(й) активно" in summary
        assert "cbrf" in summary
        assert "ЦБ РФ данные" in summary

    def test_summary_with_skipped(self) -> None:
        registry = ReyestrFunktsiy()
        registry._skipped["broken"] = "отсутствует META_FUNKTSII"
        summary = registry.svodka()
        assert "1 пропущено" in summary
        assert "broken" in summary

    def test_skipped_returns_copy(self) -> None:
        registry = ReyestrFunktsiy()
        registry._skipped["x"] = "reason"
        skipped = registry.propushcheno
        skipped["y"] = "other"
        assert "y" not in registry._skipped

    def test_features_returns_copy(self) -> None:
        registry = ReyestrFunktsiy()
        features = registry.funktsii
        features["fake"] = None  # type: ignore[assignment]
        assert "fake" not in registry._features


# ---------------------------------------------------------------------------
# Интеграция: монтирование и вызов через fastmcp.Client
# ---------------------------------------------------------------------------


class TestRegistryIntegration:
    @pytest.mark.asyncio
    async def test_mounted_tool_callable(self) -> None:
        """Инструмент, подключённый через registry, вызывается через Client."""
        sub = FastMCP("sub")

        @sub.tool
        def echo(msg: str) -> str:
            """Вернуть сообщение."""
            return f"echo: {msg}"

        root = FastMCP("root")
        root.mount(sub, namespace="test")

        async with Client(root) as client:
            result = await client.call_tool("test_echo", {"msg": "hello"})
            assert result.data == "echo: hello"

    @pytest.mark.asyncio
    async def test_root_server_starts_empty(self) -> None:
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
            result = await client.call_tool("spisok_funktsiy", {})
            assert "mcp-russia" in result.data
