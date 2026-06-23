"""Схемы Pydantic модуля Росстата."""

from __future__ import annotations

from pydantic import BaseModel


class PokazatelRosstata(BaseModel):
    """Показатель Росстата."""

    kod: str
    nazvanie: str
    znachenie: float
    edinitsa: str = ""
    data: str = ""
    istochnik: str = "Федеральная служба государственной статистики (Росстат)"


class DannyeRegiona(BaseModel):
    """Данные по региону РФ."""

    kod: str
    nazvanie: str
    federalny_okrug: str = ""
    naselenie: int | None = None
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
    vrp_na_dushu: float | None = None


class DannyeZarplaty(BaseModel):
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


class OtraslevayaStrukturaVRP(BaseModel):
    """Отраслевая структура ВРП по ОКВЭД."""

    region: str = ""
    period: str = ""
    otrasl: str = ""
    kod_okved: str = ""
    dolya_vvp: float | None = None
    vrp: float | None = None


class InvestitsiiPoVidam(BaseModel):
    """Инвестиции в основной капитал по видам деятельности."""

    region: str = ""
    period: str = ""
    vid_deyatelnosti: str = ""
    kod_okved: str = ""
    investitsii: float | None = None
    dolya: float | None = None
