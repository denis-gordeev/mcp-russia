"""Простой потокобезопасный TTL-кэш для ответов API.

Предотвращает повторные идентичные запросы к государственным API.
Использует словарь в памяти с посерийным истечением срока — без внешних зависимостей.

Использование:
    from mcp_russia._shared.cache import ttl_cache

    cache = ttl_cache(ttl=300)  # 5 минут

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


class TTLCache:
    """Кэш в памяти с посерийным TTL-истечением.

    Потокобезопасен для asyncio (однопоточный цикл событий).
    Не подходит для многопроцессных развертываний — используйте Redis.
    """

    def __init__(self, ttl: float = 300.0, maxsize: int = 256) -> None:
        """Инициализация кэша с заданным TTL и максимальным размером."""
        self._ttl = ttl
        self._maxsize = maxsize
        self._store: dict[str, tuple[float, Any]] = {}

    @property
    def size(self) -> int:
        """Количество записей в кэше (включая просроченные)."""
        return len(self._store)

    def get(self, key: str) -> Any | None:
        """Получение значения, если оно существует и не истекло."""
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        """Сохранение значения с TTL-истечением."""
        if len(self._store) >= self._maxsize:
            self._evict()
        self._store[key] = (time.monotonic() + self._ttl, value)

    def clear(self) -> None:
        """Удаление всех записей."""
        self._store.clear()

    def _evict(self) -> None:
        """Удаление просроченных записей; если кэш полон — удаление самой старой."""
        now = time.monotonic()
        expired = [k for k, (exp, _) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]

        # Всё ещё полон? Удаляем запись с ближайшим истечением
        if len(self._store) >= self._maxsize:
            oldest_key = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest_key]


def ttl_cache(ttl: float = 300.0, maxsize: int = 256) -> Callable[[F], F]:
    """Декоратор кэширования результатов асинхронных функций с TTL.

    Ключ кэша строится из имени функции + строковых аргументов/kwargs.

    Аргументы:
        ttl: Время жизни в секундах. По умолчанию: 300 (5 минут).
        maxsize: Максимальное число записей в кэше. По умолчанию: 256.

    Возвращает:
        Декоратор, оборачивающий асинхронную функцию кэшированием.

    Example:
        @ttl_cache(ttl=60)
        async def poluchit_region() -> list[Region]:
            return await http_get(...)
    """
    cache = TTLCache(ttl=ttl, maxsize=maxsize)

    def decorator(func: F) -> F:
        """Обёртка функции с привязкой к кэшу."""

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Асинхронное выполнение с проверкой кэша перед вызовом."""
            key = f"{func.__qualname__}:{args!r}:{kwargs!r}"
            cached = cache.get(key)
            if cached is not None:
                return cached
            result = await func(*args, **kwargs)
            cache.set(key, result)
            return result

        # Доступ к кэшу для тестирования/очистки
        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator
