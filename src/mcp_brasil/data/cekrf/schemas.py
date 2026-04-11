"""Модели данных для модуля ЦИК РФ."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SubyektRF(BaseModel):
    """Субъект Российской Федерации."""

    code: str = Field(description="Код субъекта РФ")
    name: str = Field(description="Полное наименование субъекта")
    okato: str = Field(description="Код ОКАТО", default="")


class TipVyborov(BaseModel):
    """Тип выборов."""

    code: int = Field(description="Код типа выборов")
    name: str = Field(description="Наименование типа выборов")


class Dolzhnost(BaseModel):
    """Избирательная должность."""

    code: int = Field(description="Код должности")
    name: str = Field(description="Наименование должности")
    level: str = Field(description="Уровень (federal/regional/municipal)")


class KandidatResumo(BaseModel):
    """Краткая информация о кандидате."""

    id: str = Field(description="ID кандидата")
    fio: str = Field(description="ФИО кандидата")
    partia: str = Field(description="Партия / статус выдвижения", default="")
    dolzhnost: str = Field(description="Избирательная должность")
    region: str = Field(description="Субъект РФ / округ", default="")
    status: str = Field(description="Статус (зарегистрирован/снят/исключён)", default="")


class Kandidat(BaseModel):
    """Полная информация о кандидате."""

    id: str = Field(description="ID кандидата")
    fio: str = Field(description="ФИО")
    data_rozhdeniya: str = Field(description="Дата рождения", default="")
    mesto_rozhdeniya: str = Field(description="Место рождения", default="")
    partia: str = Field(description="Партия / статус выдвижения", default="")
    dolzhnost: str = Field(description="Избирательная должность")
    region: str = Field(description="Субъект РФ / округ", default="")
    status: str = Field(description="Статус", default="")
    obrazovanie: str = Field(description="Образование", default="")
    mesto_raboty: str = Field(description="Место работы", default="")
    dolzhnost_rabota: str = Field(description="Должность на момент выдвижения", default="")
    dokhod: str = Field(description="Декларированный доход", default="")
    scheta: str = Field(description="Счета в банках", default="")
    nedvizhimost: str = Field(description="Недвижимость", default="")
    transport: str = Field(description="Транспортные средства", default="")


class ResultatKandidata(BaseModel):
    """Результат кандидата по итогам голосования."""

    kandidat_id: str = Field(description="ID кандидата")
    fio: str = Field(description="ФИО")
    partia: str = Field(description="Партия", default="")
    golosov: int = Field(description="Число голосов", default=0)
    procent: float = Field(description="Процент голосов", default=0.0)
    izbrann: bool = Field(description="Избран/не избран", default=False)
    yavka_procent: float = Field(description="Явка избирателей, %", default=0.0)


class ItogiVYborov(BaseModel):
    """Итоги выборов."""

    tip: str = Field(description="Тип выборов")
    data: str = Field(description="Дата голосования")
    region: str = Field(description="Субъект РФ / регион", default="")
    yavka_procent: float = Field(description="Явка избирателей, %", default=0.0)
    vseh_izbirateley: int = Field(description="Всего избирателей", default=0)
    progalosovalo: int = Field(description="Проголосовало", default=0)
    deystvitelnykh_byulleteney: int = Field(description="Действительных бюллетеней", default=0)
    nedeystvitelnykh_byulleteney: int = Field(description="Недействительных бюллетеней", default=0)


class PartiaInfo(BaseModel):
    """Информация о политической партии."""

    name: str = Field(description="Полное наименование партии")
    short_name: str = Field(description="Краткое наименование")
    color: str = Field(description="Цвет партии (hex)", default="")
    registraciya: str = Field(description="Номер регистрации Минюста", default="")
