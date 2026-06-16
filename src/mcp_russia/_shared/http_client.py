"""Общий асинхронный HTTP-клиент для mcp-russia.

Предоставляет фабрику httpx.AsyncClient и функцию запроса с
повторными попытками и экспоненциальной задержкой для transient-ошибок (5xx, 429, таймауты).

Использование:
    from mcp_russia._shared.http_client import create_client, http_get

    # Вариант 1: фабрика клиентов (для нескольких запросов в клиенте модуля)
    async with create_client(base_url="https://api.example.com") as client:
        response = await client.get("/endpoint")

    # Вариант 2: разовый запрос с автоматическими повторными попытками
    data = await http_get("https://api.example.com/endpoint")
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from mcp_russia.exceptions import HttpClientError
from mcp_russia.settings import HTTP_BACKOFF_BASE, HTTP_MAX_RETRIES, HTTP_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)

# Коды состояния, инициирующие повторную попытку
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def create_client(
    base_url: str = "",
    timeout: float | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.AsyncClient:
    """Создание настроенного httpx.AsyncClient.

    Аргументы:
        base_url: Базовый URL для всех запросов.
        timeout: Таймаут запроса в секундах. По умолчанию: settings.HTTP_TIMEOUT.
        headers: Дополнительные заголовки для слияния с заголовками по умолчанию.

    Возвращает:
        Настроенный httpx.AsyncClient (использовать как async context manager).
    """
    default_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if headers:
        default_headers.update(headers)

    return httpx.AsyncClient(
        base_url=base_url,
        timeout=httpx.Timeout(timeout or HTTP_TIMEOUT),
        headers=default_headers,
        follow_redirects=True,
    )


async def http_get(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
    max_retries: int | None = None,
) -> Any:
    """Выполнение GET-запроса с повторными попытками и экспоненциальной задержкой.

    Повторяет при: HTTP 429/5xx, таймаутах и ошибках соединения.
    НЕ повторяет при 4xx (кроме 429) — это клиентские ошибки.

    Аргументы:
        url: Полный URL для запроса.
        params: Параметры запроса.
        headers: Дополнительные заголовки (сливаются с заголовками по умолчанию).
        timeout: Таймаут запроса в секундах.
        max_retries: Максимальное число попыток. По умолчанию: settings.HTTP_MAX_RETRIES.

    Возвращает:
        Разобранный JSON-ответ.

    Вызывает:
        HttpClientError: При неповторяемых ошибках или исчерпании попыток.
    """
    retries = max_retries if max_retries is not None else HTTP_MAX_RETRIES
    last_error: Exception | None = None

    async with create_client(timeout=timeout, headers=headers) as client:
        for attempt in range(retries + 1):
            try:
                response = await client.get(url, params=params)

                if response.status_code in _RETRYABLE_STATUS_CODES:
                    if attempt < retries:
                        wait = HTTP_BACKOFF_BASE * (2**attempt)
                        logger.warning(
                            "Повтор %d/%d для %s (HTTP %d), ожидание %.1fс",
                            attempt + 1,
                            retries,
                            url,
                            response.status_code,
                            wait,
                        )
                        await asyncio.sleep(wait)
                        continue
                    # Последняя попытка завершилась повторяемой ошибкой
                    raise HttpClientError(
                        f"Запрос к {url} не удался после {retries + 1} попыток "
                        f"(последняя: HTTP {response.status_code})"
                    )

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as exc:
                raise HttpClientError(
                    f"HTTP {exc.response.status_code} от {url}: {exc.response.text[:200]}"
                ) from exc

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                last_error = exc
                if attempt < retries:
                    wait = HTTP_BACKOFF_BASE * (2**attempt)
                    logger.warning(
                        "Запрос к %s не удался (попытка %d/%d): %s, ожидание %.1fс",
                        url,
                        attempt + 1,
                        retries,
                        type(exc).__name__,
                        wait,
                    )
                    await asyncio.sleep(wait)
                    continue

    raise HttpClientError(f"Запрос к {url} не удался после {retries + 1} попыток") from last_error


async def http_post(
    url: str,
    *,
    json_body: Any | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
    max_retries: int | None = None,
) -> Any:
    """Выполнение POST-запроса с повторными попытками и экспоненциальной задержкой.

    Повторяет при: HTTP 429/5xx, таймаутах и ошибках соединения.

    Аргументы:
        url: Полный URL для запроса.
        json_body: JSON-тело для отправки.
        params: Параметры запроса.
        headers: Дополнительные заголовки (сливаются с заголовками по умолчанию).
        timeout: Таймаут запроса в секундах.
        max_retries: Максимальное число попыток. По умолчанию: settings.HTTP_MAX_RETRIES.

    Возвращает:
        Разобранный JSON-ответ.

    Вызывает:
        HttpClientError: При неповторяемых ошибках или исчерпании попыток.
    """
    retries = max_retries if max_retries is not None else HTTP_MAX_RETRIES
    last_error: Exception | None = None

    async with create_client(timeout=timeout, headers=headers) as client:
        for attempt in range(retries + 1):
            try:
                response = await client.post(url, json=json_body, params=params)

                if response.status_code in _RETRYABLE_STATUS_CODES:
                    if attempt < retries:
                        wait = HTTP_BACKOFF_BASE * (2**attempt)
                        logger.warning(
                            "Повтор %d/%d для %s (HTTP %d), ожидание %.1fс",
                            attempt + 1,
                            retries,
                            url,
                            response.status_code,
                            wait,
                        )
                        await asyncio.sleep(wait)
                        continue
                    raise HttpClientError(
                        f"Запрос к {url} не удался после {retries + 1} попыток "
                        f"(последняя: HTTP {response.status_code})"
                    )

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as exc:
                raise HttpClientError(
                    f"HTTP {exc.response.status_code} от {url}: {exc.response.text[:200]}"
                ) from exc

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                last_error = exc
                if attempt < retries:
                    wait = HTTP_BACKOFF_BASE * (2**attempt)
                    logger.warning(
                        "Запрос к %s не удался (попытка %d/%d): %s, ожидание %.1fс",
                        url,
                        attempt + 1,
                        retries,
                        type(exc).__name__,
                        wait,
                    )
                    await asyncio.sleep(wait)
                    continue

    raise HttpClientError(f"Запрос к {url} не удался после {retries + 1} попыток") from last_error
