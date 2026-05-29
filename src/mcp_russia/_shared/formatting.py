"""Вспомогательные функции для форматирования текста в LLM-ориентированном виде.

Модуль предоставляет утилиты форматирования для российской локали (рубли,
русский формат чисел) с обратной совместимостью для устаревших бразильских
форматов (BRL).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Render tabular data as Markdown.

    Args:
        headers: Column headers.
        rows: List of rows (each row is a sequence of values).

    Returns:
        Markdown-formatted table string.
    """
    if not rows:
        return "Результаты не найдены."

    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    body_lines = ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]

    return "\n".join([header_line, separator, *body_lines])


def format_rub(value: float) -> str:
    """Format a number using Russian RUB style.

    Args:
        value: Numeric value.

    Returns:
        Formatted string like "1 234,56 ₽".
    """
    sign = "-" if value < 0 else ""
    abs_value = abs(value)
    integer_part = int(abs_value)
    decimal_part = round((abs_value - integer_part) * 100)
    int_str = f"{integer_part:,}".replace(",", " ")
    return f"{sign}{int_str},{decimal_part:02d} ₽"


def format_brl(value: float) -> str:
    """Format a number using the Russian RUB style (deprecated alias for format_rub).

    .. deprecated:: Use format_rub instead.

    Args:
        value: Numeric value.

    Returns:
        Formatted string like "1 234,56 ₽".
    """
    return format_rub(value)


def format_number_ru(value: float, decimals: int = 2) -> str:
    """Format a number with Russian locale style (space thousands, comma decimal).

    Args:
        value: Numeric value.
        decimals: Number of decimal places.

    Returns:
        Formatted string like "1 234,56".
    """
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", " ").replace(".", ",")


def format_number_br(value: float, decimals: int = 2) -> str:
    """Format a number with Russian locale style (deprecated alias for format_number_ru).

    .. deprecated:: Use format_number_ru instead.

    Args:
        value: Numeric value.
        decimals: Number of decimal places.

    Returns:
        Formatted string like "1 234,56".
    """
    return format_number_ru(value, decimals)


def format_percent(value: float, decimals: int = 2) -> str:
    """Format a numeric ratio as percentage text.

    Args:
        value: Numeric value (e.g., 0.05 for 5%).

    Returns:
        Formatted string like "5,00%".
    """
    return f"{format_number_ru(value * 100, decimals)}%"


def parse_rub_number(value: Any) -> float | None:
    """Parse a locale-formatted number string into a float.

    Handles strings like "1 234,56" (space=thousands, comma=decimal)
    and "348.600,00" (dot=thousands, comma=decimal) for backward
    compatibility with legacy Brazilian API responses.
    Passes through int/float values unchanged.

    Args:
        value: Raw value from API (string, int, float, or None).

    Returns:
        Parsed float or None if unparseable.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace(" ", "")
        if "," in cleaned and "." in cleaned:
            cleaned = cleaned.replace(".", "").replace(",", ".")
        elif "," in cleaned:
            cleaned = cleaned.replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def parse_brl_number(value: Any) -> float | None:
    """Parse a locale-formatted number string into a float (deprecated alias for parse_rub_number).

    .. deprecated:: Use parse_rub_number instead.

    Args:
        value: Raw value from API (string, int, float, or None).

    Returns:
        Parsed float or None if unparseable.
    """
    return parse_rub_number(value)


def truncate_list(items: Sequence[str], max_items: int = 50) -> str:
    """Join items with newlines and truncate long lists.

    Args:
        items: List of strings.
        max_items: Maximum items to show before truncating.

    Returns:
        Joined string with truncation notice if needed.
    """
    if len(items) <= max_items:
        return "\n".join(items)

    shown = items[:max_items]
    remaining = len(items) - max_items
    return "\n".join(shown) + f"\n\n... и ещё {remaining} результатов."
