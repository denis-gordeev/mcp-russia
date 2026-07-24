"""Схемы Pydantic модуля Совета Федерации РФ."""

from __future__ import annotations

from pydantic import BaseModel


class SenatorRezyume(BaseModel):
    nomer: str
    familiya: str
    imya: str
    otchestvo: str = ""
    subiekt: str = ""
    dolzhnost: str = ""
    komitet: str = ""
    fraktsiya: str = ""
    data_naznacheniya: str = ""


class InformatsiyaKomiteta(BaseModel):
    nazvanie: str
    predsedatel: str = ""
    kolichestvo_chlenov: int = 0
    napravlenie: str = ""


class InformatsiyaZasedaniya(BaseModel):
    nomer: str
    data: str = ""
    sostoyanie: str = ""
    povestka: str = ""


class ZakonoproektSovfeda(BaseModel):
    nomer: str
    nazvanie: str
    sostoyanie: str = ""
    data_rassmotreniya: str = ""
    iniciator: str = ""
