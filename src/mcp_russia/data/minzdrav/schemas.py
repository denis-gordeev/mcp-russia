"""Схемы Pydantic модуля Минздрава РФ."""

from __future__ import annotations

from pydantic import BaseModel


class MedOrganizatsia(BaseModel):
    """Медицинская организация."""

    id: str
    nazvanie: str
    tip: str = ""  # тип МО (больница, поликлиника и т.д.)
    region: str = ""
    city: str = ""
    adres: str = ""
    telefon: str = ""
    litsenzia: str = ""
    krovatey: int = 0
    vrachey: int = 0


class VrachebnyyKadr(BaseModel):
    """Кадровая единица врача."""

    id: str
    familiya: str
    imya: str
    otchestvo: str = ""
    spetsialnost: str = ""
    kategoriya: str = ""  # высшая, первая, без категории
    stazh_let: int = 0
    organizatsia_id: str = ""


class PokazatelZdorovya(BaseModel):
    """Показатель здоровья населения."""

    kod: str
    nazvanie: str
    znachenie: float = 0.0
    ed_izm: str = ""
    god: int = 0
    region: str = ""
    istochnik: str = ""


class ZabolevanieStat(BaseModel):
    """Статистика по заболеванию."""

    kod_mkb: str
    nazvanie: str
    chelovek_zabolelo: int = 0
    chelovek_vylechilos: int = 0
    letalnykh_sluchaev: int = 0
    god: int = 0
    region: str = ""
