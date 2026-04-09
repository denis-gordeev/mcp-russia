"""Validators for Russian and Brazilian documents: INN, KPP, SNILS, postal code.

This module provides validators for Russian identification documents
(INN, KPP, SNILS) and postal codes, with backward-compatible aliases
for legacy Brazilian validators (CPF, CNPJ, CEP).
"""

from __future__ import annotations

import re

_DIGITS_RE = re.compile(r"\D")


def _only_digits(value: str) -> str:
    """Strip all non-digit characters."""
    return _DIGITS_RE.sub("", value)


# ---------------------------------------------------------------------------
# INN (Идентификационный номер налогоплательщика)
# ---------------------------------------------------------------------------


def validate_inn(inn: str) -> bool:
    """Validate a Russian INN (taxpayer identification number).

    Supports both 10-digit (legal entities) and 12-digit (individuals) formats.

    Args:
        inn: INN string (with or without formatting).

    Returns:
        True if valid, False otherwise.
    """
    digits = _only_digits(inn)
    if len(digits) not in (10, 12):
        return False

    if len(digits) == 10:
        # 10-digit INN (legal entity)
        weights = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        total = sum(int(digits[i]) * weights[i] for i in range(9))
        remainder = total % 11
        check = remainder % 10
        return int(digits[9]) == check

    # 12-digit INN (individual)
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
    """Format an INN string for display.

    Args:
        inn: INN digits (with or without formatting).

    Returns:
        Formatted INN string.

    Raises:
        ValueError: If INN does not have 10 or 12 digits.
    """
    digits = _only_digits(inn)
    if len(digits) == 10:
        return digits
    if len(digits) == 12:
        return digits
    raise ValueError(f"INN must have 10 or 12 digits, got {len(digits)}")


# ---------------------------------------------------------------------------
# KPP (Код причины постановки на учёт)
# ---------------------------------------------------------------------------


def validate_kpp(kpp: str) -> bool:
    """Validate a Russian KPP (tax registration reason code).

    KPP is a 9-digit code used alongside INN for legal entities.

    Args:
        kpp: KPP string (with or without formatting).

    Returns:
        True if valid format, False otherwise.
    """
    digits = _only_digits(kpp)
    if len(digits) != 9:
        return False
    # First two digits cannot be 00
    return digits[:2] != "00"


def format_kpp(kpp: str) -> str:
    """Format a KPP string for display.

    Args:
        kpp: KPP digits (with or without formatting).

    Returns:
        Formatted KPP string.

    Raises:
        ValueError: If KPP does not have exactly 9 digits.
    """
    digits = _only_digits(kpp)
    if len(digits) != 9:
        raise ValueError(f"KPP must have 9 digits, got {len(digits)}")
    return digits


# ---------------------------------------------------------------------------
# SNILS (Страховой номер индивидуального лицевого счёта)
# ---------------------------------------------------------------------------


def validate_snils(snils: str) -> bool:
    """Validate a Russian SNILS (individual insurance account number).

    SNILS is an 11-digit number (9 digits + 2 check digits).

    Args:
        snils: SNILS string (with or without formatting).

    Returns:
        True if valid, False otherwise.
    """
    digits = _only_digits(snils)
    if len(digits) != 11:
        return False

    # Calculate check digits
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
    """Format a SNILS string as XXX-XXX-XXX XX.

    Args:
        snils: SNILS digits (with or without formatting).

    Returns:
        Formatted SNILS string.

    Raises:
        ValueError: If SNILS does not have exactly 11 digits.
    """
    digits = _only_digits(snils)
    if len(digits) != 11:
        raise ValueError(f"SNILS must have 11 digits, got {len(digits)}")
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:9]} {digits[9:]}"


# ---------------------------------------------------------------------------
# Russian postal code
# ---------------------------------------------------------------------------


def validate_postal_code_ru(postal_code: str) -> bool:
    """Validate a Russian postal code (6 digits).

    Args:
        postal_code: Postal code string (with or without formatting).

    Returns:
        True if valid format, False otherwise.
    """
    digits = _only_digits(postal_code)
    if len(digits) != 6:
        return False
    # First digit should be 1-6 (valid range for Russia)
    return digits[0] in "123456"


def format_postal_code_ru(postal_code: str) -> str:
    """Format a Russian postal code as XXXXXX.

    Args:
        postal_code: Postal code digits (with or without formatting).

    Returns:
        Formatted postal code string.

    Raises:
        ValueError: If postal code does not have exactly 6 digits.
    """
    digits = _only_digits(postal_code)
    if len(digits) != 6:
        raise ValueError(f"Russian postal code must have 6 digits, got {len(digits)}")
    return digits


# ---------------------------------------------------------------------------
# Legacy Brazilian aliases (backward compatibility)
# ---------------------------------------------------------------------------
# These are preserved for backward compatibility during migration.
# Brazilian CPF, CNPJ, CEP validators are kept as thin wrappers.


def validate_cpf(cpf: str) -> bool:
    """Validate a Brazilian CPF (legacy alias for migration compatibility).

    Args:
        cpf: CPF string (with or without formatting).

    Returns:
        True if valid, False otherwise.
    """
    digits = _only_digits(cpf)
    if len(digits) != 11:
        return False
    if digits == digits[0] * 11:
        return False

    total = sum(int(digits[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    d1 = 0 if remainder < 2 else 11 - remainder
    if int(digits[9]) != d1:
        return False

    total = sum(int(digits[i]) * (11 - i) for i in range(10))
    remainder = total % 11
    d2 = 0 if remainder < 2 else 11 - remainder
    return int(digits[10]) == d2


def format_cpf(cpf: str) -> str:
    """Format a CPF string as XXX.XXX.XXX-XX (legacy alias)."""
    digits = _only_digits(cpf)
    if len(digits) != 11:
        raise ValueError(f"CPF must have 11 digits, got {len(digits)}")
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


_CNPJ_WEIGHTS_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_CNPJ_WEIGHTS_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def validate_cnpj(cnpj: str) -> bool:
    """Validate a Brazilian CNPJ (legacy alias for migration compatibility)."""
    digits = _only_digits(cnpj)
    if len(digits) != 14:
        return False
    if digits == digits[0] * 14:
        return False

    total = sum(int(digits[i]) * _CNPJ_WEIGHTS_1[i] for i in range(12))
    remainder = total % 11
    d1 = 0 if remainder < 2 else 11 - remainder
    if int(digits[12]) != d1:
        return False

    total = sum(int(digits[i]) * _CNPJ_WEIGHTS_2[i] for i in range(13))
    remainder = total % 11
    d2 = 0 if remainder < 2 else 11 - remainder
    return int(digits[13]) == d2


def format_cnpj(cnpj: str) -> str:
    """Format a CNPJ string as XX.XXX.XXX/XXXX-XX (legacy alias)."""
    digits = _only_digits(cnpj)
    if len(digits) != 14:
        raise ValueError(f"CNPJ must have 14 digits, got {len(digits)}")
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"


def validate_cep(cep: str) -> bool:
    """Validate a Brazilian CEP format (legacy alias for migration compatibility)."""
    digits = _only_digits(cep)
    if len(digits) != 8:
        return False
    return digits != "00000000"


def format_cep(cep: str) -> str:
    """Format a CEP string as XXXXX-XXX (legacy alias)."""
    digits = _only_digits(cep)
    if len(digits) != 8:
        raise ValueError(f"CEP must have 8 digits, got {len(digits)}")
    return f"{digits[:5]}-{digits[5:]}"
