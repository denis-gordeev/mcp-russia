"""Валидаторы российских документов: ИНН, КПП, СНИЛС, почтовый индекс."""

from __future__ import annotations

import re

_DIGITS_RE = re.compile(r"\D")


def _tolko_tsifry(stroka: str) -> str:
    """Удаление всех нецифровых символов."""
    return _DIGITS_RE.sub("", stroka)


# ---------------------------------------------------------------------------
# ИНН (Идентификационный номер налогоплательщика)
# ---------------------------------------------------------------------------


def proverit_inn(inn: str) -> bool:
    """Валидация российского ИНН (идентификационный номер налогоплательщика).

    Поддерживает форматы 10 цифр (юридические лица) и 12 цифр (физические лица).

    Аргументы:
        inn: Строка ИНН (с форматированием или без).

    Возвращает:
        True если валиден, иначе False.
    """
    tsifry = _tolko_tsifry(inn)
    if len(tsifry) not in (10, 12):
        return False

    if len(tsifry) == 10:
        vesa = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        itogo = sum(int(tsifry[i]) * vesa[i] for i in range(9))
        ostatok = itogo % 11
        proverochnaya_tsifra = ostatok % 10
        return int(tsifry[9]) == proverochnaya_tsifra

    vesa1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    vesa2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    summa1 = sum(int(tsifry[i]) * vesa1[i] for i in range(10))
    ostatok1 = summa1 % 11
    kontrol1 = ostatok1 % 10
    if int(tsifry[10]) != kontrol1:
        return False

    summa2 = sum(int(tsifry[i]) * vesa2[i] for i in range(11))
    ostatok2 = summa2 % 11
    kontrol2 = ostatok2 % 10
    return int(tsifry[11]) == kontrol2


def formatirovat_inn(inn: str) -> str:
    """Форматирование ИНН для отображения.

    Аргументы:
        inn: Цифры ИНН (с форматированием или без).

    Возвращает:
        Отформатированная строка ИНН.

    Вызывает:
        ValueError: Если ИНН не содержит 10 или 12 цифр.
    """
    tsifry = _tolko_tsifry(inn)
    if len(tsifry) == 10:
        return tsifry
    if len(tsifry) == 12:
        return tsifry
    raise ValueError(f"ИНН должен содержать 10 или 12 цифр, получено {len(tsifry)}")


# ---------------------------------------------------------------------------
# КПП (Код причины постановки на учёт)
# ---------------------------------------------------------------------------


def proverit_kpp(kpp: str) -> bool:
    """Валидация российского КПП (код причины постановки на учёт).

    КПП — 9-значный код, используемый совместно с ИНН для юридических лиц.

    Аргументы:
        kpp: Строка КПП (с форматированием или без).

    Возвращает:
        True если формат корректен, иначе False.
    """
    tsifry = _tolko_tsifry(kpp)
    if len(tsifry) != 9:
        return False
    return tsifry[:2] != "00"


def formatirovat_kpp(kpp: str) -> str:
    """Форматирование КПП для отображения.

    Аргументы:
        kpp: Цифры КПП (с форматированием или без).

    Возвращает:
        Отформатированная строка КПП.

    Вызывает:
        ValueError: Если КПП не содержит ровно 9 цифр.
    """
    tsifry = _tolko_tsifry(kpp)
    if len(tsifry) != 9:
        raise ValueError(f"КПП должен содержать 9 цифр, получено {len(tsifry)}")
    return tsifry


# ---------------------------------------------------------------------------
# СНИЛС (Страховой номер индивидуального лицевого счёта)
# ---------------------------------------------------------------------------


def proverit_snils(snils: str) -> bool:
    """Валидация российского СНИЛС (страховой номер индивидуального лицевого счёта).

    СНИЛС — 11-значное число (9 цифр + 2 контрольные цифры).

    Аргументы:
        snils: Строка СНИЛС (с форматированием или без).

    Возвращает:
        True если валиден, иначе False.
    """
    tsifry = _tolko_tsifry(snils)
    if len(tsifry) != 11:
        return False

    itogo = 0
    for i in range(9):
        itogo += int(tsifry[i]) * (9 - i)

    if itogo < 100:
        proverochnaya_tsifra = itogo
    elif itogo in (100, 101):
        proverochnaya_tsifra = 0
    else:
        ostatok = itogo % 101
        proverochnaya_tsifra = 0 if ostatok == 100 else ostatok

    stroka_kontrolya = f"{proverochnaya_tsifra:02d}"
    return tsifry[9:] == stroka_kontrolya


def formatirovat_snils(snils: str) -> str:
    """Форматирование СНИЛС в виде XXX-XXX-XXX XX.

    Аргументы:
        snils: Цифры СНИЛС (с форматированием или без).

    Возвращает:
        Отформатированная строка СНИЛС.

    Вызывает:
        ValueError: Если СНИЛС не содержит ровно 11 цифр.
    """
    tsifry = _tolko_tsifry(snils)
    if len(tsifry) != 11:
        raise ValueError(f"СНИЛС должен содержать 11 цифр, получено {len(tsifry)}")
    return f"{tsifry[:3]}-{tsifry[3:6]}-{tsifry[6:9]} {tsifry[9:]}"


# ---------------------------------------------------------------------------
# Почтовый индекс России
# ---------------------------------------------------------------------------


def proverit_pochtovyy_indeks(pochtovyy_indeks: str) -> bool:
    """Валидация российского почтового индекса (6 цифр).

    Аргументы:
        pochtovyy_indeks: Строка почтового индекса (с форматированием или без).

    Возвращает:
        True если формат корректен, иначе False.
    """
    tsifry = _tolko_tsifry(pochtovyy_indeks)
    if len(tsifry) != 6:
        return False
    return tsifry[0] in "123456"


def formatirovat_pochtovyy_indeks(pochtovyy_indeks: str) -> str:
    """Форматирование российского почтового индекса как XXXXXX.

    Аргументы:
        pochtovyy_indeks: Цифры почтового индекса (с форматированием или без).

    Возвращает:
        Отформатированная строка почтового индекса.

    Вызывает:
        ValueError: Если почтовый индекс не содержит ровно 6 цифр.
    """
    tsifry = _tolko_tsifry(pochtovyy_indeks)
    if len(tsifry) != 6:
        raise ValueError(
            f"Российский почтовый индекс должен содержать 6 цифр, получено {len(tsifry)}"
        )
    return tsifry
