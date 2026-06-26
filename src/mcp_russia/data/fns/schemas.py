"""Схемы Pydantic модуля ФНС."""

from __future__ import annotations

from pydantic import BaseModel


class OrganizaciyaEGRUL(BaseModel):
    """Организация из ЕГРЮЛ."""

    inn: str
    ogrn: str = ""
    nazvanie: str = ""
    polnoe_nazvanie: str = ""
    yuridicheskiy_adres: str = ""
    data_registracii: str = ""
    sostoyanie: str = ""
    vid_deyatelnosti: str = ""
    ustroyennyy_kapital: str = ""
    rukovoditel: str = ""


class IPEGRIP(BaseModel):
    """Индивидуальный предприниматель из ЕГРИП."""

    inn: str
    ogrnip: str = ""
    fio: str = ""
    data_registracii: str = ""
    sostoyanie: str = ""
    vid_deyatelnosti: str = ""


class NalogovayaProverka(BaseModel):
    """Налоговая проверка."""

    nomer: str
    tip_proverki: str = ""
    period_proverki: str = ""
    data_nachala: str = ""
    data_okonchaniya: str = ""
    sostoyanie: str = ""
    vyavleno_narusheniy: int = 0
    summa_dochnachisleniy: float | None = None


class NalogovoeNachislenie(BaseModel):
    """Налоговое начисление."""

    inn: str
    vid_naloga: str = ""
    period: str = ""
    summa: float | None = None
    status_oplaty: str = ""
    zadolzhennost: float | None = None


class SvedeniyaOrganizacii(BaseModel):
    """Сводные сведения об организации."""

    inn: str
    nazvanie: str = ""
    registracionnyy_nomer: str = ""
    data_postanovki_na_uchet: str = ""
    nalogovyy_organ: str = ""
    rezhim_nalogooblozheniya: str = ""
    srednespisochnaya_chislennost: int | None = None
