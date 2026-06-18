"""Схемы Pydantic модуля ЕИС Закупок."""

from __future__ import annotations

from pydantic import BaseModel


class Zakupka(BaseModel):
    """Закупка в ЕИС."""

    id: str
    number: str = ""
    title: str
    zakon: str = ""  # "44-ФЗ" или "223-ФЗ"
    sposob: str = ""  # способ определения поставщика
    status: str = ""
    initial_price: float = 0.0
    currency: str = "RUB"
    data_publikatsii: str = ""
    deadline: str = ""
    nazvanie_organizatora: str = ""
    organizer_inn: str = ""


class Kontrakt(BaseModel):
    """Контракт в реестре контрактов."""

    id: str
    number: str = ""
    zakupka_number: str = ""
    nazvanie_podryadchika: str = ""
    contractor_inn: str = ""
    price: float = 0.0
    currency: str = "RUB"
    data_podpisaniya: str = ""
    status: str = ""
    execution_deadline: str = ""


class Zakazchik(BaseModel):
    """Заказчик (государственный/муниципальный орган)."""

    id: str
    nazvanie: str
    inn: str = ""
    kpp: str = ""
    region: str = ""
    adres: str = ""
    zakupki_count: int = 0
    total_spent: float = 0.0


class Postavshchik(BaseModel):
    """Поставщик (участник закупки)."""

    id: str
    nazvanie: str
    inn: str = ""
    region: str = ""
    contracts_won: int = 0
    contracts_executed: int = 0
    total_revenue: float = 0.0
    is_dobrosovestny: bool = True


class PlanZakupki(BaseModel):
    """План-график закупки."""

    id: str
    year: int
    nazvanie_organizatora: str = ""
    organizer_inn: str = ""
    items_count: int = 0
    total_budget: float = 0.0
    data_sozdaniya: str = ""
    data_obnovleniya: str = ""
