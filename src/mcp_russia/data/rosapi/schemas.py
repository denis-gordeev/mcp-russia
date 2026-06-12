"""Схемы Pydantic модуля РосАПИ."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AdresRF(BaseModel):
    """Адрес, возвращаемый при запросе по почтовому индексу или ФИАС."""

    postal_code: str = Field(description="Почтовый индекс (6 цифр)")
    region: str = Field(description="Субъект РФ (область, край, республика)")
    city: str = Field(description="Город/населённый пункт")
    street: str | None = None
    house: str | None = None
    full_address: str = Field(description="Полный адрес одной строкой")


class Organizatsiya(BaseModel):
    """Данные организации, возвращаемые при запросе по ИНН/ОГРН."""

    inn: str = Field(description="ИНН (10 или 12 цифр)")
    kpp: str | None = Field(default=None, description="КПП (9 цифр)")
    ogrn: str | None = Field(default=None, description="ОГРН (13 или 15 цифр)")
    name_full: str | None = None
    name_short: str | None = None
    status: str | None = Field(default=None, description="Статус: ACTIVE, LIQUIDATED, etc.")
    address: str | None = None
    director: str | None = None
    registration_date: str | None = None


class BankRF(BaseModel):
    """Справочные данные российского банка."""

    bik: str = Field(description="БИК банка (9 цифр)")
    name: str
    name_short: str | None = None
    city: str | None = None
    region: str | None = None
    phone: str | None = None
    swift: str | None = None


class Prazdnik(BaseModel):
    """Национальный праздник РФ."""

    date: str = Field(description="Дата (YYYY-MM-DD)")
    name: str
    type: str = Field(description="Тип: national, professional, memorial")


class PostalCodeInfo(BaseModel):
    """Информация о почтовом индексе."""

    code: str = Field(description="Почтовый индекс (6 цифр)")
    region: str
    city: str
    district: str | None = None
    addresses: list[str] = Field(description="Список обслуживаемых адресов")
