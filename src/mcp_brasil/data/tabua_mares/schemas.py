"""Pydantic-схемы для модуля таблицы приливов (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GeoLocalizacao(BaseModel):
    """Географические координаты порта (legacy -- Brazil)."""

    lat: str
    lng: str
    decimal_lat: str = Field(
        description="Широта в формате градусы/минуты (напр.: 09 41' S) (legacy -- Brazil)"
    )
    decimal_lng: str = Field(
        description="Долгота в формате градусы/минуты (напр.: 35 43'.5 W) (legacy -- Brazil)"
    )
    lat_direction: str
    lng_direction: str


class Porto(BaseModel):
    """Подробная информация о порте (legacy -- Brazil)."""

    id: int
    harbor_name: str
    state: str
    timezone: str
    card: str
    geo_location: list[GeoLocalizacao] = Field(default_factory=list)
    mean_level: float | None = Field(
        default=None, description="Средний уровень моря в метрах (legacy -- Brazil)"
    )


class PortoResumo(BaseModel):
    """Сокращённая информация о порте, возвращаемая списком по штатам (legacy -- Brazil)."""

    id: int
    year: int
    harbor_name: str
    data_collection_institution: str


class HoraMare(BaseModel):
    """Запись прилива за конкретный час (legacy -- Brazil)."""

    hour: str = Field(description="Время в формате ЧЧ:ММ:СС (legacy -- Brazil)")
    level: float = Field(description="Уровень прилива в метрах (legacy -- Brazil)")


class DiaMare(BaseModel):
    """Данные приливов за день (legacy -- Brazil)."""

    weekday_name: str
    day: int
    hours: list[HoraMare] = Field(default_factory=list)


class MesMare(BaseModel):
    """Данные приливов за месяц (legacy -- Brazil)."""

    month_name: str
    month: int
    days: list[DiaMare] = Field(default_factory=list)


class TabuaMare(BaseModel):
    """Полная таблица приливов для порта (legacy -- Brazil)."""

    year: int
    harbor_name: str
    state: str
    timezone: str
    card: str
    data_collection_institution: str
    mean_level: float
    months: list[MesMare] = Field(default_factory=list)
