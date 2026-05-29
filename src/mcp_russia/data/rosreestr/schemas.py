"""Pydantic schemas for the Росреестр feature."""

from __future__ import annotations

from pydantic import BaseModel


class KadastrovyyObekt(BaseModel):
    """Кадастровый объект недвижимости."""

    kadastrovyy_nomer: str
    tip_obekta: str = ""
    adreshnye_svedeniya: str = ""
    ploshchad: str = ""
    kadastrovaya_stoimost: str = ""
    data_opredeleniya_stoimosti: str = ""
    status_ucheta: str = ""
    kategoriya_zemel: str = ""


class ZemelnyyUchastok(BaseModel):
    """Земельный участок."""

    kadastrovyy_nomer: str
    adreshnye_svedeniya: str = ""
    ploshchad: float | None = None
    edinitsa_izmereniya: str = "кв.м"
    kategoriya_zemel: str = ""
    vid_ispolzovaniya: str = ""
    kadastrovaya_stoimost: float | None = None
    forma_sobstvennosti: str = ""


class Zdanie(BaseModel):
    """Здание."""

    kadastrovyy_nomer: str
    adreshnye_svedeniya: str = ""
    ploshchad: float | None = None
    etazhnost: int | None = None
    god_vvoda_v_ekspluataciyu: str = ""
    material_sten: str = ""
    kadastrovaya_stoimost: float | None = None
    naznachenie: str = ""


class Pomeshchenie(BaseModel):
    """Помещение (квартира, офис и т.д.)."""

    kadastrovyy_nomer: str
    adreshnye_svedeniya: str = ""
    ploshchad: float | None = None
    naznachenie: str = ""
    etazh: int | None = None
    kadastrovaya_stoimost: float | None = None
    tip_pomeshcheniya: str = ""


class KadastrovayaStoimost(BaseModel):
    """Кадастровая стоимость объекта."""

    kadastrovyy_nomer: str
    stoimost: float | None = None
    data_opredeleniya: str = ""
    data_vneseniya_v_egrn: str = ""
    osnovanie: str = ""
