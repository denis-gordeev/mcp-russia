"""Общий асинхронный HTTP-клиент для mcp-russia.

Предоставляет фабрику httpx.AsyncClient и функцию запроса с
повторными попытками и экспоненциальной задержкой для transient-ошибок (5xx, 429, таймауты).

Использование:
    from mcp_russia._shared.http_client import sozdat_klienta, http_poluchit

    # Вариант 1: фабрика клиентов (для нескольких запросов в клиенте модуля)
    async with sozdat_klienta(bazovyy_adres_url="https://api.example.com") as klient:
        otvet = await klient.get("/endpoint")

    # Вариант 2: разовый запрос с автоматическими повторными попытками
    dannye = await http_poluchit("https://api.example.com/endpoint")
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from mcp_russia.exceptions import OshibkaHttpClienta
from mcp_russia.settings import (
    BAZA_EKSPON_ZADERZH,
    MAKS_POVTOROV_HTTP,
    POLZOVATELSKIY_AGENT,
    TAIMAUT_HTTP,
)

logger = logging.getLogger(__name__)

# Коды состояния, инициирующие повторную попытку
_KODY_STATUSOV_DLYA_POVTORA = frozenset({429, 500, 502, 503, 504})


def sozdat_klienta(
    bazovyy_adres_url: str = "",
    taimaut: float | None = None,
    zagolovki: dict[str, str] | None = None,
) -> httpx.AsyncClient:
    """Создание настроенного httpx.AsyncClient.

    Аргументы:
        bazovyy_adres_url: Базовый URL для всех запросов.
        taimaut: Таймаут запроса в секундах. По умолчанию: settings.TAIMAUT_HTTP.
        zagolovki: Дополнительные заголовки для слияния с заголовками по умолчанию.

    Возвращает:
        Настроенный httpx.AsyncClient (использовать как async context manager).
    """
    zagolovki_po_umolchaniyu = {
        "User-Agent": POLZOVATELSKIY_AGENT,
        "Accept": "application/json",
    }
    if zagolovki:
        zagolovki_po_umolchaniyu.update(zagolovki)

    return httpx.AsyncClient(
        base_url=bazovyy_adres_url,
        timeout=httpx.Timeout(taimaut or TAIMAUT_HTTP),
        headers=zagolovki_po_umolchaniyu,
        follow_redirects=True,
    )


async def http_poluchit(
    adres_url: str,
    *,
    parametry: dict[str, Any] | None = None,
    zagolovki: dict[str, str] | None = None,
    taimaut: float | None = None,
    maks_povtorov: int | None = None,
) -> Any:
    """Выполнение GET-запроса с повторными попытками и экспоненциальной задержкой.

    Повторяет при: HTTP 429/5xx, таймаутах и ошибках соединения.
    НЕ повторяет при 4xx (кроме 429) — это клиентские ошибки.

    Аргументы:
        adres_url: Полный URL для запроса.
        parametry: Параметры запроса.
        zagolovki: Дополнительные заголовки (сливаются с заголовками по умолчанию).
        taimaut: Таймаут запроса в секундах.
        maks_povtorov: Максимальное число попыток. По умолчанию: settings.MAKS_POVTOROV_HTTP.

    Возвращает:
        Разобранный JSON-ответ.

    Вызывает:
        OshibkaHttpClienta: При неповторяемых ошибках или исчерпании попыток.
    """
    povtory = maks_povtorov if maks_povtorov is not None else MAKS_POVTOROV_HTTP
    poslednyaya_oshibka: Exception | None = None

    async with sozdat_klienta(taimaut=taimaut, zagolovki=zagolovki) as klient:
        for popytka in range(povtory + 1):
            try:
                otvet = await klient.get(adres_url, params=parametry)

                if otvet.status_code in _KODY_STATUSOV_DLYA_POVTORA:
                    if popytka < povtory:
                        ozhidanie = BAZA_EKSPON_ZADERZH * (2**popytka)
                        logger.warning(
                            "Повтор %d/%d для %s (HTTP %d), ожидание %.1fс",
                            popytka + 1,
                            povtory,
                            adres_url,
                            otvet.status_code,
                            ozhidanie,
                        )
                        await asyncio.sleep(ozhidanie)
                        continue
                    raise OshibkaHttpClienta(
                        f"Запрос к {adres_url} не удался после {povtory + 1} попыток "
                        f"(последняя: HTTP {otvet.status_code})"
                    )

                otvet.raise_for_status()
                return otvet.json()

            except httpx.HTTPStatusError as exc:
                raise OshibkaHttpClienta(
                    f"HTTP {exc.response.status_code} от {adres_url}: {exc.response.text[:200]}"
                ) from exc

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                poslednyaya_oshibka = exc
                if popytka < povtory:
                    ozhidanie = BAZA_EKSPON_ZADERZH * (2**popytka)
                    logger.warning(
                        "Запрос к %s не удался (попытка %d/%d): %s, ожидание %.1fс",
                        adres_url,
                        popytka + 1,
                        povtory,
                        type(exc).__name__,
                        ozhidanie,
                    )
                    await asyncio.sleep(ozhidanie)
                    continue

    raise OshibkaHttpClienta(
        f"Запрос к {adres_url} не удался после {povtory + 1} попыток"
    ) from poslednyaya_oshibka


async def http_otpravit(
    adres_url: str,
    *,
    telo_json: Any | None = None,
    parametry: dict[str, Any] | None = None,
    zagolovki: dict[str, str] | None = None,
    taimaut: float | None = None,
    maks_povtorov: int | None = None,
) -> Any:
    """Выполнение POST-запроса с повторными попытками и экспоненциальной задержкой.

    Повторяет при: HTTP 429/5xx, таймаутах и ошибках соединения.

    Аргументы:
        adres_url: Полный URL для запроса.
        telo_json: JSON-тело для отправки.
        parametry: Параметры запроса.
        zagolovki: Дополнительные заголовки (сливаются с заголовками по умолчанию).
        taimaut: Таймаут запроса в секундах.
        maks_povtorov: Максимальное число попыток. По умолчанию: settings.MAKS_POVTOROV_HTTP.

    Возвращает:
        Разобранный JSON-ответ.

    Вызывает:
        OshibkaHttpClienta: При неповторяемых ошибках или исчерпании попыток.
    """
    povtory = maks_povtorov if maks_povtorov is not None else MAKS_POVTOROV_HTTP
    poslednyaya_oshibka: Exception | None = None

    async with sozdat_klienta(taimaut=taimaut, zagolovki=zagolovki) as klient:
        for popytka in range(povtory + 1):
            try:
                otvet = await klient.post(adres_url, json=telo_json, params=parametry)

                if otvet.status_code in _KODY_STATUSOV_DLYA_POVTORA:
                    if popytka < povtory:
                        ozhidanie = BAZA_EKSPON_ZADERZH * (2**popytka)
                        logger.warning(
                            "Повтор %d/%d для %s (HTTP %d), ожидание %.1fс",
                            popytka + 1,
                            povtory,
                            adres_url,
                            otvet.status_code,
                            ozhidanie,
                        )
                        await asyncio.sleep(ozhidanie)
                        continue
                    raise OshibkaHttpClienta(
                        f"Запрос к {adres_url} не удался после {povtory + 1} попыток "
                        f"(последняя: HTTP {otvet.status_code})"
                    )

                otvet.raise_for_status()
                return otvet.json()

            except httpx.HTTPStatusError as exc:
                raise OshibkaHttpClienta(
                    f"HTTP {exc.response.status_code} от {adres_url}: {exc.response.text[:200]}"
                ) from exc

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                poslednyaya_oshibka = exc
                if popytka < povtory:
                    ozhidanie = BAZA_EKSPON_ZADERZH * (2**popytka)
                    logger.warning(
                        "Запрос к %s не удался (попытка %d/%d): %s, ожидание %.1fс",
                        adres_url,
                        popytka + 1,
                        povtory,
                        type(exc).__name__,
                        ozhidanie,
                    )
                    await asyncio.sleep(ozhidanie)
                    continue

    raise OshibkaHttpClienta(
        f"Запрос к {adres_url} не удался после {povtory + 1} попыток"
    ) from poslednyaya_oshibka
