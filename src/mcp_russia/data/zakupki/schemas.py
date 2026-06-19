"""Схемы Pydantic модуля ЕИС Закупок."""

from __future__ import annotations

from pydantic import BaseModel


class Zakupka(BaseModel):
    """Закупка в ЕИС."""

    identifikator: str
    nomer: str = ""
    nazvanie: str
    zakon: str = ""
    sposob: str = ""
    status: str = ""
    nachalnaya_tsena: float = 0.0
    valyuta: str = "RUB"
    data_publikatsii: str = ""
    srok_podachi: str = ""
    nazvanie_organizatora: str = ""
    organizator_inn: str = ""


class Kontrakt(BaseModel):
    """Контракт в реестре контрактов."""

    identifikator: str
    nomer: str = ""
    zakupka_nomer: str = ""
    nazvanie_podryadchika: str = ""
    podryadchik_inn: str = ""
    tsena: float = 0.0
    valyuta: str = "RUB"
    data_podpisaniya: str = ""
    status: str = ""
    srok_ispolneniya: str = ""


class Zakazchik(BaseModel):
    """Заказчик (государственный/муниципальный орган)."""

    identifikator: str
    nazvanie: str
    inn: str = ""
    kpp: str = ""
    region: str = ""
    adres: str = ""
    zakupki_kolichestvo: int = 0
    obshchie_raskhody: float = 0.0


class Postavshchik(BaseModel):
    """Поставщик (участник закупки)."""

    identifikator: str
    nazvanie: str
    inn: str = ""
    region: str = ""
    kontraktov_vyigrano: int = 0
    kontraktov_ispolneno: int = 0
    obshchiy_dokhod: float = 0.0
    is_dobrosovestny: bool = True


class PlanZakupki(BaseModel):
    """План-график закупки."""

    identifikator: str
    god: int
    nazvanie_organizatora: str = ""
    organizator_inn: str = ""
    kolichestvo_pozitsiy: int = 0
    obshchiy_byudzhet: float = 0.0
    data_sozdaniya: str = ""
    data_obnovleniya: str = ""
