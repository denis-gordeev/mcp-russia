"""Resources: шаблоны и нормыамы делопроизводства РФ.

Resources — это данные, которые LLM загружает как контекст.
"""

from __future__ import annotations

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"
NORMAS_DIR = Path(__file__).parent / "normas"


def _load_file(directory: Path, filename: str) -> str:
    """Загружает файл шаблона или нормы."""
    filepath = directory / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    return filepath.read_text(encoding="utf-8")


# === Шаблоны документов ===


def get_template_pismo() -> str:
    """Шаблон официального письма."""
    return _load_file(TEMPLATES_DIR, "pismo.md")


def get_template_prikaz() -> str:
    """Шаблон приказа."""
    return _load_file(TEMPLATES_DIR, "prikaz.md")


def get_template_rasporyazhenie() -> str:
    """Шаблон распоряжения."""
    return _load_file(TEMPLATES_DIR, "rasporyazhenie.md")


def get_template_akt() -> str:
    """Шаблон акта."""
    return _load_file(TEMPLATES_DIR, "akt.md")


def get_template_spravka() -> str:
    """Шаблон справки."""
    return _load_file(TEMPLATES_DIR, "spravka.md")


def get_template_protokol() -> str:
    """Шаблон протокола."""
    return _load_file(TEMPLATES_DIR, "protokol.md")


def get_template_dokladnaya_zapiska() -> str:
    """Шаблон докладной записки."""
    return _load_file(TEMPLATES_DIR, "dokladnaya_zapiska.md")


# === Нормы делопроизводства ===


def get_manual_deloproizvodstvo() -> str:
    """Сводка правил оформления документов (ГОСТ Р 7.0.97-2016)."""
    return _load_file(NORMAS_DIR, "manual_deloproizvodstvo.md")


def get_obrashcheniya() -> str:
    """Формы обращения к должностным лицам."""
    return _load_file(NORMAS_DIR, "obrashcheniya.md")


def get_zaklyuchitelnye_formuly() -> str:
    """Заключительные формулы в официальных документах."""
    return _load_file(NORMAS_DIR, "zaklyuchitelnye_formuly.md")
