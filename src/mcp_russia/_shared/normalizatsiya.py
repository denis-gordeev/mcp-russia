"""Типизированная нормализация значений из внешних JSON-ответов.

Модуль предоставляет безопасные помощники для приведения значений
внешних API к ожидаемым типам без превращения None в строку «None»
и без потери данных при некорректных типах.

Контракт:
- bezopasnaya_stroka: None/bool/dict/list → умолчание; str → str; int/float → str
- bezopasnoe_tseloe: None/bool → умолчание; int → int; float → int если целое; str → разбор
- bezopasnoe_chislo: None/bool → умолчание; int/float/str → float при успехе
- izvlech_spisok: list → list; dict → поиск по ключам; прочее → []
- pervoe_znachenie: первое не-None значение из нескольких ключей словаря
- razorvat_stroku_spisok: str → split; list → str каждого; прочее → []
"""

from __future__ import annotations

from typing import Any


def bezopasnaya_stroka(znachenie: object, po_umolchaniyu: str = "") -> str:
    """Безопасно приводит скалярное значение внешнего API к строке.

    Отвергает None, bool, dict, list — возвращает умолчание.
    Строки пропускаются без изменений; числа преобразуются в строку.
    """
    if znachenie is None or isinstance(znachenie, (bool, dict, list)):
        return po_umolchaniyu
    if isinstance(znachenie, str):
        return znachenie
    if isinstance(znachenie, (int, float)):
        return str(znachenie)
    return po_umolchaniyu


def bezopasnoe_tseloe(znachenie: object, po_umolchaniyu: int = 0) -> int:
    """Безопасно приводит целочисленное значение внешнего API к числу.

    Отвергает None и bool. Целые числа пропускаются; дробные — только
    если значение целое; строки разбираются через int().
    """
    if znachenie is None or isinstance(znachenie, bool):
        return po_umolchaniyu
    if isinstance(znachenie, int):
        return znachenie
    if isinstance(znachenie, float):
        return int(znachenie) if znachenie.is_integer() else po_umolchaniyu
    if isinstance(znachenie, str):
        try:
            return int(znachenie.strip())
        except ValueError:
            return po_umolchaniyu
    return po_umolchaniyu


def bezopasnoe_chislo(znachenie: object, po_umolchaniyu: float | None = None) -> float | None:
    """Безопасно приводит числовое значение внешнего API к float.

    Отвергает None и bool. Числа и числовые строки преобразуются;
    прочие строки и типы возвращают умолчание.
    """
    if znachenie is None or isinstance(znachenie, bool):
        return po_umolchaniyu
    if isinstance(znachenie, (int, float)):
        return float(znachenie)
    if isinstance(znachenie, str):
        try:
            return float(znachenie)
        except ValueError:
            return po_umolchaniyu
    return po_umolchaniyu


def izvlech_spisok(dannye: object, *klyuchi: str) -> list[Any]:
    """Извлекает список из корневого массива или известных полей ответа.

    Если даны ключи — ищет по ним; иначе — по типичным именам:
    data, items, results, records, list.
    """
    if isinstance(dannye, list):
        return dannye
    if not isinstance(dannye, dict):
        return []
    klyuchi_poiska = klyuchi if klyuchi else ("data", "items", "results", "records", "list")
    for klyuch in klyuchi_poiska:
        elementy = dannye.get(klyuch)
        if isinstance(elementy, list):
            return elementy
    return []


def pervoe_znachenie(zapis: dict[str, Any], *klyuchi: str) -> object:
    """Возвращает первое не-None значение из вариантов схемы API."""
    for klyuch in klyuchi:
        znachenie = zapis.get(klyuch)
        if znachenie is not None:
            return znachenie
    return None


def razorvat_stroku_spisok(dannye: object, razdelitel: str = ",") -> list[str]:
    """Разбирает строку-через-разделитель или список в список строк.

    Строки разбиваются по разделителю с удалением пустых элементов;
    списки приводятся поэлементно к str; прочие типы дают [].
    """
    if isinstance(dannye, str):
        return [element.strip() for element in dannye.split(razdelitel) if element.strip()]
    if isinstance(dannye, list):
        return [element if isinstance(element, str) else str(element) for element in dannye]
    return []
