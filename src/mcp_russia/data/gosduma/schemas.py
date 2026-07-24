"""Схемы Pydantic модуля Госдумы."""

from __future__ import annotations

from pydantic import BaseModel


class Deputat(BaseModel):
    """Депутат Государственной Думы."""

    identifikator: int
    familiya: str
    imya: str
    otchestvo: str
    fraktsiya: str = ""
    komitet: str = ""
    subiekt: str = ""
    sozyv: str = ""
    foto_ssylka: str = ""


class Zakonoproekt(BaseModel):
    """Законопроект Государственной Думы."""

    identifikator: str
    nomer: str
    nazvanie: str
    sostoyanie: str = ""
    data_vneseniya: str = ""
    avtor: str = ""
    chteniya: int = 0


class Fraktsiya(BaseModel):
    """Фракция Государственной Думы."""

    kod: str
    nazvanie: str
    rukovoditel: str = ""
    kolichestvo: int = 0


class Golosovanie(BaseModel):
    """Результат голосования."""

    zakonoproekt_identifikator: str
    nazvanie: str
    data: str
    za: int = 0
    protiv: int = 0
    vozhderzhalsya: int = 0
    ne_golosoval: int = 0
