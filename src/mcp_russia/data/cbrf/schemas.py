"""Схемы Pydantic модуля ЦБ РФ."""

from __future__ import annotations

from pydantic import BaseModel


class ZnachenieValyuty(BaseModel):
    """Значение одной валюты на определённую дату."""

    kod: str
    nazvanie: str
    nominal: int
    znachenie: float
    predydushchee_znachenie: float | None = None
    data: str = ""


class DannyeValyuty(BaseModel):
    """Полные данные по валюте из API ЦБ РФ."""

    kod: str
    nazvanie: str
    nominal: int
    znachenie: float
    previous: float | None = None
    data: str = ""


class EkonomicheskiyIndikator(BaseModel):
    """Экономический показатель ЦБ РФ."""

    nazvanie: str
    znachenie: float
    data: str
    edinitsa: str = ""
    istochnik: str = "Центральный банк Российской Федерации"


class KlyuchevayaStavka(BaseModel):
    """Ключевая ставка ЦБ РФ."""

    znachenie: float
    data: str
    predydushchaya_data: str | None = None
    predydushchee_znachenie: float | None = None
    raznitsa: float | None = None
    istochnik: str = "Центральный банк Российской Федерации"
