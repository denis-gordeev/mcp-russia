"""Схемы Pydantic модуля Картотеки арбитражных дел."""

from __future__ import annotations

from pydantic import BaseModel


class SudebnoeDelo(BaseModel):
    """Судебное дело в Картотеке арбитражных дел."""

    number: str  # номер дела (например, А40-12345/2024)
    category: str = ""
    status: str = ""
    sudya: str = ""
    nazvanie_suda: str = ""
    data_vozbuzhdeniya: str = ""
    data_poslednego_akta: str = ""
    istorcy: list[str] = []
    otvetchiki: list[str] = []
    summa_iska: float = 0.0
    currency: str = "RUB"


class SudebnyyAkt(BaseModel):
    """Судебный акт (решение, определение, постановление)."""

    id: str
    delo_number: str
    tip_akta: str  # решение, определение, постановление
    data_akta: str = ""
    sud: str = ""
    sudya: str = ""
    kratkoe_soderzhanie: str = ""
    rezolyutsiya: str = ""
    pdf_url: str = ""


class SudebnoeZasedanie(BaseModel):
    """Судебное заседание."""

    id: str
    delo_number: str
    data_zasedaniya: str
    vremya: str = ""
    sudya: str = ""
    zala: str = ""
    status: str = ""  # назначено, отложено, состоялось
    rezultaty: str = ""


class Sudy(BaseModel):
    """Судья арбитражного суда."""

    id: str
    familiya_imya: str
    nazvanie_suda: str = ""
    dolzhnost: str = ""  # председатель, судья
    del_rassmotreno: int = 0


class StoronaDela(BaseModel):
    """Сторона судебного дела (истец/ответчик)."""

    nazvanie: str
    inn: str = ""
    tip: str = ""  # "истец" или "ответчик"
    region: str = ""
    predstavitelem: str = ""
