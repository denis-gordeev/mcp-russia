"""Валидаторы российских документов: ИНН, КПП, СНИЛС, почтовый индекс."""

from __future__ import annotations

import re

_DIGITS_RE = re.compile(r"\D")


def _only_digits(value: str) -> str:
    """Удаление всех нецифровых символов."""
    return _DIGITS_RE.sub("", value)


# ---------------------------------------------------------------------------
# ИНН (Идентификационный номер налогоплательщика)
# ---------------------------------------------------------------------------


def validate_inn(inn: str) -> bool:
    """Валидация российского ИНН (идентификационный номер налогоплательщика).

    Поддерживает форматы 10 цифр (юридические лица) и 12 цифр (физические лица).

    Args:
        inn: Строка ИНН (с форматированием или без).

    Returns:
        True если валиден, иначе False.
    """
    digits = _only_digits(inn)
    if len(digits) not in (10, 12):
        return False

    if len(digits) == 10:
        weights = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        total = sum(int(digits[i]) * weights[i] for i in range(9))
        remainder = total % 11
        check = remainder % 10
        return int(digits[9]) == check

    weights1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    weights2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    total1 = sum(int(digits[i]) * weights1[i] for i in range(10))
    remainder1 = total1 % 11
    check1 = remainder1 % 10
    if int(digits[10]) != check1:
        return False

    total2 = sum(int(digits[i]) * weights2[i] for i in range(11))
    remainder2 = total2 % 11
    check2 = remainder2 % 10
    return int(digits[11]) == check2


def format_inn(inn: str) -> str:
    """Форматирование ИНН для отображения.

    Args:
        inn: Цифры ИНН (с форматированием или без).

    Returns:
        Отформатированная строка ИНН.

    Raises:
        ValueError: Если ИНН не содержит 10 или 12 цифр.
    """
    digits = _only_digits(inn)
    if len(digits) == 10:
        return digits
    if len(digits) == 12:
        return digits
    raise ValueError(f"ИНН должен содержать 10 или 12 цифр, получено {len(digits)}")


# ---------------------------------------------------------------------------
# КПП (Код причины постановки на учёт)
# ---------------------------------------------------------------------------


def validate_kpp(kpp: str) -> bool:
    """Валидация российского КПП (код причины постановки на учёт).

    КПП — 9-значный код, используемый совместно с ИНН для юридических лиц.

    Args:
        kpp: Строка КПП (с форматированием или без).

    Returns:
        True если формат корректен, иначе False.
    """
    digits = _only_digits(kpp)
    if len(digits) != 9:
        return False
    return digits[:2] != "00"


def format_kpp(kpp: str) -> str:
    """Форматирование КПП для отображения.

    Args:
        kpp: Цифры КПП (с форматированием или без).

    Returns:
        Отформатированная строка КПП.

    Raises:
        ValueError: Если КПП не содержит ровно 9 цифр.
    """
    digits = _only_digits(kpp)
    if len(digits) != 9:
        raise ValueError(f"КПП должен содержать 9 цифр, получено {len(digits)}")
    return digits


# ---------------------------------------------------------------------------
# СНИЛС (Страховой номер индивидуального лицевого счёта)
# ---------------------------------------------------------------------------


def validate_snils(snils: str) -> bool:
    """Валидация российского СНИЛС (страховой номер индивидуального лицевого счёта).

    СНИЛС — 11-значное число (9 цифр + 2 контрольные цифры).

    Args:
        snils: Строка СНИЛС (с форматированием или без).

    Returns:
        True если валиден, иначе False.
    """
    digits = _only_digits(snils)
    if len(digits) != 11:
        return False

    total = 0
    for i in range(9):
        total += int(digits[i]) * (9 - i)

    if total < 100:
        check = total
    elif total in (100, 101):
        check = 0
    else:
        remainder = total % 101
        check = 0 if remainder == 100 else remainder

    check_str = f"{check:02d}"
    return digits[9:] == check_str


def format_snils(snils: str) -> str:
    """Форматирование СНИЛС в виде XXX-XXX-XXX XX.

    Args:
        snils: Цифры СНИЛС (с форматированием или без).

    Returns:
        Отформатированная строка СНИЛС.

    Raises:
        ValueError: Если СНИЛС не содержит ровно 11 цифр.
    """
    digits = _only_digits(snils)
    if len(digits) != 11:
        raise ValueError(f"СНИЛС должен содержать 11 цифр, получено {len(digits)}")
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:9]} {digits[9:]}"


# ---------------------------------------------------------------------------
# Почтовый индекс России
# ---------------------------------------------------------------------------


def validate_postal_code_ru(postal_code: str) -> bool:
    """Валидация российского почтового индекса (6 цифр).

    Args:
        postal_code: Строка почтового индекса (с форматированием или без).

    Returns:
        True если формат корректен, иначе False.
    """
    digits = _only_digits(postal_code)
    if len(digits) != 6:
        return False
    return digits[0] in "123456"


def format_postal_code_ru(postal_code: str) -> str:
    """Форматирование российского почтового индекса как XXXXXX.

    Args:
        postal_code: Цифры почтового индекса (с форматированием или без).

    Returns:
        Отформатированная строка почтового индекса.

    Raises:
        ValueError: Если почтовый индекс не содержит ровно 6 цифр.
    """
    digits = _only_digits(postal_code)
    if len(digits) != 6:
        raise ValueError(
            f"Российский почтовый индекс должен содержать 6 цифр, получено {len(digits)}"
        )
    return digits
