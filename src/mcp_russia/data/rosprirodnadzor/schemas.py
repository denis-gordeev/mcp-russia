"""Схемы Pydantic модуля Росприроднадзора."""

from __future__ import annotations

from pydantic import BaseModel


class ProverkaEkologicheskaya(BaseModel):
    nomer: str
    organizaciya: str = ""
    vid_nadzora: str = ""
    data_nachala: str = ""
    data_okonchaniya: str = ""
    sostoyanie: str = ""
    vyavleno_narusheniy: int = 0


class ObektNegativnogoVozdeystviya(BaseModel):
    nomer: str
    nazvanie: str = ""
    kategoriya: str = ""
    subiekt: str = ""
    vid_deyatelnosti: str = ""


class LitsenziyaNedropolzovanie(BaseModel):
    nomer: str
    vid_litsenzii: str = ""
    territoriya: str = ""
    srok_deystviya: str = ""
    derzhatel: str = ""


class EkologicheskiyPlatezh(BaseModel):
    nomer: str
    tip_platezha: str = ""
    summa: float | None = None
    god: str = ""
    platelshchik: str = ""
