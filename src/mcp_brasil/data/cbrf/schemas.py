"""Pydantic schemas for the CBRF (Central Bank of Russia) feature."""

from __future__ import annotations

from pydantic import BaseModel


class ValorMoeda(BaseModel):
    """Значение одной валюты на определённую дату."""

    codigo: str
    nome: str
    nominal: int
    valor: float
    valor_anterior: float | None = None
    data: str = ""


class DadosMoeda(BaseModel):
    """Полные данные по валюте из API ЦБ РФ."""

    code: str
    name: str
    nominal: int
    value: float
    previous: float | None = None
    date: str = ""


class IndicadorEconomico(BaseModel):
    """Экономический показатель ЦБ РФ."""

    nome: str
    valor: float
    data: str
    unidade: str = ""
    fonte: str = "Центральный банк Российской Федерации"


class TaxaChave(BaseModel):
    """Ключевая ставка ЦБ РФ."""

    valor: float
    data: str
    data_anterior: str | None = None
    valor_anterior: float | None = None
    diferenca: float | None = None
    fonte: str = "Центральный банк Российской Федерации"
