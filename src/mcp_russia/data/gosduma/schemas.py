"""Схемы Pydantic модуля Госдумы."""

from __future__ import annotations

from pydantic import BaseModel


class Deputat(BaseModel):
    """Депутат Государственной Думы."""

    id: int
    фамилия: str
    имя: str
    отчество: str
    фракция: str = ""
    комитет: str = ""
    регион: str = ""
    созыв: str = ""
    foto_url: str = ""


class Zakonoproekt(BaseModel):
    """Законопроект Государственной Думы."""

    id: str
    number: str
    title: str
    status: str = ""
    data_vneseniya: str = ""
    author: str = ""
    readings: int = 0


class Frakciya(BaseModel):
    """Фракция Государственной Думы."""

    kod: str
    nazvanie: str
    rukovoditel: str = ""
    count: int = 0


class Golosovanie(BaseModel):
    """Результат голосования."""

    zakonoproekt_id: str
    title: str
    data: str
    za: int = 0
    protiv: int = 0
    vozhderzhalsya: int = 0
    ne_golosoval: int = 0
