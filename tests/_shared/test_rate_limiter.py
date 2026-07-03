"""Тесты асинхронного ограничителя запросов (OgranichitelChastoty)."""

from __future__ import annotations

import asyncio
import time

import pytest

from mcp_russia._shared.rate_limiter import OgranichitelChastoty


class TestOgranichitelChastoty:
    @pytest.mark.asyncio
    async def test_propuskaet_v_predelakh_limita(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=5, period=60.0)
        for _ in range(5):
            async with limiter:
                pass
        # Все 5 должны пройти без блокировки

    @pytest.mark.asyncio
    async def test_blokiruet_pri_ischerpanii(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=2, period=60.0)
        async with limiter:
            pass
        async with limiter:
            pass

        # Третий запрос должен блокироваться; проверяем с коротким таймаутом
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(limiter.zakhvatit(), timeout=0.05)

    @pytest.mark.asyncio
    async def test_propuskaet_posle_istecheniya_okna(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=1, period=0.05)
        async with limiter:
            pass
        # Ждём истечения окна
        await asyncio.sleep(0.06)
        # Теперь должен быть разрешён
        async with limiter:
            pass

    @pytest.mark.asyncio
    async def test_protokol_menedzhera_konteksta(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=10, period=60.0)
        async with limiter as ctx:
            assert ctx is limiter

    @pytest.mark.asyncio
    async def test_ochistka_udalyaet_starye_metki(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=2, period=0.05)
        now = time.monotonic()
        # Имитируем старые метки времени
        limiter._timestamps.append(now - 1.0)
        limiter._timestamps.append(now - 1.0)
        # Очистка должна удалить их, разрешив новые запросы
        async with limiter:
            pass
        assert len(limiter._timestamps) == 1

    @pytest.mark.asyncio
    async def test_parallelnyy_dostup(self) -> None:
        limiter = OgranichitelChastoty(maks_zaprosov=3, period=60.0)
        rezultaty: list[int] = []

        async def worker(i: int) -> None:
            async with limiter:
                rezultaty.append(i)

        await asyncio.gather(worker(0), worker(1), worker(2))
        assert sorted(rezultaty) == [0, 1, 2]
