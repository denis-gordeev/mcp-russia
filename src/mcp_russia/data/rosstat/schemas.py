"""Pydantic schemas for the Rosstat feature."""

from __future__ import annotations

from pydantic import BaseModel


class PokazatelRosstata(BaseModel):
    """Показатель Росстата."""

    code: str
    name: str
    value: float
    unit: str = ""
    date: str = ""
    source: str = "Федеральная служба государственной статистики (Росстат)"


class RegionData(BaseModel):
    """Данные по региону РФ."""

    code: str
    name: str
    federalny_okrug: str = ""
    population: int | None = None
    vrp: float | None = None
    srednyaya_zp: float | None = None


class InflaciyaData(BaseModel):
    """Данные об инфляции (ИПЦ)."""

    period: str
    ipcz_mesyac: float | None = None
    ipcz_nakoplenny: float | None = None
    ipcz_god: float | None = None


class DemografiyaData(BaseModel):
    """Демографические данные."""

    period: str
    naselenie: int | None = None
    rozhdaemost: float | None = None
    smertnost: float | None = None
    estestvenny_prirost: float | None = None


class VRPData(BaseModel):
    """Данные о валовом региональном продукте."""

    period: str
    region: str = ""
    vrp: float | None = None
    vrp_per_capita: float | None = None


class WagesData(BaseModel):
    """Данные о заработной плате."""

    period: str
    region: str = ""
    nominalnaya_zp: float | None = None
    realnaya_zp_change: float | None = None


class IndikatorDannye(BaseModel):
    """Универсальные данные показателя ЕМИСС."""

    kod_emiss: str
    nazvanie: str = ""
    period: str = ""
    znachenie: float | None = None
    edinitsa: str = ""
    region: str = ""
