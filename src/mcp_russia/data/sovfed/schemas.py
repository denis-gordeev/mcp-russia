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
    frakciya: str = ""
    data_naznacheniya: str = ""


class KomitetInfo(BaseModel):
    nazvanie: str
    predsedatel: str = ""
    kolichestvo_chlenov: int = 0
    napravlenie: str = ""


class ZasedanieInfo(BaseModel):
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
