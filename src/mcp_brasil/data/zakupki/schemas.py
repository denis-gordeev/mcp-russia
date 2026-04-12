"""Pydantic schemas for the Zakupki (ЕИС закупок) feature."""

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
    publish_date: str = ""
    deadline: str = ""
    organizer_name: str = ""
    organizer_inn: str = ""


class Kontrakt(BaseModel):
    """Контракт в реестре контрактов."""

    id: str
    number: str = ""
    zakupka_number: str = ""
    contractor_name: str = ""
    contractor_inn: str = ""
    price: float = 0.0
    currency: str = "RUB"
    sign_date: str = ""
    status: str = ""
    execution_deadline: str = ""


class Zakazchik(BaseModel):
    """Заказчик (государственный/муниципальный орган)."""

    id: str
    name: str
    inn: str = ""
    kpp: str = ""
    region: str = ""
    adres: str = ""
    zakupki_count: int = 0
    total_spent: float = 0.0


class Postavshchik(BaseModel):
    """Поставщик (участник закупки)."""

    id: str
    name: str
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
    organizer_name: str = ""
    organizer_inn: str = ""
    items_count: int = 0
    total_budget: float = 0.0
    created_date: str = ""
    updated_date: str = ""
