"""Вспомогательные функции для форматирования текста в LLM-ориентированном виде.

Модуль предоставляет утилиты форматирования для российской локали (рубли,
русский формат чисел).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def tablitsa_v_markdown(headers: Sequence[str], stroki_tablitsy: Sequence[Sequence[Any]]) -> str:
    """Рендеринг табличных данных в Markdown.

    Аргументы:
        headers: Заголовки столбцов.
        rows: Список строк (каждая строка — последовательность значений).

    Возвращает:
        Строка таблицы в формате Markdown.
    """
    if not stroki_tablitsy:
        return "Результаты не найдены."

    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    body_lines = ["| " + " | ".join(str(v) for v in row) + " |" for row in stroki_tablitsy]

    return "\n".join([header_line, separator, *body_lines])


def formatirovat_rubli(value: float) -> str:
    """Форматирование числа в российском рублёвом стиле.

    Аргументы:
        value: Числовое значение.

    Возвращает:
        Отформатированная строка вида «1 234,56 ₽».
    """
    sign = "-" if value < 0 else ""
    abs_value = abs(value)
    integer_part = int(abs_value)
    decimal_part = round((abs_value - integer_part) * 100)
    if decimal_part >= 100:
        integer_part += 1
        decimal_part = 0
    int_str = f"{integer_part:,}".replace(",", " ")
    return f"{sign}{int_str},{decimal_part:02d} ₽"


def formatirovat_chislo_ru(value: float, decimals: int = 2) -> str:
    """Форматирование числа в российском стиле (пробел — тысячи, запятая — десятичные).

    Аргументы:
        value: Числовое значение.
        decimals: Количество десятичных знаков.

    Возвращает:
        Отформатированная строка вида «1 234,56».
    """
    otformatirovannoe = f"{value:,.{decimals}f}"
    return otformatirovannoe.replace(",", " ").replace(".", ",")


def formatirovat_protsent(value: float, decimals: int = 2) -> str:
    """Форматирование числового значения как процент.

    Аргументы:
        value: Числовое значение (напр. 0.05 для 5%).
        decimals: Количество десятичных знаков.

    Возвращает:
        Отформатированная строка вида «5,00%».
    """
    return f"{formatirovat_chislo_ru(value * 100, decimals)}%"


def razobrat_rublevoe_chislo(value: Any) -> float | None:
    """Разбор локализованной строки числа в число с плавающей точкой.

    Обрабатывает строки вида «1 234,56» (пробел=тысячи, запятая=десятичные)
    и «348.600,00» (точка=тысячи, запятая=десятичные) для обратной
    совместимости с устаревшими ответами API.
    Значения int/float пропускаются без изменений.

    Аргументы:
        value: Исходное значение из API (строка, int, float или None).

    Возвращает:
        Расобранное число float или None при невозможности разбора.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        ochishchennoe = value.replace(" ", "")
        if "," in ochishchennoe and "." in ochishchennoe:
            ochishchennoe = ochishchennoe.replace(".", "").replace(",", ".")
        elif "," in ochishchennoe:
            ochishchennoe = ochishchennoe.replace(",", ".")
        try:
            return float(ochishchennoe)
        except ValueError:
            return None
    return None


def usech_spisok(elementy: Sequence[str], max_items: int = 50) -> str:
    """Объединение элементов через перевод строки с усечением длинных списков.

    Аргументы:
        items: Список строк.
        max_items: Максимальное количество элементов перед усечением.

    Возвращает:
        Объединённая строка с уведомлением об усечении при необходимости.
    """
    if len(elementy) <= max_items:
        return "\n".join(elementy)

    shown = elementy[:max_items]
    remaining = len(elementy) - max_items
    return "\n".join(shown) + f"\n\n... и ещё {remaining} результатов."
