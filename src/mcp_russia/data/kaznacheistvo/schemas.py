"""Pydantic schemas for the Федеральное казначейство feature."""

from __future__ import annotations

from pydantic import BaseModel


class ByudzhetnayaSmeta(BaseModel):
    nomer: str
    nazvanie: str
    tip: str = ""
    god: str = ""
    dohody: float | None = None
    raskhody: float | None = None
    deficit: float | None = None


class UchastnikBP(BaseModel):
    inn: str
    nazvanie: str
    tip_uchastnika: str = ""
    byudzhet: str = ""


class SvedeniyaUchrezhdeniya(BaseModel):
    inn: str
    nazvanie: str
    tip: str = ""
    osnovnoj_vid_deyatelnosti: str = ""
    osnovanie: str = ""


class MezhbyudzhetnyyTransfer(BaseModel):
    vid: str
    otpravitel: str = ""
    poluchatel: str = ""
    summa: float | None = None
    god: str = ""
