"""Пакетное выполнение нескольких инструментов за один вызов.

Формирует таблицу диспетчеризации, связывающую полные имена инструментов
с соответствующими функциями Python, затем выполняет их параллельно через asyncio.gather().
"""

from __future__ import annotations

import asyncio
import importlib
import inspect
import logging
import pkgutil
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    TipFunktsiiInstrumenta = Callable[..., Coroutine[Any, Any, str]]

    from mcp_russia._shared.feature import ReyestrFunktsiy

logger = logging.getLogger(__name__)

_dispetcher: dict[str, Any] = {}


def postroit_dispetcherizatsiyu(reyestr: ReyestrFunktsiy) -> dict[str, Any]:
    """Построение отображения полных имён инструментов → асинхронные функции.

    Сканирует модули tools.py всех зарегистрированных функций, включая
    вложенные подпакеты (напр., zakupki/sub-module).
    """
    global _dispetcher
    if _dispetcher:
        return _dispetcher

    for imya, feat in reyestr.funktsii.items():
        baza = feat.put_modulya
        _skanirovat_modul_instrumentov(baza, imya)

        # Подпакеты (напр., модуль данных с подфункциями)
        try:
            paket = importlib.import_module(baza)
            if hasattr(paket, "__path__"):
                for _, put_podmodulya, eto_paket in pkgutil.iter_modules(
                    paket.__path__, baza + "."
                ):
                    imya_podmodulya = put_podmodulya.rsplit(".", 1)[-1]
                    if eto_paket and not imya_podmodulya.startswith("_"):
                        _skanirovat_modul_instrumentov(put_podmodulya, f"{imya}_{imya_podmodulya}")
        except Exception:
            pass

    logger.info("Диспетчеризация пакета: зарегистрировано %d инструментов", len(_dispetcher))
    return _dispetcher


def _skanirovat_modul_instrumentov(put_modulya: str, namespace: str) -> None:
    """Импорт модуля инструментов и регистрация его асинхронных функций."""
    try:
        modul = importlib.import_module(f"{put_modulya}.tools")
    except ImportError:
        return

    for imya_fn, funktsiya in inspect.getmembers(modul, inspect.iscoroutinefunction):
        if not imya_fn.startswith("_"):
            klyuch = f"{namespace}_{imya_fn}"
            _dispetcher[klyuch] = funktsiya


async def vypolnit_paket_vnutrenniy(
    queries: list[dict[str, Any]],
    ctx: Any,
) -> str:
    """Параллельное выполнение нескольких вызовов инструментов.

    Аргументы:
        queries: Список словарей {"instrument": "имя", "argumenty": {}}.
        ctx: Контекст FastMCP для передачи в инструменты, которые его принимают.

    Возвращает:
        Отформатированный markdown со всеми результатами.
    """
    if not queries:
        return "Нет запросов для выполнения."

    if len(queries) > 10:
        return "Максимум 10 запросов на пакет. Уменьшите список."

    async def _vypolnit_odin(q: dict[str, Any]) -> tuple[str, str]:
        """Выполнение одного инструмента из пакета."""
        imya_instrumenta = q.get("instrument", "")
        args = q.get("argumenty", {})
        fn = _dispetcher.get(imya_instrumenta)

        if fn is None:
            return imya_instrumenta, f"Инструмент '{imya_instrumenta}' не найден."

        try:
            signatura = inspect.signature(fn)
            if "ctx" in signatura.parameters:
                rezultat = await fn(ctx=ctx, **args)
            else:
                rezultat = await fn(**args)
            return imya_instrumenta, rezultat
        except Exception as exc:
            return imya_instrumenta, f"Ошибка при выполнении '{imya_instrumenta}': {exc}"

    rezultaty = await asyncio.gather(*[_vypolnit_odin(q) for q in queries])

    chasti: list[str] = []
    for imya_instrumenta, vyvod in rezultaty:
        chasti.append(f"## {imya_instrumenta}\n\n{vyvod}")

    return "\n\n---\n\n".join(chasti)
