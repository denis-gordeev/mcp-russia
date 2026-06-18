"""Схемы Pydantic модуля РосАПИ."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AdresRF(BaseModel):
    """Адрес, возвращаемый при запросе по почтовому индексу или ФИАС."""

    pochtovyy_indeks: str = Field(description="Почтовый индекс (6 цифр)")
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
    nazvanie_polnoe: str | None = None
    nazvanie_kratkoe: str | None = None
    status: str | None = Field(default=None, description="Статус: ACTIVE, LIQUIDATED и т.д.")
    address: str | None = None
    director: str | None = None
    data_registratsii: str | None = None


class BankRF(BaseModel):
    """Справочные данные российского банка."""

    bik: str = Field(description="БИК банка (9 цифр)")
    nazvanie: str
    nazvanie_kratkoe: str | None = None
    city: str | None = None
    region: str | None = None
    phone: str | None = None
    swift: str | None = None


class Prazdnik(BaseModel):
    """Национальный праздник РФ."""

    data: str = Field(description="Дата (YYYY-MM-DD)")
    nazvanie: str
    type: str = Field(description="Тип: национальный, профессиональный, памятный")


class PostalCodeInfo(BaseModel):
    """Информация о почтовом индексе."""

    kod: str = Field(description="Почтовый индекс (6 цифр)")
    region: str
    city: str
    district: str | None = None
    addresses: list[str] = Field(description="Список обслуживаемых адресов")
