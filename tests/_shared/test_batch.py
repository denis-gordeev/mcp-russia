"""Тесты модуля пакетного выполнения."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_russia._shared import batch


def _maket_konteksta() -> MagicMock:
    ctx = MagicMock()
    ctx.info = AsyncMock()
    return ctx


@pytest.fixture(autouse=True)
def _sbrosit_dispetchera() -> None:
    """Очищает таблицу диспетчеризации перед каждым тестом."""
    batch._dispetcher.clear()


class TestPostroenieDispetcherizatsii:
    def test_stroitsya_iz_reestra(self) -> None:
        """Должен обнаруживать инструменты из модулей features."""
        rezultat = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("cbrf_") for k in rezultat)

    def test_nakhodit_vlozhennye_moduli(self) -> None:
        """Должен обнаруживать инструменты в подпакетах."""
        rezultat = batch.postroit_dispetcherizatsiyu(_real_registry())
        assert any(k.startswith("sovfed_") for k in rezultat)
        assert any(k.startswith("kaznacheistvo_") for k in rezultat)

    def test_keshiruet_rezultat(self) -> None:
        """Повторный вызов должен возвращать кэшированную таблицу диспетчеризации."""
        reg = _real_registry()
        pervyy = batch.postroit_dispetcherizatsiyu(reg)
        vtoroy = batch.postroit_dispetcherizatsiyu(reg)
        assert pervyy is vtoroy


class TestVypolneniePaketa:
    @pytest.mark.asyncio
    async def test_pustoy_spisok(self) -> None:
        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy([], ctx)
        assert "Нет запросов" in rezultat

    @pytest.mark.asyncio
    async def test_prevyshaet_limit(self) -> None:
        ctx = _maket_konteksta()
        zaprosy = [{"instrument": "x", "argumenty": {}} for _ in range(11)]
        rezultat = await batch.vypolnit_paket_vnutrenniy(zaprosy, ctx)
        assert "Максимум 10" in rezultat

    @pytest.mark.asyncio
    async def test_neizvestnyy_instrument(self) -> None:
        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "nonexistent_tool", "argumenty": {}}], ctx
        )
        assert "не найден" in rezultat

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_s_kontekstom(self) -> None:
        """Должен передавать ctx инструментам, которые его принимают."""

        async def _spec(ctx: object, param: str) -> str: ...

        maket_funktsii = AsyncMock(spec=_spec, return_value="rezultat ok")
        batch._dispetcher["test_tool"] = maket_funktsii

        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "test_tool", "argumenty": {"param": "value"}}], ctx
        )
        assert "rezultat ok" in rezultat
        maket_funktsii.assert_called_once()

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_bez_konteksta(self) -> None:
        """Должен работать с инструментами, не принимающими ctx."""

        async def instrument_bez_konteksta(imya: str) -> str:
            return f"privet {imya}"

        batch._dispetcher["greet"] = instrument_bez_konteksta

        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "greet", "argumenty": {"imya": "world"}}], ctx
        )
        assert "privet world" in rezultat

    @pytest.mark.asyncio
    async def test_parallelnoe_vypolnenie(self) -> None:
        """Должен выполнять несколько запросов параллельно."""
        schetchik_vyzovov = 0

        async def schitayushchiy_instrument(n: int) -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return f"rezultat-{n}"

        batch._dispetcher["counter"] = schitayushchiy_instrument

        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [
                {"instrument": "counter", "argumenty": {"n": 1}},
                {"instrument": "counter", "argumenty": {"n": 2}},
                {"instrument": "counter", "argumenty": {"n": 3}},
            ],
            ctx,
        )
        assert schetchik_vyzovov == 3
        assert "rezultat-1" in rezultat
        assert "rezultat-2" in rezultat
        assert "rezultat-3" in rezultat

    @pytest.mark.asyncio
    async def test_obrabatyvaet_oshibku_instrumenta(self) -> None:
        """Должен перехватывать исключения и включать ошибку в результаты."""

        async def neudachnyy_instrument() -> str:
            msg = "API timeout"
            raise TimeoutError(msg)

        batch._dispetcher["fail"] = neudachnyy_instrument

        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"instrument": "fail", "argumenty": {}}], ctx
        )
        assert "Ошибка" in rezultat
        assert "timeout" in rezultat.lower()

    @pytest.mark.asyncio
    async def test_smeshannye_uspekh_i_oshibka(self) -> None:
        """Должен возвращать частичные результаты при ошибках части инструментов."""

        async def normanyy_instrument() -> str:
            return "success"

        async def plokhoy_instrument() -> str:
            msg = "oops"
            raise ValueError(msg)

        batch._dispetcher["ok"] = normanyy_instrument
        batch._dispetcher["bad"] = plokhoy_instrument

        ctx = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [
                {"instrument": "ok", "argumenty": {}},
                {"instrument": "bad", "argumenty": {}},
            ],
            ctx,
        )
        assert "success" in rezultat
        assert "Ошибка" in rezultat


def _real_registry() -> batch.ReyestrFunktsiy:
    """Собирает реальный registry проекта для интеграционного тестирования."""
    from mcp_russia._shared.feature import ReyestrFunktsiy

    reg = ReyestrFunktsiy()
    reg.obnaruzhit("mcp_russia.data")
    reg.obnaruzhit("mcp_russia.agenty")
    return reg
