"""Схемы Pydantic модуля Минздрава РФ."""

from __future__ import annotations

from pydantic import BaseModel


class MedOrganizatsia(BaseModel):
    """Медицинская организация."""

    identifikator: str
    nazvanie: str
    tip: str = ""
    subiekt: str = ""
    gorod: str = ""
    adres: str = ""
    telefon: str = ""
    litsenzia: str = ""
    krovatey: int = 0
    vrachey: int = 0


class VrachebnyyKadr(BaseModel):
    """Кадровая единица врача."""

    identifikator: str
    familiya: str
    imya: str
    otchestvo: str = ""
    spetsialnost: str = ""
    kategoriya: str = ""  # высшая, первая, без категории
    stazh_let: int = 0
    organizatsia_identifikator: str = ""


class PokazatelZdorovya(BaseModel):
    """Показатель здоровья населения."""

    kod: str
    nazvanie: str
    znachenie: float = 0.0
    edinitsa_izmereniya: str = ""
    god: int = 0
    subiekt: str = ""
    istochnik: str = ""


class ZabolevanieStat(BaseModel):
    """Статистика по заболеванию."""

    kod_mkb: str
    nazvanie: str
    chelovek_zabolelo: int = 0
    chelovek_vylechilos: int = 0
    letalnykh_sluchaev: int = 0
    god: int = 0
    subiekt: str = ""
