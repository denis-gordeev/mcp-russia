"""Тесты FeatureRegistry и FeatureMeta."""

import os
from unittest.mock import patch

import pytest
from fastmcp import Client, FastMCP

from mcp_russia._shared.feature import FeatureMeta, FeatureRegistry, RegisteredFeature

# ---------------------------------------------------------------------------
# FeatureMeta
# ---------------------------------------------------------------------------


class TestFeatureMeta:
    def test_create_minimal(self) -> None:
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ API")
        assert meta.name == "cbrf"
        assert meta.description == "ЦБ РФ API"
        assert meta.version == "0.1.0"
        assert meta.enabled is True
        assert meta.requires_auth is False

    def test_create_with_auth(self) -> None:
        meta = FeatureMeta(
            name="zakupki",
            description="ЕИС Закупки",
            requires_auth=True,
            auth_env_var="ZAKUPKI_API_KEY",
        )
        assert meta.requires_auth is True
        assert meta.auth_env_var == "ZAKUPKI_API_KEY"

    def test_is_auth_available_no_auth_required(self) -> None:
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ")
        assert meta.is_auth_available() is True

    def test_is_auth_available_missing_env_var(self) -> None:
        meta = FeatureMeta(
            name="t",
            description="T",
            requires_auth=True,
            auth_env_var="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.is_auth_available() is False

    def test_is_auth_available_env_var_set(self) -> None:
        meta = FeatureMeta(
            name="t",
            description="T",
            requires_auth=True,
            auth_env_var="TEST_MCP_KEY",
        )
        with patch.dict(os.environ, {"TEST_MCP_KEY": "secret"}):
            assert meta.is_auth_available() is True

    def test_is_auth_available_requires_auth_no_env_var(self) -> None:
        meta = FeatureMeta(name="t", description="T", requires_auth=True)
        assert meta.is_auth_available() is False

    def test_is_auth_available_optional_auth_no_env(self) -> None:
        meta = FeatureMeta(
            name="t",
            description="T",
            requires_auth=False,
            auth_env_var="FAKE_KEY_NOT_SET",
        )
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FAKE_KEY_NOT_SET", None)
            assert meta.is_auth_available() is True

    def test_is_auth_available_optional_auth_with_env(self) -> None:
        meta = FeatureMeta(
            name="t",
            description="T",
            requires_auth=False,
            auth_env_var="TEST_OPT_KEY",
        )
        with patch.dict(os.environ, {"TEST_OPT_KEY": "val"}):
            assert meta.is_auth_available() is True

    def test_frozen(self) -> None:
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ")
        with pytest.raises(AttributeError):
            meta.name = "other"  # type: ignore[misc]

    def test_tags_default_empty(self) -> None:
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ")
        assert meta.tags == []

    def test_tags_custom(self) -> None:
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ", tags=["валюта", "курсы"])
        assert meta.tags == ["валюта", "курсы"]


# ---------------------------------------------------------------------------
# FeatureRegistry
# ---------------------------------------------------------------------------


class TestFeatureRegistry:
    def test_empty_registry(self) -> None:
        registry = FeatureRegistry()
        assert registry.features == {}
        assert registry.skipped == {}

    def test_discover_returns_self_for_chaining(self) -> None:
        """discover() возвращает self для цепочки вызовов."""
        registry = FeatureRegistry()
        result = registry.discover("mcp_russia.data")
        assert result is registry

    def test_discover_finds_cbrf(self) -> None:
        """Discovery находит feature cbrf в пакете data."""
        registry = FeatureRegistry()
        registry.discover("mcp_russia.data")
        assert "cbrf" in registry.features

    def test_discover_finds_redator(self) -> None:
        """Discovery находит feature redator в пакете agenty."""
        registry = FeatureRegistry()
        registry.discover("mcp_russia.agenty")
        assert "redator" in registry.features

    def test_summary_empty(self) -> None:
        registry = FeatureRegistry()
        summary = registry.summary()
        assert "0 функция(й) активно" in summary
        assert "0 пропущено" in summary

    def test_get_feature_not_found(self) -> None:
        registry = FeatureRegistry()
        assert registry.get_feature("nonexistent") is None

    def test_mount_all_empty(self) -> None:
        """Mount с пустым registry не вызывает исключение."""
        registry = FeatureRegistry()
        root = FastMCP("test-root")
        registry.mount_all(root)  # не должен вызывать исключение

    def test_register_and_mount_manual(self) -> None:
        """Регистрирует feature вручную и монтирует в root."""
        registry = FeatureRegistry()

        meta = FeatureMeta(name="test_feat", description="Тестовая функция")
        sub_server = FastMCP("test-sub")

        @sub_server.tool
        def ping() -> str:
            """Инструмент проверки связи."""
            return "pong"

        registry._features["test_feat"] = RegisteredFeature(
            meta=meta,
            server=sub_server,
            module_path="fake.module",
        )

        root = FastMCP("test-root")
        registry.mount_all(root)

        assert registry.get_feature("test_feat") is not None
        assert "test_feat" in registry.summary()

    def test_summary_with_features(self) -> None:
        registry = FeatureRegistry()
        meta = FeatureMeta(name="cbrf", description="ЦБ РФ данные")
        sub = FastMCP("sub")
        registry._features["cbrf"] = RegisteredFeature(meta=meta, server=sub, module_path="m")
        summary = registry.summary()
        assert "1 функция(й) активно" in summary
        assert "cbrf" in summary
        assert "ЦБ РФ данные" in summary

    def test_summary_with_skipped(self) -> None:
        registry = FeatureRegistry()
        registry._skipped["broken"] = "отсутствует FEATURE_META"
        summary = registry.summary()
        assert "1 пропущено" in summary
        assert "broken" in summary

    def test_skipped_returns_copy(self) -> None:
        registry = FeatureRegistry()
        registry._skipped["x"] = "reason"
        skipped = registry.skipped
        skipped["y"] = "other"
        assert "y" not in registry._skipped

    def test_features_returns_copy(self) -> None:
        registry = FeatureRegistry()
        features = registry.features
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
