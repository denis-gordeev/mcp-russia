"""Простой потокобезопасный TTL-кэш для ответов API.

Предотвращает повторные идентичные запросы к государственным API.
Использует словарь в памяти с посерийным истечением срока — без внешних зависимостей.

Использование:
    from mcp_russia._shared.cache import kesh_s_vremenem_zhizni

    cache = kesh_s_vremenem_zhizni(ttl=300)  # 5 минут

    @cache
    async def spisok_regionov() -> list[Region]:
        ...  # HTTP-запрос выполняется только при промахе кэша или истечении срока
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class KeshSVremenemZhizni:
    """Кэш в памяти с посерийным TTL-истечением.

    Потокобезопасен для asyncio (однопоточный цикл событий).
    Не подходит для многопроцессных развертываний — используйте Redis.
    """

    def __init__(self, vremya_zhizni: float = 300.0, maks_razmer: int = 256) -> None:
        """Инициализация кэша с заданным TTL и максимальным размером."""
        self._vremya_zhizni = vremya_zhizni
        self._maks_razmer = maks_razmer
        self._khranilishche: dict[str, tuple[float, Any]] = {}

    @property
    def razmer(self) -> int:
        """Количество записей в кэше (включая просроченные)."""
        return len(self._khranilishche)

    def poluchit(self, klyuch: str) -> Any | None:
        """Получение значения, если оно существует и не истекло."""
        zapis = self._khranilishche.get(klyuch)
        if zapis is None:
            return None
        istekaet_v, znachenie = zapis
        if time.monotonic() > istekaet_v:
            del self._khranilishche[klyuch]
            return None
        return znachenie

    def ustanovit(self, klyuch: str, znachenie: Any) -> None:
        """Сохранение значения с TTL-истечением."""
        if len(self._khranilishche) >= self._maks_razmer:
            self._ischislit()
        self._khranilishche[klyuch] = (time.monotonic() + self._vremya_zhizni, znachenie)

    def ochistit(self) -> None:
        """Удаление всех записей."""
        self._khranilishche.clear()

    def _ischislit(self) -> None:
        """Удаление просроченных записей; если кэш полон — удаление самой старой."""
        seychas = time.monotonic()
        istekshie = [
            klyuch for klyuch, (istekaet, _) in self._khranilishche.items() if seychas > istekaet
        ]
        for klyuch in istekshie:
            del self._khranilishche[klyuch]

        # Всё ещё полон? Удаляем запись с ближайшим истечением
        if len(self._khranilishche) >= self._maks_razmer:
            samyy_staryy_klyuch = min(
                self._khranilishche,
                key=lambda klyuch: self._khranilishche[klyuch][0],
            )
            del self._khranilishche[samyy_staryy_klyuch]


def kesh_s_vremenem_zhizni(
    vremya_zhizni: float = 300.0, maks_razmer: int = 256
) -> Callable[[F], F]:
    """Декоратор кэширования результатов асинхронных функций с TTL.

    Ключ кэша строится из имени функции + строковых аргументов/kwargs.

    Аргументы:
        vremya_zhizni: Время жизни в секундах. По умолчанию: 300 (5 минут).
        maks_razmer: Максимальное число записей в кэше. По умолчанию: 256.

    Возвращает:
        Декоратор, оборачивающий асинхронную функцию кэшированием.

    Пример:
        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit_region() -> list[Region]:
            return await http_poluchit(...)
    """
    kesh = KeshSVremenemZhizni(vremya_zhizni=vremya_zhizni, maks_razmer=maks_razmer)

    def dekorator(funktsiya: F) -> F:
        """Обёртка функции с привязкой к кэшу."""

        @functools.wraps(funktsiya)
        async def obertka(*args: Any, **kwargs: Any) -> Any:
            """Асинхронное выполнение с проверкой кэша перед вызовом."""
            klyuch = f"{funktsiya.__qualname__}:{args!r}:{kwargs!r}"
            zakeshirovano = kesh.poluchit(klyuch)
            if zakeshirovano is not None:
                return zakeshirovano
            rezultat = await funktsiya(*args, **kwargs)
            kesh.ustanovit(klyuch, rezultat)
            return rezultat

        # Доступ к кэшу для тестирования/очистки
        obertka.kesh = kesh  # type: ignore[attr-defined]
        return obertka  # type: ignore[return-value]

    return dekorator
