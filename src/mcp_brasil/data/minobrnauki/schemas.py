"""Pydantic schemas for the Минобрнауки feature."""

from __future__ import annotations

from pydantic import BaseModel


class VUZ(BaseModel):
    """Высшее учебное заведение."""
    nazvanie: str = ""
    tip: str = ""
    gorod: str = ""
    region: str = ""
    federalny_okrug: str = ""
    status_akkreditatsii: str = ""
    kolichestvo_studentov: int | None = None
    kolichestvo_prepodavateley: int | None = None
    god_osnovaniya: int | None = None
    sajt: str = ""
    rektor: str = ""


class ObrazovatelnayaProgramma(BaseModel):
    """Образовательная программа."""
    nazvanie: str = ""
    kod_napravleniya: str = ""
    uroven: str = ""
    forma_obucheniya: str = ""
    vuz: str = ""
    srok_obucheniya: str = ""
    byudzhetnye_mesta: int | None = None
    prohodnoy_ball: float | None = None


class NauchnoeIssledovanie(BaseModel):
    """Научное исследование / грант."""
    nazvanie: str = ""
    rukovoditel: str = ""
    organizatsiya: str = ""
    tip_granta: str = ""
    summa_finansirovaniya: float | None = None
    god_nachala: int | None = None
    god_okonchaniya: int | None = None
    otrasl_nauki: str = ""
    status: str = ""


class Aspirant(BaseModel):
    """Аспирант / докторант."""
    fio: str = ""
    organizatsiya: str = ""
    napravlenie: str = ""
    god_postupleniya: int | None = None
    forma_obucheniya: str = ""
    nauchny_rukovoditel: str = ""
    status: str = ""


class ReytingVUZa(BaseModel):
    """Рейтинг вуза."""
    nazvanie: str = ""
    mesto_v_reytinge: int | None = None
    ball: float | None = None
    tip_reytinga: str = ""
    god: int | None = None
    ocenka_obrazovanie: float | None = None
    ocenka_nauka: float | None = None
    ocenka_socialnaya: float | None = None
