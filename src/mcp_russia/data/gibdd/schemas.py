"""Схемы Pydantic модуля ГИБДД/МВД."""

from __future__ import annotations

from pydantic import BaseModel


class TransportnoeSredstvo(BaseModel):
    """Транспортное средство."""

    gos_nomer: str = ""
    vin: str = ""
    marka_model: str = ""
    god_vypuska: int | None = None
    tip_ts: str = ""
    kuzov_nomer: str = ""
    dvigatel_nomer: str = ""
    moshchnost_ls: int | None = None
    obiem_sm3: int | None = None
    tip_dvigatelya: str = ""
    registratsionnaya_oblast: str = ""


class VoditelskoeUdostoverenie(BaseModel):
    """Водительское удостоверение."""

    nomer_vu: str = ""
    kategoriya: str = ""
    data_vydachi: str = ""
    srok_deystviya: str = ""
    fio: str = ""
    mesto_rozhdeniya: str = ""
    ograniceniya: str = ""
    osoboie_otmetki: str = ""
    sostoyanie: str = ""


class ShtrafGIBDD(BaseModel):
    """Штраф ГИБДД."""

    postanovlenie_nomer: str = ""
    data_narusheniya: str = ""
    statya_koap: str = ""
    opisanie_narusheniya: str = ""
    summa_shtrafa: float | None = None
    skidka_50: bool = False
    sostoyanie_oplaty: str = ""
    data_oplaty: str = ""
    mesto_narusheniya: str = ""


class StatistikaDTP(BaseModel):
    """Статистика ДТП по региону."""

    subiekt: str = ""
    god: int = 0
    kolichestvo_dtp: int = 0
    pogibshie: int = 0
    ranennye: int = 0
    dtp_s_peshchodami: int = 0
    dtp_s_detmi: int = 0
    alco_gibdd: int = 0


class RegistratsionnoeDeystvie(BaseModel):
    """Регистрационное действие с ТС."""

    vin: str = ""
    gos_nomer: str = ""
    tip_deystviya: str = ""
    data_deystviya: str = ""
    subiekt: str = ""
