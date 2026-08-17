"""Схемы Pydantic модуля Роспотребнадзора."""

from __future__ import annotations

from pydantic import BaseModel


class OrganNadzora(BaseModel):
    """Орган Роспотребнадзора (территориальное управление)."""

    kod: str
    nazvanie: str
    federalnyy_okrug: str = ""
    subiekt: str = ""
    telefon: str = ""
    elektronnaya_pochta: str = ""


class Proverka(BaseModel):
    """Проверка объекта надзора."""

    nomer: str
    tip_proverki: str = ""
    organizatsiya: str = ""
    data_nachala: str = ""
    data_okonchaniya: str = ""
    sostoyanie: str = ""
    vyavleno_narusheniy: int = 0
    rezulstat: str = ""


class NarushenieSanitarnoe(BaseModel):
    """Выявленное санитарное нарушение."""

    opisanie: str
    tip_narusheniya: str = ""
    organizatsiya: str = ""
    norma_prava: str = ""  # ссылка на СанПиН/нормативный акт
    predpisaniya: list[str] = []
    shtraf: float | None = None
    valyuta: str = "руб."


class PokazatelBezopasnosti(BaseModel):
    """Показатель безопасности (эпидемиологический, санитарный)."""

    kod: str
    nazvanie: str
    znachenie: float | None = None
    edinitsa_izmereniya: str = ""
    predelno_dopustimoe: float | None = None
    sostoyanie: str = ""  # возможные значения: «норма», «превышение», «понижение»


class ZhalobaPotrebitelya(BaseModel):
    """Жалоба потребителя, зарегистрированная в Роспотребнадзоре."""

    nomer: str
    tema: str = ""
    data_registratsii: str = ""
    sostoyanie_rassmotreniya: str = ""
    organizatsiya: str = ""
    rezulstat: str = ""
