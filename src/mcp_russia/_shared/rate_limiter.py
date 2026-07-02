"""Асинхронный ограничитель частоты запросов со скользящим окном.

Использование::

    limiter = OgranichitelChastoty(maks_zaprosov=80, period=60.0)

    async with limiter:
        await do_request()
"""

from __future__ import annotations

import asyncio
import time
from collections import deque


class OgranichitelChastoty:
    """Ограничитель частоты запросов по принципу token bucket со скользящим окном.

    Аргументы:
        maks_zaprosov: Максимальное число запросов в окне.
        period: Длительность окна в секундах.
    """

    def __init__(self, maks_zaprosov: int, period: float) -> None:
        """Инициализация ограничителя с заданными параметрами окна."""
        self._maks_zaprosov = maks_zaprosov
        self._period = period
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    def _ochistit(self, seychas: float) -> None:
        """Удаление меток времени за пределами текущего окна."""
        porog = seychas - self._period
        while self._timestamps and self._timestamps[0] <= porog:
            self._timestamps.popleft()

    async def zakhvatit(self) -> None:
        """Ожидание доступного слота запроса и его резервирование."""
        while True:
            async with self._lock:
                seychas = time.monotonic()
                self._ochistit(seychas)
                if len(self._timestamps) < self._maks_zaprosov:
                    self._timestamps.append(seychas)
                    return
                # Расчёт времени ожидания до истечения самой старой записи
                ozhidanie = self._timestamps[0] + self._period - seychas
            await asyncio.sleep(max(ozhidanie, 0.01))

    async def __aenter__(self) -> OgranichitelChastoty:
        """Вход в контекст: ожидание и резервирование слота."""
        await self.zakhvatit()
        return self

    async def __aexit__(self, *exc: object) -> None:
        """Выход из контекста: без освобождения слота (скользящее окно)."""
        pass
