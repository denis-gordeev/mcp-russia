"""Схемы Pydantic модуля Официальные публикации РФ."""

from __future__ import annotations

from pydantic import BaseModel


class NormativnyyAkt(BaseModel):
    """Нормативный правовой акт РФ."""

    nomer: str
    nazvanie: str
    tip: str = ""  # фз, указ, постановление пр. и т.д.
    data_prinyatiya: str = ""
    data_publikatsii: str = ""
    istochnik: str = ""  # pravo.gov.ru, rg.ru и т.д.
    sostoyanie: str = ""  # действующий, утратил силу и т.д.
    otrasl: str = ""
    kratkoe_opisanie: str = ""
    tekst_ssylka: str = ""
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
    tekst_ssylka: str = ""


class OficialnayaPublikatsiya(BaseModel):
    """Официальная публикация."""

    nazvanie: str
    tip_dokumenta: str = ""
    data_publikatsii: str = ""
    nomer_vypuska: str = ""
    istochnik: str = ""
    rubrika: str = ""
    annotatsiya: str = ""
    tekst_ssylka: str = ""


class IzmenenieAkta(BaseModel):
    """Изменение нормативного акта."""

    akt_nomer: str
    akt_nazvanie: str
    izmenenie_nomer: str
    izmenenie_data: str = ""
    izmenenie_opisanie: str = ""
    data_vstupleniya_v_silu: str = ""
    tekst_ssylka: str = ""
