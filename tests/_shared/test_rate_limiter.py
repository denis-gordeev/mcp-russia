"""Тесты асинхронного ограничителя запросов (OgranichitelChastoty)."""

from __future__ import annotations

import asyncio
import time

import pytest

from mcp_russia._shared.rate_limiter import OgranichitelChastoty


class TestOgranichitelChastoty:
    @pytest.mark.asyncio
    async def test_propuskaet_v_predelakh_limita(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=5, period=60.0)
        for _ in range(5):
            async with ogranichitel:
                pass
        # Все 5 должны пройти без блокировки

    @pytest.mark.asyncio
    async def test_blokiruet_pri_ischerpanii(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=2, period=60.0)
        async with ogranichitel:
            pass
        async with ogranichitel:
            pass

        # Третий запрос должен блокироваться; проверяем с коротким таймаутом
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(ogranichitel.zakhvatit(), timeout=0.05)

    @pytest.mark.asyncio
    async def test_propuskaet_posle_istecheniya_okna(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=1, period=0.05)
        async with ogranichitel:
            pass
        # Ждём истечения окна
        await asyncio.sleep(0.06)
        # Теперь должен быть разрешён
        async with ogranichitel:
            pass

    @pytest.mark.asyncio
    async def test_protokol_menedzhera_konteksta(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=10, period=60.0)
        async with ogranichitel as kontekst:
            assert kontekst is ogranichitel

    @pytest.mark.asyncio
    async def test_ochistka_udalyaet_starye_metki(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=2, period=0.05)
        seychas = time.monotonic()
        # Имитируем старые метки времени
        ogranichitel._metki_vremeni.append(seychas - 1.0)
        ogranichitel._metki_vremeni.append(seychas - 1.0)
        # Очистка должна удалить их, разрешив новые запросы
        async with ogranichitel:
            pass
        assert len(ogranichitel._metki_vremeni) == 1

    @pytest.mark.asyncio
    async def test_parallelnyy_dostup(self) -> None:
        ogranichitel = OgranichitelChastoty(maks_zaprosov=3, period=60.0)
        rezultaty: list[int] = []

        async def rabotnik(i: int) -> None:
            async with ogranichitel:
                rezultaty.append(i)

        await asyncio.gather(rabotnik(0), rabotnik(1), rabotnik(2))
        assert sorted(rezultaty) == [0, 1, 2]
