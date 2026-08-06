"""Схемы Pydantic модуля Ростехнадзора."""

from __future__ import annotations

from pydantic import BaseModel


class Intsident(BaseModel):
    nomer: str = ""
    vid: str = ""
    data: str = ""
    subiekt: str = ""
    opisanie: str = ""
    pogibshikh: int = 0
    postradavshikh: int = 0
    istochnik: str = "Ростехнадзор (rostechnadzor.gov.ru)"


class LitsenziyaRT(BaseModel):
    nomer: str = ""
    vid: str = ""
    organizatsiya: str = ""
    subiekt: str = ""
    data_vydachi: str = ""
    srok_deystviya: str = ""
    sostoyanie: str = ""
    istochnik: str = "Ростехнадзор (rostechnadzor.gov.ru)"


class OpasnyyObekt(BaseModel):
    registratsionnyy_nomer: str = ""
    nazvanie: str = ""
    vid_deyatelnosti: str = ""
    klass_opasnosti: str = ""
    subiekt: str = ""
    organizatsiya: str = ""
    istochnik: str = "Ростехнадзор (rostechnadzor.gov.ru)"
