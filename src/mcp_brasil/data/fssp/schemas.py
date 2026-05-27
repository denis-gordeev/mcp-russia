"""Pydantic schemas for the ФССП feature."""

from __future__ import annotations

from pydantic import BaseModel


class IspolnitelnoeProizvodstvo(BaseModel):
    """Исполнительное производство."""
    nomer: str
    tip_proizvodstva: str = ""
    dolzhnik: str = ""
    vzyskatel: str = ""
    summa_vzyskaniya: float | None = None
    ostatok_dolga: float | None = None
    status: str = ""
    data_vozbuzhdeniya: str = ""
    osnovanie: str = ""
    otdel_pristavov: str = ""


class SvedeniyaDolzhnika(BaseModel):
    """Сведения о должнике."""
    fio_nazvanie: str
    inn: str = ""
    tip_dolzhnika: str = ""
    kolichestvo_proizvodstv: int = 0
    obschaya_summa_dolga: float | None = None
    ogranicheniya: list[str] = []


class Ogranichenie(BaseModel):
    """Ограничение, наложенное судебным приставом."""
    tip_ogranicheniya: str
    osnovanie: str = ""
    data_nalozheniya: str = ""
    srok: str = ""
    nomer_proizvodstva: str = ""


class Rosysk(BaseModel):
    """Сведения о розыске."""
    tip_rozyska: str
    obekt_rozyska: str = ""
    osnovanie: str = ""
    data_obyavleniya: str = ""
    kto_obyavil: str = ""
