"""Тесты модуля Россельхознадзор."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from mcp_russia.data.rosselkhoznadzor import client, tools
from mcp_russia.data.rosselkhoznadzor.constants import (
    FEDERALNYE_OKRUGA_RSKHN,
    KARANTINNYE_OBYEKTY,
    KATEGORII_PROVEROK,
    STATISTIKA_RSKHN_2023,
    TIPY_PRODUKTSII,
    VIDY_NADZORA,
    VIDY_NARUSHENIY_RSKHN,
)
from mcp_russia.data.rosselkhoznadzor.server import mcp as rosselkhoznadzor_server


class TestKonstanty:
    def test_vidy_nadzora(self) -> None:
        assert len(VIDY_NADZORA) == 6
        codes = [v["kod"] for v in VIDY_NADZORA]
        assert "veterinarnyy" in codes
        assert "fitosanitarnyy" in codes

    def test_kategorii_proverok(self) -> None:
        assert len(KATEGORII_PROVEROK) == 4

    def test_vidy_narusheniy(self) -> None:
        assert len(VIDY_NARUSHENIY_RSKHN) == 6

    def test_tipy_produktsii(self) -> None:
        assert len(TIPY_PRODUKTSII) == 5

    def test_karantinnye_obekty(self) -> None:
        assert len(KARANTINNYE_OBYEKTY) == 3

    def test_federalnye_okruga(self) -> None:
        assert len(FEDERALNYE_OKRUGA_RSKHN) == 8

    def test_statistika_rskhn(self) -> None:
        assert STATISTIKA_RSKHN_2023["vsego_proverok"] > 0
        assert "po_vidam" in STATISTIKA_RSKHN_2023


class TestInstrumenty:
    @pytest.mark.asyncio
    async def test_spisok_vidov_nadzora(self) -> None:
        ctx = AsyncMock()
        rezultat = await tools.spisok_vidov_nadzora(ctx)
        assert "Ветеринарный надзор" in rezultat
        assert "Фитосанитарный контроль" in rezultat

    @pytest.mark.asyncio
    async def test_spisok_kategoriy_proverok(self) -> None:
        ctx = AsyncMock()
        rezultat = await tools.spisok_kategoriy_proverok(ctx)
        assert "Плановая" in rezultat

    @pytest.mark.asyncio
    async def test_spisok_vidov_narusheniy(self) -> None:
        ctx = AsyncMock()
        rezultat = await tools.spisok_vidov_narusheniy(ctx)
        assert "ветеринарного" in rezultat

    @pytest.mark.asyncio
    async def test_spisok_tipov_produktsii(self) -> None:
        ctx = AsyncMock()
        rezultat = await tools.spisok_tipov_produktsii(ctx)
        assert "Животноводческая" in rezultat

    @pytest.mark.asyncio
    async def test_poisk_proverok_zapasnoy(self) -> None:
        ctx = AsyncMock()
        with patch.object(client, "poisk_proverok", return_value=[]):
            rezultat = await tools.poisk_proverok(ctx)
        assert "резервные данные" in rezultat or "не найдены" in rezultat

    @pytest.mark.asyncio
    async def test_poisk_proverok_s_dannymi(self) -> None:
        ctx = AsyncMock()
        maket_dannykh = [
            {
                "nomer": "123",
                "vid_nadzora": "Ветеринарный",
                "data_provedeniya": "2024-01-15",
                "subiekt": "Московская область",
                "sostoyanie": "Завершена",
                "narusheniya": 3,
            }
        ]
        with patch.object(client, "poisk_proverok", return_value=maket_dannykh):
            rezultat = await tools.poisk_proverok(ctx)
        assert "123" in rezultat
        assert "Ветеринарный" in rezultat

    @pytest.mark.asyncio
    async def test_poisk_karantinnykh_obektov_pustoy(self) -> None:
        ctx = AsyncMock()
        with patch.object(client, "poisk_karantinnykh_obektov", return_value=[]):
            rezultat = await tools.poisk_karantinnykh_obektov(ctx)
        assert "не найдены" in rezultat

    @pytest.mark.asyncio
    async def test_poisk_karantinnykh_obektov_s_dannymi(self) -> None:
        ctx = AsyncMock()
        maket_dannykh = [
            {
                "nazvanie": "Калифорнийская щитовка",
                "tip": "Вредитель",
                "subiekt": "Краснодарский край",
                "status_karantina": "Действует",
                "data_vvedeniya": "2023-06-01",
            }
        ]
        with patch.object(client, "poisk_karantinnykh_obektov", return_value=maket_dannykh):
            rezultat = await tools.poisk_karantinnykh_obektov(ctx)
        assert "Калифорнийская" in rezultat

    @pytest.mark.asyncio
    async def test_poisk_registratsiy_pustoy(self) -> None:
        ctx = AsyncMock()
        with patch.object(client, "poisk_registratsiy_produktsii", return_value=[]):
            rezultat = await tools.poisk_registratsiy_produktsii(ctx)
        assert "не найдена" in rezultat

    @pytest.mark.asyncio
    async def test_veterinarsnye_sertifikaty_pustoy(self) -> None:
        ctx = AsyncMock()
        with patch.object(client, "veterinarsnye_sertifikaty", return_value=[]):
            rezultat = await tools.veterinarsnye_sertifikaty(ctx)
        assert "не найдены" in rezultat

    @pytest.mark.asyncio
    async def test_preduprezhdeniya_karantina_pustoy(self) -> None:
        ctx = AsyncMock()
        with patch.object(client, "preduprezhdeniya_karantina", return_value=[]):
            rezultat = await tools.preduprezhdeniya_karantina(ctx)
        assert "не найдены" in rezultat


class TestIntegratsiya:
    @pytest.mark.asyncio
    async def test_server_imeet_instrumenty(self) -> None:
        async with Client(rosselkhoznadzor_server) as c:
            tool_names = [t.name for t in await c.list_tools()]
        assert "spisok_vidov_nadzora" in tool_names
        assert "poisk_proverok" in tool_names
        assert "poisk_karantinnykh_obektov" in tool_names

    @pytest.mark.asyncio
    async def test_server_imeet_resursy(self) -> None:
        async with Client(rosselkhoznadzor_server) as c:
            resources = await c.list_resources()
        assert len(resources) >= 3

    @pytest.mark.asyncio
    async def test_server_imeet_prompty(self) -> None:
        async with Client(rosselkhoznadzor_server) as c:
            prompts = await c.list_prompts()
        assert len(prompts) >= 2
