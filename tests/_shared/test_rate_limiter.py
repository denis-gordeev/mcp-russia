"""Тесты асинхронного ограничителя запросов (OgranichitelChastoty)."""

from __future__ import annotations

import asyncio
import time

import pytest

from mcp_russia._shared.rate_limiter import OgranichitelChastoty


class TestOgranichitelChastoty:
    @pytest.mark.asyncio
    async def test_allows_within_limit(self) -> None:
        limiter = OgranichitelChastoty(max_requests=5, period=60.0)
        for _ in range(5):
            async with limiter:
                pass
        # Все 5 должны пройти без блокировки

    @pytest.mark.asyncio
    async def test_blocks_when_exhausted(self) -> None:
        limiter = OgranichitelChastoty(max_requests=2, period=60.0)
        async with limiter:
            pass
        async with limiter:
            pass

        # Третий запрос должен блокироваться; проверяем с коротким таймаутом
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(limiter.zakhvatit(), timeout=0.05)

    @pytest.mark.asyncio
    async def test_allows_after_window_expires(self) -> None:
        limiter = OgranichitelChastoty(max_requests=1, period=0.05)
        async with limiter:
            pass
        # Ждём истечения окна
        await asyncio.sleep(0.06)
        # Теперь должен быть разрешён
        async with limiter:
            pass

    @pytest.mark.asyncio
    async def test_context_manager_protocol(self) -> None:
        limiter = OgranichitelChastoty(max_requests=10, period=60.0)
        async with limiter as ctx:
            assert ctx is limiter

    @pytest.mark.asyncio
    async def test_purge_removes_old_timestamps(self) -> None:
        limiter = OgranichitelChastoty(max_requests=2, period=0.05)
        now = time.monotonic()
        # Имитируем старые метки времени
        limiter._timestamps.append(now - 1.0)
        limiter._timestamps.append(now - 1.0)
        # Очистка должна удалить их, разрешив новые запросы
        async with limiter:
            pass
        assert len(limiter._timestamps) == 1

    @pytest.mark.asyncio
    async def test_concurrent_access(self) -> None:
        limiter = OgranichitelChastoty(max_requests=3, period=60.0)
        results: list[int] = []

        async def worker(i: int) -> None:
            async with limiter:
                results.append(i)

        await asyncio.gather(worker(0), worker(1), worker(2))
        assert sorted(results) == [0, 1, 2]
