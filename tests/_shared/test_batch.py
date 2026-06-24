"""Тесты модуля пакетного выполнения."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_russia._shared import batch


def _mock_ctx() -> MagicMock:
    ctx = MagicMock()
    ctx.info = AsyncMock()
    return ctx


@pytest.fixture(autouse=True)
def _reset_dispatch() -> None:
    """Очищает таблицу диспетчеризации перед каждым тестом."""
    batch._dispatch.clear()


class TestBuildDispatch:
    def test_builds_from_registry(self) -> None:
        """Должен обнаруживать инструменты из модулей features."""
        result = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("cbrf_") for k in result)

    def test_finds_nested_features(self) -> None:
        """Должен обнаруживать инструменты в подпакетах."""
        result = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("sovfed_") for k in result)
        assert any(k.startswith("kaznacheistvo_") for k in result)

    def test_caches_result(self) -> None:
        """Повторный вызов должен возвращать кэшированную таблицу диспетчеризации."""
        reg = _real_registry()
        first = batch.postroit_dispetcherizatsiyu(reg)
        second = batch.postroit_dispetcherizatsiyu(reg)
        assert first is second


class TestExecuteBatch:
    @pytest.mark.asyncio
    async def test_empty_list(self) -> None:
        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy([], ctx)
        assert "Нет запросов" in result

    @pytest.mark.asyncio
    async def test_exceeds_limit(self) -> None:
        ctx = _mock_ctx()
        queries = [{"tool": "x", "args": {}} for _ in range(11)]
        result = await batch.vypolnit_paket_vnutrenniy(queries, ctx)
        assert "Максимум 10" in result

    @pytest.mark.asyncio
    async def test_unknown_tool(self) -> None:
        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"tool": "nonexistent_tool", "args": {}}], ctx
        )
        assert "не найден" in result

    @pytest.mark.asyncio
    async def test_calls_tool_with_ctx(self) -> None:
        """Должен передавать ctx инструментам, которые его принимают."""

        async def _spec(ctx: object, param: str) -> str: ...

        mock_fn = AsyncMock(spec=_spec, return_value="rezultat ok")
        batch._dispatch["test_tool"] = mock_fn

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"tool": "test_tool", "args": {"param": "value"}}], ctx
        )
        assert "rezultat ok" in result
        mock_fn.assert_called_once()

    @pytest.mark.asyncio
    async def test_calls_tool_without_ctx(self) -> None:
        """Должен работать с инструментами, не принимающими ctx."""

        async def no_ctx_tool(name: str) -> str:
            return f"hello {name}"

        batch._dispatch["greet"] = no_ctx_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"tool": "greet", "args": {"name": "world"}}], ctx
        )
        assert "hello world" in result

    @pytest.mark.asyncio
    async def test_parallel_execution(self) -> None:
        """Должен выполнять несколько запросов параллельно."""
        call_count = 0

        async def counting_tool(n: int) -> str:
            nonlocal call_count
            call_count += 1
            return f"result-{n}"

        batch._dispatch["counter"] = counting_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [
                {"tool": "counter", "args": {"n": 1}},
                {"tool": "counter", "args": {"n": 2}},
                {"tool": "counter", "args": {"n": 3}},
            ],
            ctx,
        )
        assert call_count == 3
        assert "result-1" in result
        assert "result-2" in result
        assert "result-3" in result

    @pytest.mark.asyncio
    async def test_handles_tool_error(self) -> None:
        """Должен перехватывать исключения и включать ошибку в результаты."""

        async def failing_tool() -> str:
            msg = "API timeout"
            raise TimeoutError(msg)

        batch._dispatch["fail"] = failing_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy([{"tool": "fail", "args": {}}], ctx)
        assert "Ошибка" in result
        assert "timeout" in result.lower()

    @pytest.mark.asyncio
    async def test_mixed_success_and_failure(self) -> None:
        """Должен возвращать частичные результаты при ошибках части инструментов."""

        async def ok_tool() -> str:
            return "success"

        async def bad_tool() -> str:
            msg = "oops"
            raise ValueError(msg)

        batch._dispatch["ok"] = ok_tool
        batch._dispatch["bad"] = bad_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [
                {"tool": "ok", "args": {}},
                {"tool": "bad", "args": {}},
            ],
            ctx,
        )
        assert "success" in result
        assert "Ошибка" in result


def _real_registry() -> batch.ReyestrFunktsiy:
    """Собирает реальный registry проекта для интеграционного тестирования."""
    from mcp_russia._shared.feature import ReyestrFunktsiy

    reg = ReyestrFunktsiy()
    reg.obnaruzhit("mcp_russia.data")
    reg.obnaruzhit("mcp_russia.agenty")
    return reg
