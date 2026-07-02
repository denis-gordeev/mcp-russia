"""Ресурсы: шаблоны и нормы делопроизводства РФ.

Ресурсы — это данные, которые LLM загружает как контекст.
"""

from __future__ import annotations

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"
NORMAS_DIR = Path(__file__).parent / "normas"


def _zagruzit_fayl(direktoriya: Path, imya_fayla: str) -> str:
    """Загружает файл шаблона или нормы."""
    filepath = direktoriya / imya_fayla
    if not filepath.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    return filepath.read_text(encoding="utf-8")


# === Шаблоны документов ===


def poluchit_shablon_pismo() -> str:
    """Шаблон официального письма."""
    return _zagruzit_fayl(TEMPLATES_DIR, "pismo.md")


def poluchit_shablon_prikaz() -> str:
    """Шаблон приказа."""
    return _zagruzit_fayl(TEMPLATES_DIR, "prikaz.md")


def poluchit_shablon_rasporyazhenie() -> str:
    """Шаблон распоряжения."""
    return _zagruzit_fayl(TEMPLATES_DIR, "rasporyazhenie.md")


def poluchit_shablon_akt() -> str:
    """Шаблон акта."""
    return _zagruzit_fayl(TEMPLATES_DIR, "akt.md")


def poluchit_shablon_spravka() -> str:
    """Шаблон справки."""
    return _zagruzit_fayl(TEMPLATES_DIR, "spravka.md")


def poluchit_shablon_protokol() -> str:
    """Шаблон протокола."""
    return _zagruzit_fayl(TEMPLATES_DIR, "protokol.md")


def poluchit_shablon_dokladnaya_zapiska() -> str:
    """Шаблон докладной записки."""
    return _zagruzit_fayl(TEMPLATES_DIR, "dokladnaya_zapiska.md")


# === Нормы делопроизводства ===


def poluchit_manual_deloproizvodstvo() -> str:
    """Сводка правил оформления документов (ГОСТ Р 7.0.97-2016)."""
    return _zagruzit_fayl(NORMAS_DIR, "manual_deloproizvodstvo.md")


def poluchit_obrashcheniya() -> str:
    """Формы обращения к должностным лицам."""
    return _zagruzit_fayl(NORMAS_DIR, "obrashcheniya.md")


def poluchit_zaklyuchitelnye_formuly() -> str:
    """Заключительные формулы в официальных документах."""
    return _zagruzit_fayl(NORMAS_DIR, "zaklyuchitelnye_formuly.md")
