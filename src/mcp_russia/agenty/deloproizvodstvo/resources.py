"""Ресурсы: шаблоны и нормы делопроизводства РФ.

Ресурсы — это данные, которые LLM загружает как контекст.
"""

from __future__ import annotations

from pathlib import Path

DIREKTORIYA_SHABLONOV = Path(__file__).parent / "shablony"
DIREKTORIYA_NORM = Path(__file__).parent / "normy"


def _zagruzit_fayl(direktoriya: Path, imya_fayla: str) -> str:
    """Загружает файл шаблона или нормы."""
    put_fayla = direktoriya / imya_fayla
    if not put_fayla.exists():
        raise FileNotFoundError(f"Файл не найден: {put_fayla}")
    return put_fayla.read_text(encoding="utf-8")


# === Шаблоны документов ===


def poluchit_shablon_pismo() -> str:
    """Шаблон официального письма."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "pismo.md")


def poluchit_shablon_prikaz() -> str:
    """Шаблон приказа."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "prikaz.md")


def poluchit_shablon_rasporyazhenie() -> str:
    """Шаблон распоряжения."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "rasporyazhenie.md")


def poluchit_shablon_akt() -> str:
    """Шаблон акта."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "akt.md")


def poluchit_shablon_spravka() -> str:
    """Шаблон справки."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "spravka.md")


def poluchit_shablon_protokol() -> str:
    """Шаблон протокола."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "protokol.md")


def poluchit_shablon_dokladnaya_zapiska() -> str:
    """Шаблон докладной записки."""
    return _zagruzit_fayl(DIREKTORIYA_SHABLONOV, "dokladnaya_zapiska.md")


# === Нормы делопроизводства ===


def poluchit_manual_deloproizvodstvo() -> str:
    """Сводка правил оформления документов (ГОСТ Р 7.0.97-2016)."""
    return _zagruzit_fayl(DIREKTORIYA_NORM, "manual_deloproizvodstvo.md")


def poluchit_obrashcheniya() -> str:
    """Формы обращения к должностным лицам."""
    return _zagruzit_fayl(DIREKTORIYA_NORM, "obrashcheniya.md")


def poluchit_zaklyuchitelnye_formuly() -> str:
    """Заключительные формулы в официальных документах."""
    return _zagruzit_fayl(DIREKTORIYA_NORM, "zaklyuchitelnye_formuly.md")
