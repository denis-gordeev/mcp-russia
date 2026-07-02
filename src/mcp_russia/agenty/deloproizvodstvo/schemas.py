"""Pydantic-модели для модуля делопроизводства."""

from __future__ import annotations

from pydantic import BaseModel


class ObrashchenieDolzhnostnogoLitsa(BaseModel):
    """Форма обращения к должностному лицу."""

    dolzhnost: str
    obrashchenie: str
    titulovanie: str
    adresatsiya: str


class RezultatValidatsii(BaseModel):
    """Результат валидации официального документа."""

    korrektno: bool
    problemy: list[str]
    rekomendatsii: list[str]
