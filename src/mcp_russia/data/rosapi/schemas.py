"""Схемы Pydantic модуля РосАПИ."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AdresRF(BaseModel):
    """Адрес, возвращаемый при запросе по почтовому индексу или ФИАС."""

    pochtovyy_indeks: str = Field(description="Почтовый индекс (6 цифр)")
    subiekt: str = Field(description="Субъект РФ (область, край, республика)")
    gorod: str = Field(description="Город/населённый пункт")
    ulitsa: str | None = None
    dom: str | None = None
    polnyy_adres: str = Field(description="Полный адрес одной строкой")


class Organizatsiya(BaseModel):
    """Данные организации, возвращаемые при запросе по ИНН/ОГРН."""

    inn: str = Field(description="ИНН (10 или 12 цифр)")
    kpp: str | None = Field(default=None, description="КПП (9 цифр)")
    ogrn: str | None = Field(default=None, description="ОГРН (13 или 15 цифр)")
    nazvanie_polnoe: str | None = None
    nazvanie_kratkoe: str | None = None
    sostoyanie: str | None = Field(
        default=None, description="Состояние: ДЕЙСТВУЮЩАЯ, ЛИКВИДИРОВАНА и т.д."
    )
    adres: str | None = None
    rukovoditel: str | None = None
    data_registratsii: str | None = None


class BankRF(BaseModel):
    """Справочные данные российского банка."""

    bik: str = Field(description="БИК банка (9 цифр)")
    nazvanie: str
    nazvanie_kratkoe: str | None = None
    gorod: str | None = None
    subiekt: str | None = None
    telefon: str | None = None
    svift: str | None = None


class Prazdnik(BaseModel):
    """Национальный праздник РФ."""

    data: str = Field(description="Дата (YYYY-MM-DD)")
    nazvanie: str
    tip: str = Field(description="Тип: национальный, профессиональный, памятный")


class InformatsiyaPochtovogoIndeksa(BaseModel):
    """Информация о почтовом индексе."""

    kod: str = Field(description="Почтовый индекс (6 цифр)")
    subiekt: str
    gorod: str
    rayon: str | None = None
    adresa: list[str] = Field(description="Список обслуживаемых адресов")
