"""Схемы Pydantic модуля МЧС России."""

from __future__ import annotations

from pydantic import BaseModel


class Pozhar(BaseModel):
    nomer: str
    data: str = ""
    subiekt: str = ""
    vid_pozhara: str = ""
    pogibshikh: int = 0
    postradavshikh: int = 0
    ushcherb: float | None = None


class ChrezvychaynayaSituatsiya(BaseModel):
    nomer: str
    vid_chs: str = ""
    klass_chs: str = ""
    data_vozniknoveniya: str = ""
    subiekt: str = ""
    opisanie: str = ""
    sostoyanie: str = ""
    pogibshikh: int = 0
    postradavshikh: int = 0


class RadiatsionnyyMonitoring(BaseModel):
    stantsiya: str
    subiekt: str = ""
    uroven_radiatsii: float = 0.0
    edinitsa: str = "мкЗв/ч"
    data_izmereniya: str = ""
    norma: float = 0.30


class GidrologicheskayaObstanovka(BaseModel):
    reka: str
    punkt_nablyudeniya: str = ""
    uroven_vody: float = 0.0
    opasnyy_uroven: float | None = None
    tendentsiya: str = ""
    data_izmereniya: str = ""
