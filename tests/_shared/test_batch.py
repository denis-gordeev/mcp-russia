"""Тесты модуля пакетного выполнения."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_russia._shared import batch


def _maket_konteksta() -> MagicMock:
    kontekst = MagicMock()
    kontekst.info = AsyncMock()
    return kontekst


@pytest.fixture(autouse=True)
def _sbrosit_dispetchera() -> None:
    """Очищает таблицу диспетчеризации перед каждым тестом."""
    batch._dispetcher.clear()


class TestPostroenieDispetcherizatsii:
    def test_stroitsya_iz_reestra(self) -> None:
        """Должен обнаруживать инструменты из модулей features."""
        rezultat = batch.postroit_dispetcherizatsiyu(_realnyy_reyestr())
        assert any(k.startswith("cbrf_") for k in rezultat)

    def test_nakhodit_vlozhennye_moduli(self) -> None:
        """Должен обнаруживать инструменты в подпакетах."""
        rezultat = batch.postroit_dispetcherizatsiyu(_realnyy_reyestr())
        assert any(k.startswith("sovfed_") for k in rezultat)
        assert any(k.startswith("kaznacheistvo_") for k in rezultat)

    def test_keshiruet_rezultat(self) -> None:
        """Повторный вызов должен возвращать кэшированную таблицу диспетчеризации."""
        reyestr = _realnyy_reyestr()
        pervyy = batch.postroit_dispetcherizatsiyu(reyestr)
        vtoroy = batch.postroit_dispetcherizatsiyu(reyestr)
        assert pervyy is vtoroy


class TestVypolneniePaketa:
    @pytest.mark.asyncio
    async def test_pustoy_spisok(self) -> None:
        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy([], kontekst)
        assert "Нет запросов" in rezultat

    @pytest.mark.asyncio
    async def test_prevyshaet_limit(self) -> None:
        kontekst = _maket_konteksta()
        zaprosy = [{"imya_instrumenta": "x", "argumenty": {}} for _ in range(11)]
        rezultat = await batch.vypolnit_paket_vnutrenniy(zaprosy, kontekst)
        assert "Максимум 10" in rezultat

    @pytest.mark.asyncio
    async def test_neizvestnyy_instrument(self) -> None:
        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"imya_instrumenta": "nesushchestvuyushchiy_instrument", "argumenty": {}}], kontekst
        )
        assert "не найден" in rezultat

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_s_kontekstom(self) -> None:
        """Должен передавать kontekst инструментам, которые его принимают."""

        async def _spets(kontekst: object, parametr: str) -> str: ...

        maket_funktsii = AsyncMock(spec=_spets, return_value="rezultat uspekha")
        batch._dispetcher["proverochnyy_instrument"] = maket_funktsii

        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [
                {
                    "imya_instrumenta": "proverochnyy_instrument",
                    "argumenty": {"parametr": "znachenie"},
                }
            ],
            kontekst,
        )
        assert "rezultat uspekha" in rezultat
        maket_funktsii.assert_called_once()

    @pytest.mark.asyncio
    async def test_vyzyvaet_instrument_bez_konteksta(self) -> None:
        """Должен работать с инструментами, не принимающими kontekst."""

        async def instrument_ne_trebuet_konteksta(imya: str) -> str:
            return f"privet {imya}"

        batch._dispetcher["privetstvie"] = instrument_ne_trebuet_konteksta

        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"imya_instrumenta": "privetstvie", "argumenty": {"imya": "mir"}}], kontekst
        )
        assert "privet mir" in rezultat

    @pytest.mark.asyncio
    async def test_parallelnoe_vypolnenie(self) -> None:
        """Должен выполнять несколько запросов параллельно."""
        schetchik_vyzovov = 0

        async def schitayushchiy_instrument(n: int) -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return f"rezultat-{n}"

        batch._dispetcher["schetchik"] = schitayushchiy_instrument

        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [
                {"imya_instrumenta": "schetchik", "argumenty": {"n": 1}},
                {"imya_instrumenta": "schetchik", "argumenty": {"n": 2}},
                {"imya_instrumenta": "schetchik", "argumenty": {"n": 3}},
            ],
            kontekst,
        )
        assert schetchik_vyzovov == 3
        assert "rezultat-1" in rezultat
        assert "rezultat-2" in rezultat
        assert "rezultat-3" in rezultat

    @pytest.mark.asyncio
    async def test_obrabatyvaet_oshibku_instrumenta(self) -> None:
        """Должен перехватывать исключения и включать ошибку в результаты."""

        async def neudachnyy_instrument() -> str:
            msg = "Таймаут API"
            raise TimeoutError(msg)

        batch._dispetcher["neudacha"] = neudachnyy_instrument

        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [{"imya_instrumenta": "neudacha", "argumenty": {}}], kontekst
        )
        assert "Ошибка" in rezultat
        assert "таймаут" in rezultat.lower()

    @pytest.mark.asyncio
    async def test_smeshannye_uspekh_i_oshibka(self) -> None:
        """Должен возвращать частичные результаты при ошибках части инструментов."""

        async def normanyy_instrument() -> str:
            return "uspekh"

        async def plokhoy_instrument() -> str:
            msg = "oy"
            raise ValueError(msg)

        batch._dispetcher["norma"] = normanyy_instrument
        batch._dispetcher["plokho"] = plokhoy_instrument

        kontekst = _maket_konteksta()
        rezultat = await batch.vypolnit_paket_vnutrenniy(
            [
                {"imya_instrumenta": "norma", "argumenty": {}},
                {"imya_instrumenta": "plokho", "argumenty": {}},
            ],
            kontekst,
        )
        assert "uspekh" in rezultat
        assert "Ошибка" in rezultat


def _realnyy_reyestr() -> batch.ReyestrFunktsiy:
    """Собирает реальный реестр проекта для интеграционного тестирования."""
    from mcp_russia._shared.feature import ReyestrFunktsiy

    reyestr = ReyestrFunktsiy()
    reyestr.obnaruzhit("mcp_russia.data")
    reyestr.obnaruzhit("mcp_russia.agenty")
    return reyestr
