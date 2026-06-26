"""Схемы Pydantic модуля Картотеки арбитражных дел."""

from __future__ import annotations

from pydantic import BaseModel


class SudebnoeDelo(BaseModel):
    """Судебное дело в Картотеке арбитражных дел."""

    nomer: str
    kategoriya: str = ""
    sostoyanie: str = ""
    sudya: str = ""
    nazvanie_suda: str = ""
    data_vozbuzhdeniya: str = ""
    data_poslednego_akta: str = ""
    istorcy: list[str] = []
    otvetchiki: list[str] = []
    summa_iska: float = 0.0
    valyuta: str = "RUB"


class SudebnyyAkt(BaseModel):
    """Судебный акт (решение, определение, постановление)."""

    identifikator: str
    delo_nomer: str
    tip_akta: str
    data_akta: str = ""
    sud: str = ""
    sudya: str = ""
    kratkoe_soderzhanie: str = ""
    rezolyutsiya: str = ""
    pdf_ssylka: str = ""


class SudebnoeZasedanie(BaseModel):
    """Судебное заседание."""

    identifikator: str
    delo_nomer: str
    data_zasedaniya: str
    vremya: str = ""
    sudya: str = ""
    zala: str = ""
    sostoyanie: str = ""  # назначено, отложено, состоялось
    rezultaty: str = ""


class Sudy(BaseModel):
    """Судья арбитражного суда."""

    identifikator: str
    familiya_imya: str
    nazvanie_suda: str = ""
    dolzhnost: str = ""  # председатель, судья
    del_rassmotreno: int = 0


class StoronaDela(BaseModel):
    """Сторона судебного дела (истец/ответчик)."""

    nazvanie: str
    inn: str = ""
    tip: str = ""  # "истец" или "ответчик"
    subiekt: str = ""
    predstavitelem: str = ""
