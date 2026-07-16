"""Вспомогательные функции для форматирования текста в LLM-ориентированном виде.

Модуль предоставляет утилиты форматирования для российской локали (рубли,
русский формат чисел).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def tablitsa_v_markdown(zagolovki: Sequence[str], stroki_tablitsy: Sequence[Sequence[Any]]) -> str:
    """Рендеринг табличных данных в Markdown.

    Аргументы:
        zagolovki: Заголовки столбцов.
        stroki_tablitsy: Список строк (каждая строка — последовательность значений).

    Возвращает:
        Строка таблицы в формате Markdown.
    """
    if not stroki_tablitsy:
        return "Результаты не найдены."

    stroka_zagolovka = "| " + " | ".join(str(zagolovok) for zagolovok in zagolovki) + " |"
    razdelitel = "| " + " | ".join("---" for _ in zagolovki) + " |"
    stroki_tela = [
        "| " + " | ".join(str(znachenie_yacheyki) for znachenie_yacheyki in stroka) + " |"
        for stroka in stroki_tablitsy
    ]

    return "\n".join([stroka_zagolovka, razdelitel, *stroki_tela])


def formatirovat_rubli(znacheniye: float) -> str:
    """Форматирование числа в российском рублёвом стиле.

    Аргументы:
        znacheniye: Числовое значение.

    Возвращает:
        Отформатированная строка вида «1 234,56 ₽».
    """
    znak = "-" if znacheniye < 0 else ""
    abs_znacheniye = abs(znacheniye)
    tselaya_chast = int(abs_znacheniye)
    drobnaya_chast = round((abs_znacheniye - tselaya_chast) * 100)
    if drobnaya_chast >= 100:
        tselaya_chast += 1
        drobnaya_chast = 0
    stroka_tseloy = f"{tselaya_chast:,}".replace(",", " ")
    return f"{znak}{stroka_tseloy},{drobnaya_chast:02d} ₽"


def formatirovat_chislo_ru(znacheniye: float, desyatichnykh: int = 2) -> str:
    """Форматирование числа в российском стиле (пробел — тысячи, запятая — десятичные).

    Аргументы:
        znacheniye: Числовое значение.
        desyatichnykh: Количество десятичных знаков.

    Возвращает:
        Отформатированная строка вида «1 234,56».
    """
    otformatirovannoe = f"{znacheniye:,.{desyatichnykh}f}"
    return otformatirovannoe.replace(",", " ").replace(".", ",")


def formatirovat_protsent(znacheniye: float, desyatichnykh: int = 2) -> str:
    """Форматирование числового значения как процент.

    Аргументы:
        znacheniye: Числовое значение (напр. 0.05 для 5%).
        desyatichnykh: Количество десятичных знаков.

    Возвращает:
        Отформатированная строка вида «5,00%».
    """
    return f"{formatirovat_chislo_ru(znacheniye * 100, desyatichnykh)}%"


def razobrat_rublevoe_chislo(znacheniye: Any) -> float | None:
    """Разбор локализованной строки числа в число с плавающей точкой.

    Обрабатывает строки вида «1 234,56» (пробел=тысячи, запятая=десятичные)
    и «348.600,00» (точка=тысячи, запятая=десятичные) для обратной
    совместимости с устаревшими ответами API.
    Значения int/float пропускаются без изменений.

    Аргументы:
        znacheniye: Исходное значение из API (строка, int, float или None).

    Возвращает:
        Расобранное число float или None при невозможности разбора.
    """
    if znacheniye is None:
        return None
    if isinstance(znacheniye, (int, float)):
        return float(znacheniye)
    if isinstance(znacheniye, str):
        ochishchennoe = znacheniye.replace(" ", "")
        if "," in ochishchennoe and "." in ochishchennoe:
            ochishchennoe = ochishchennoe.replace(".", "").replace(",", ".")
        elif "," in ochishchennoe:
            ochishchennoe = ochishchennoe.replace(",", ".")
        try:
            return float(ochishchennoe)
        except ValueError:
            return None
    return None


def usech_spisok(elementy: Sequence[str], maks_elementov: int = 50) -> str:
    """Объединение элементов через перевод строки с усечением длинных списков.

    Аргументы:
        elementy: Список строк.
        maks_elementov: Максимальное количество элементов перед усечением.

    Возвращает:
        Объединённая строка с уведомлением об усечении при необходимости.
    """
    if len(elementy) <= maks_elementov:
        return "\n".join(elementy)

    pokazannye = elementy[:maks_elementov]
    ostalos = len(elementy) - maks_elementov
    return "\n".join(pokazannye) + f"\n\n... и ещё {ostalos} результатов."
