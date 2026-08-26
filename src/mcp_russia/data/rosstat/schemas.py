"""Схемы Pydantic модуля Росстата."""

from __future__ import annotations

from pydantic import BaseModel


class DannyeRegiona(BaseModel):
    """Данные по региону РФ."""

    kod: str
    nazvanie: str
    federalny_okrug: str = ""
    naselenie: int | None = None
    vrp: float | None = None
    srednyaya_zp: float | None = None


class InflyatsiyaDannye(BaseModel):
    """Данные об инфляции (ИПЦ)."""

    period: str
    ipcz_mesyac: float | None = None
    ipcz_nakoplenny: float | None = None
    ipcz_god: float | None = None


class DemografiyaDannye(BaseModel):
    """Демографические данные."""

    period: str
    naselenie: int | None = None
    rozhdaemost: float | None = None
    smertnost: float | None = None
    estestvenny_prirost: float | None = None


class VRPDannye(BaseModel):
    """Данные о валовом региональном продукте."""

    period: str
    subiekt: str = ""
    vrp: float | None = None
    vrp_na_dushu: float | None = None


class DannyeZarplaty(BaseModel):
    """Данные о заработной плате."""

    period: str
    subiekt: str = ""
    nominalnaya_zp: float | None = None
    realnaya_zp_izmenenie: float | None = None


class IndikatorDannye(BaseModel):
    """Универсальные данные показателя ЕМИСС."""

    kod_emiss: str
    nazvanie: str = ""
    period: str = ""
    znachenie: float | None = None
    edinitsa_izmereniya: str = ""
    subiekt: str = ""


class OtraslevayaStrukturaVRP(BaseModel):
    """Отраслевая структура ВРП по ОКВЭД."""

    subiekt: str = ""
    period: str = ""
    otrasl: str = ""
    kod_okved: str = ""
    dolya_vvp: float | None = None
    vrp: float | None = None


class InvestitsiiPoVidam(BaseModel):
    """Инвестиции в основной капитал по видам деятельности."""

    subiekt: str = ""
    period: str = ""
    vid_deyatelnosti: str = ""
    kod_okved: str = ""
    investitsii: float | None = None
    dolya: float | None = None
