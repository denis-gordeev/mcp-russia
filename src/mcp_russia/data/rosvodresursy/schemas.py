"""Схемы Pydantic модуля Росводресурсов."""

from __future__ import annotations

from pydantic import BaseModel


class VodnyyObekt(BaseModel):
    """Водный объект РФ."""

    kod: str
    nazvanie: str
    tip: str = ""  # reka, ozero, vodokhranilishche, и т.д.
    basseyn: str = ""
    dlinna_km: float | None = None
    ploshchad_km2: float | None = None
    region: str = ""
    opisaniye: str = ""


class GidroData(BaseModel):
    """Гидрологические данные."""

    post: str = ""
    vodnyy_obekt: str = ""
    data_izmereniya: str = ""
    uroven: float | None = None
    raskhod: float | None = None
    temperatura: float | None = None
    ledovaya_obstanovka: str = ""
    preduprezhdenie: str = ""


class VodokhranilishcheData(BaseModel):
    """Данные водохранилища."""

    kod: str
    nazvanie: str
    region: str = ""
    obiem_km3: float | None = None
    ploshchad_km2: float | None = None
    uroven_m: float | None = None
    priznak_napolneniya: str = ""  # normalnoe, nizkoe, vysokoe
    data_izmereniya: str = ""


class Vodopolzovanie(BaseModel):
    """Данные о водопользовании."""

    region: str = ""
    god: str = ""
    zabrano_vody_km3: float | None = None
    ispolzovano_vody_km3: float | None = None
    sbrosheno_stokov_km3: float | None = None
    istochnik: str = ""
    naznachenie: str = ""
