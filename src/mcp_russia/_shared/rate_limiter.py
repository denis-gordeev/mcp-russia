"""Асинхронный ограничитель частоты запросов со скользящим окном.

Использование::

    ogranichitel = OgranichitelChastoty(maks_zaprosov=80, period=60.0)

    async with ogranichitel:
        await vypolnit_zapros()
"""

from __future__ import annotations

import asyncio
import time
from collections import deque


class OgranichitelChastoty:
    """Ограничитель частоты запросов по принципу ведра токенов со скользящим окном.

    Аргументы:
        maks_zaprosov: Максимальное число запросов в окне.
        period: Длительность окна в секундах.
    """

    def __init__(self, maks_zaprosov: int, period: float) -> None:
        """Инициализация ограничителя с заданными параметрами окна."""
        self._maks_zaprosov = maks_zaprosov
        self._period = period
        self._metki_vremeni: deque[float] = deque()
        self._zamok = asyncio.Lock()

    def _ochistit(self, seychas: float) -> None:
        """Удаление меток времени за пределами текущего окна."""
        porog = seychas - self._period
        while self._metki_vremeni and self._metki_vremeni[0] <= porog:
            self._metki_vremeni.popleft()

    async def zakhvatit(self) -> None:
        """Ожидание доступного слота запроса и его резервирование."""
        while True:
            async with self._zamok:
                seychas = time.monotonic()
                self._ochistit(seychas)
                if len(self._metki_vremeni) < self._maks_zaprosov:
                    self._metki_vremeni.append(seychas)
                    return
                # Расчёт времени ожидания до истечения самой старой записи
                ozhidanie = self._metki_vremeni[0] + self._period - seychas
            await asyncio.sleep(max(ozhidanie, 0.01))

    async def __aenter__(self) -> OgranichitelChastoty:
        """Вход в контекст: ожидание и резервирование слота."""
        await self.zakhvatit()
        return self

    async def __aexit__(self, *exc: object) -> None:
        """Выход из контекста: без освобождения слота (скользящее окно)."""
        pass
