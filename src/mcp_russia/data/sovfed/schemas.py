"""Pydantic schemas for the Совет Федерации РФ feature."""

from __future__ import annotations

from pydantic import BaseModel


class SenatorRezyume(BaseModel):
    nomer: str
    familiya: str
    imya: str
    otchestvo: str = ""
    region: str = ""
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
    status: str = ""
    povestka: str = ""


class ZakonoproektSovfeda(BaseModel):
    nomer: str
    nazvanie: str
    status: str = ""
    data_rassmotreniya: str = ""
    iniciator: str = ""
