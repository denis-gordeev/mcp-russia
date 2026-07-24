"""Схемы Pydantic модуля Счётной палаты РФ."""

from __future__ import annotations

from pydantic import BaseModel


class KontrolnoeMeropriyatie(BaseModel):
    """Контрольное мероприятие Счётной палаты."""

    nomer: str
    nazvanie: str
    tip: str = ""
    napravlenie: str = ""
    data_nachala: str = ""
    data_okonchaniya: str = ""
    sostoyanie: str = ""
    obiem_sredstv: float | None = None
    valyuta: str = "руб."


class AuditorskoeZaklyuchenie(BaseModel):
    """Аудиторское заключение."""

    nomer: str
    nazvanie: str
    data_publikatsii: str = ""
    obekt_audita: str = ""
    napravlenie: str = ""
    vyavleno_narusheniy: int = 0
    summa_narusheniy: float | None = None
    rekomendatsii: list[str] = []
    ispolnenie: str = ""


class Narushenie(BaseModel):
    """Выявленное нарушение."""

    opisanie: str
    summa: float | None = None
    valyuta: str = "руб."
    tip_narusheniya: str = ""
    organizatsiya: str = ""
    norma_prava: str = ""


class ByudzhetIspolnenie(BaseModel):
    """Данные об исполнении федерального бюджета."""

    period: str
    dohody: float | None = None
    raskhody: float | None = None
    defitsit: float | None = None
    istochnik: str = "Счётная палата РФ"
