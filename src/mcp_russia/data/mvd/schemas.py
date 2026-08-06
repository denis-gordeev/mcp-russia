"""Схемы Pydantic модуля МВД России."""

from __future__ import annotations

from pydantic import BaseModel


class StatistikaPrestupnosti(BaseModel):
    god: int = 0
    subiekt: str = ""
    zaregistrirovano: int = 0
    raskryto: int = 0
    neraskryto: int = 0
    tyazhkie_osobo_tyazhkie: int = 0
    istochnik: str = "МВД России (мвд.рф)"


class StatistikaDTP(BaseModel):
    god: int = 0
    subiekt: str = ""
    vsego_dtp: int = 0
    pogibshikh: int = 0
    postradavshikh: int = 0
    istochnik: str = "МВД России (мвд.рф)"


class RozyskDelo(BaseModel):
    nomer_dela: str = ""
    kategoriya: str = ""
    subiekt: str = ""
    data_vozbuzhdeniya: str = ""
    opisanie: str = ""
    istochnik: str = "МВД России (мвд.рф)"


class NarkotikiZapis(BaseModel):
    subiekt: str = ""
    vid_prestupleniya: str = ""
    kolichestvo_prestupleniy: int = 0
    izyato_gramm: float = 0.0
    vid_narkotika: str = ""
    istochnik: str = "МВД России (мвд.рф)"
