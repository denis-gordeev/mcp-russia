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
    batch._dispetcher.clear()


class TestPostroenieDispetcherizatsii:
    def test_stroitsya_iz_reestra(self) -> None:
        """Должен обнаруживать инструменты из модулей features."""
        result = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("cbrf_") for k in result)

    def test_nakhodit_vlozhennye_moduli(self) -> None:
        """Должен обнаруживать инструменты в подпакетах."""
        result = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("sovfed_") for k in result)
        assert any(k.startswith("kaznacheistvo_") for k in result)

    def test_keshiruet_rezultat(self) -> None:
        """Повторный вызов должен возвращать кэшированную таблицу диспетчеризации."""
        reg = _real_registry()
        first = batch.postroit_dispetcherizatsiyu(reg)
        second = batch.postroit_dispetcherizatsiyu(reg)
        assert first is second


class TestVypolneniePaketa:
    @pytest.mark.asyncio
    async def test_pustoy_spisok(self) -> None:
        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy([], ctx)
        assert "Нет запросов" in result

    @pytest.mark.asyncio
    async def test_prevyshaet_limit(self) -> None:
        ctx = _mock_ctx()
        queries = [{"instrument": "x", "argumenty": {}} for _ in range(11)]
        result = await batch.vypolnit_paket_vnutrenniy(queries, ctx)
        assert "Максимум 10" in result

    @pytest.mark.asyncio
    async def test_neizvestnyy_instrument(self) -> None:
        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "nonexistent_tool", "argumenty": {}}], ctx
        )
        assert "не найден" in result

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_s_kontekstom(self) -> None:
        """Должен передавать ctx инструментам, которые его принимают."""

        async def _spec(ctx: object, param: str) -> str: ...

        mock_fn = AsyncMock(spec=_spec, return_value="rezultat ok")
        batch._dispetcher["test_tool"] = mock_fn

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "test_tool", "argumenty": {"param": "value"}}], ctx
        )
        assert "rezultat ok" in result
        mock_fn.assert_called_once()

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_bez_konteksta(self) -> None:
        """Должен работать с инструментами, не принимающими ctx."""

        async def no_ctx_tool(name: str) -> str:
            return f"hello {name}"

        batch._dispetcher["greet"] = no_ctx_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "greet", "argumenty": {"name": "world"}}], ctx
        )
        assert "hello world" in result

    @pytest.mark.asyncio
    async def test_parallelnoe_vypolnenie(self) -> None:
        """Должен выполнять несколько запросов параллельно."""
        call_count = 0

        async def counting_tool(n: int) -> str:
            nonlocal call_count
            call_count += 1
            return f"result-{n}"

        batch._dispetcher["counter"] = counting_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [
                {"instrument": "counter", "argumenty": {"n": 1}},
                {"instrument": "counter", "argumenty": {"n": 2}},
                {"instrument": "counter", "argumenty": {"n": 3}},
            ],
            ctx,
        )
        assert call_count == 3
        assert "result-1" in result
        assert "result-2" in result
        assert "result-3" in result

    @pytest.mark.asyncio
    async def test_obrabatyvaet_oshibku_instrumenta(self) -> None:
        """Должен перехватывать исключения и включать ошибку в результаты."""

        async def failing_tool() -> str:
            msg = "API timeout"
            raise TimeoutError(msg)

        batch._dispetcher["fail"] = failing_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "fail", "argumenty": {}}], ctx
        )
        assert "Ошибка" in result
        assert "timeout" in result.lower()

    @pytest.mark.asyncio
    async def test_smeshannye_uspekh_i_oshibka(self) -> None:
        """Должен возвращать частичные результаты при ошибках части инструментов."""

        async def ok_tool() -> str:
            return "success"

        async def bad_tool() -> str:
            msg = "oops"
            raise ValueError(msg)

        batch._dispetcher["ok"] = ok_tool
        batch._dispetcher["bad"] = bad_tool

        ctx = _mock_ctx()
        result = await batch.vypolnit_paket_vnutrenniy(
            [
                {"instrument": "ok", "argumenty": {}},
                {"instrument": "bad", "argumenty": {}},
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
