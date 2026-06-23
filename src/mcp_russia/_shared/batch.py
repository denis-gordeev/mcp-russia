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

    ToolFn = Callable[..., Coroutine[Any, Any, str]]

    from mcp_russia._shared.feature import FeatureRegistry

logger = logging.getLogger(__name__)

_dispatch: dict[str, Any] = {}


def postroit_dispetcherizatsiyu(registry: FeatureRegistry) -> dict[str, Any]:
    """Построение отображения полных имён инструментов → асинхронные функции.

    Сканирует модули tools.py всех зарегистрированных функций, включая
    вложенные подпакеты (напр., zakupki/sub-module).
    """
    global _dispatch
    if _dispatch:
        return _dispatch

    for name, feat in registry.features.items():
        base = feat.module_path
        _scan_tools_module(base, name)

        # Подпакеты (напр., модуль данных с подфункциями)
        try:
            pkg = importlib.import_module(base)
            if hasattr(pkg, "__path__"):
                for _, sub_path, is_pkg in pkgutil.iter_modules(pkg.__path__, base + "."):
                    sub_name = sub_path.rsplit(".", 1)[-1]
                    if is_pkg and not sub_name.startswith("_"):
                        _scan_tools_module(sub_path, f"{name}_{sub_name}")
        except Exception:
            pass

    logger.info("Диспетчеризация пакета: зарегистрировано %d инструментов", len(_dispatch))
    return _dispatch


def _scan_tools_module(module_path: str, namespace: str) -> None:
    """Импорт модуля инструментов и регистрация его асинхронных функций."""
    try:
        mod = importlib.import_module(f"{module_path}.tools")
    except ImportError:
        return

    for fn_name, fn in inspect.getmembers(mod, inspect.iscoroutinefunction):
        if not fn_name.startswith("_"):
            key = f"{namespace}_{fn_name}"
            _dispatch[key] = fn


async def vypolnit_paket_vnutrenniy(
    queries: list[dict[str, Any]],
    ctx: Any,
) -> str:
    """Параллельное выполнение нескольких вызовов инструментов.

    Аргументы:
        queries: Список словарей {"tool": "имя", "args": {}}.
        ctx: Контекст FastMCP для передачи в инструменты, которые его принимают.

    Возвращает:
        Отформатированный markdown со всеми результатами.
    """
    if not queries:
        return "Нет запросов для выполнения."

    if len(queries) > 10:
        return "Максимум 10 запросов на пакет. Уменьшите список."

    async def _run_one(q: dict[str, Any]) -> tuple[str, str]:
        """Выполнение одного инструмента из пакета."""
        tool_name = q.get("tool", "")
        args = q.get("args", {})
        fn = _dispatch.get(tool_name)

        if fn is None:
            return tool_name, f"Инструмент '{tool_name}' не найден."

        try:
            sig = inspect.signature(fn)
            if "ctx" in sig.parameters:
                result = await fn(ctx=ctx, **args)
            else:
                result = await fn(**args)
            return tool_name, result
        except Exception as exc:
            return tool_name, f"Ошибка при выполнении '{tool_name}': {exc}"

    results = await asyncio.gather(*[_run_one(q) for q in queries])

    parts: list[str] = []
    for tool_name, output in results:
        parts.append(f"## {tool_name}\n\n{output}")

    return "\n\n---\n\n".join(parts)
