"""Асинхронный ограничитель частоты запросов со скользящим окном.

Использование::

    limiter = RateLimiter(max_requests=80, period=60.0)

    async with limiter:
        await do_request()
"""

from __future__ import annotations

import asyncio
import time
from collections import deque


class RateLimiter:
    """Ограничитель частоты запросов по принципу token bucket со скользящим окном.

    Args:
        max_requests: Максимальное число запросов в окне.
        period: Длительность окна в секундах.
    """

    def __init__(self, max_requests: int, period: float) -> None:
        self._max_requests = max_requests
        self._period = period
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    def _purge(self, now: float) -> None:
        """Удаление меток времени за пределами текущего окна."""
        cutoff = now - self._period
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

    async def acquire(self) -> None:
        """Ожидание доступного слота запроса и его резервирование."""
        while True:
            async with self._lock:
                now = time.monotonic()
                self._purge(now)
                if len(self._timestamps) < self._max_requests:
                    self._timestamps.append(now)
                    return
                # Расчёт времени ожидания до истечения самой старой записи
                wait = self._timestamps[0] + self._period - now
            await asyncio.sleep(max(wait, 0.01))

    async def __aenter__(self) -> RateLimiter:
        await self.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        pass
