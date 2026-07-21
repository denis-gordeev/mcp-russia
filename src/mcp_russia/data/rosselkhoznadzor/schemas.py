"""Схемы Pydantic модуля Россельхознадзор."""

from __future__ import annotations

from pydantic import BaseModel


class ProverkaRskhn(BaseModel):
    nomer: str
    vid_nadzora: str = ""
    tip_proverki: str = ""
    data_provedeniya: str = ""
    subiekt: str = ""
    sostoyanie: str = ""
    narusheniya: int = 0
    istochnik: str = ""


class KarantinnyyObyekt(BaseModel):
    nazvanie: str
    tip: str = ""
    subiekt: str = ""
    sostoyanie_karantina: str = ""
    data_vvedeniya: str = ""
    opisanie: str = ""


class RegistratsiyaProduktsii(BaseModel):
    nomer: str
    naimenovanie: str = ""
    proizvoditel: str = ""
    tip_produktsii: str = ""
    data_registratsii: str = ""
    srok_deystviya: str = ""
    sostoyanie: str = ""


class VeterinarnyySertifikat(BaseModel):
    nomer: str
    tip_produktsii: str = ""
    otpravitel: str = ""
    poluchatel: str = ""
    data_oformleniya: str = ""
    subiekt_otpravki: str = ""
    sostoyanie: str = ""
