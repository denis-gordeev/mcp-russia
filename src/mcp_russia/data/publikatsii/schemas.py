"""Схемы Pydantic модуля Официальные публикации РФ."""

from __future__ import annotations

from pydantic import BaseModel


class NormativnyyAkt(BaseModel):
    """Нормативный правовой акт РФ."""

    nomer: str
    nazvanie: str
    tip: str = ""  # fz, ukaz, postanovlenie_pr, etc.
    data_prinyatiya: str = ""
    data_publikatsii: str = ""
    istochnik: str = ""  # pravo.gov.ru, rg.ru, etc.
    status: str = ""  # deystvuyushchiy, utratil_silu, etc.
    otrysl: str = ""
    kratkoe_opisanie: str = ""
    tekst_url: str = ""
    izmeneniya: list[str] = []


class ZakonProekt(BaseModel):
    """Законопроект."""

    nomer: str
    nazvanie: str
    stadnya: str = ""
    data_vneseniya: str = ""
    vnesen_subiekt: str = ""
    otvetstvennyy_komitet: str = ""
    chteniya: list[dict[str, str]] = []
    tekst_url: str = ""


class OficialnayaPublikatsiya(BaseModel):
    """Официальная публикация."""

    nazvanie: str
    tip_dokumenta: str = ""
    data_publikatsii: str = ""
    nomer_vypuska: str = ""
    istochnik: str = ""
    rubrika: str = ""
    annotaciya: str = ""
    tekst_url: str = ""


class IzmenenieAkta(BaseModel):
    """Изменение нормативного акта."""

    akt_nomer: str
    akt_nazvanie: str
    izmenenie_nomer: str
    izmenenie_data: str = ""
    izmenenie_opisanie: str = ""
    data_vstupleniya_v_silu: str = ""
    tekst_url: str = ""
