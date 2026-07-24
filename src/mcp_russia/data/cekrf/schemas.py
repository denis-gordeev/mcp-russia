"""Модели данных для модуля ЦИК РФ."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SubiektRF(BaseModel):
    """Субъект Российской Федерации."""

    kod: str = Field(description="Код субъекта РФ")
    nazvanie: str = Field(description="Полное наименование субъекта")
    okato: str = Field(description="Код ОКАТО", default="")


class TipVyborov(BaseModel):
    """Тип выборов."""

    kod: int = Field(description="Код типа выборов")
    nazvanie: str = Field(description="Наименование типа выборов")


class Dolzhnost(BaseModel):
    """Избирательная должность."""

    kod: int = Field(description="Код должности")
    nazvanie: str = Field(description="Наименование должности")
    uroven: str = Field(description="Уровень (федеральный/региональный/муниципальный)")


class KandidatKratko(BaseModel):
    """Краткая информация о кандидате."""

    identifikator: str = Field(description="Идентификатор кандидата")
    fio: str = Field(description="ФИО кандидата")
    partiya: str = Field(description="Партия / статус выдвижения", default="")
    dolzhnost: str = Field(description="Избирательная должность")
    subiekt: str = Field(description="Субъект РФ / округ", default="")
    sostoyanie: str = Field(description="Состояние (зарегистрирован/снят/исключён)", default="")


class Kandidat(BaseModel):
    """Полная информация о кандидате."""

    identifikator: str = Field(description="Идентификатор кандидата")
    fio: str = Field(description="ФИО")
    data_rozhdeniya: str = Field(description="Дата рождения", default="")
    mesto_rozhdeniya: str = Field(description="Место рождения", default="")
    partiya: str = Field(description="Партия / статус выдвижения", default="")
    dolzhnost: str = Field(description="Избирательная должность")
    subiekt: str = Field(description="Субъект РФ / округ", default="")
    sostoyanie: str = Field(description="Состояние", default="")
    obrazovanie: str = Field(description="Образование", default="")
    mesto_raboty: str = Field(description="Место работы", default="")
    dolzhnost_rabota: str = Field(description="Должность на момент выдвижения", default="")
    dokhod: str = Field(description="Декларированный доход", default="")
    scheta: str = Field(description="Счета в банках", default="")
    nedvizhimost: str = Field(description="Недвижимость", default="")
    transport: str = Field(description="Транспортные средства", default="")


class ResultatKandidata(BaseModel):
    """Результат кандидата по итогам голосования."""

    kandidat_identifikator: str = Field(description="Идентификатор кандидата")
    fio: str = Field(description="ФИО")
    partiya: str = Field(description="Партия", default="")
    golosov: int = Field(description="Число голосов", default=0)
    protsent: float = Field(description="Процент голосов", default=0.0)
    izbrann: bool = Field(description="Избран/не избран", default=False)
    yavka_protsent: float = Field(description="Явка избирателей, %", default=0.0)


class ItogiVYborov(BaseModel):
    """Итоги выборов."""

    tip: str = Field(description="Тип выборов")
    data: str = Field(description="Дата голосования")
    subiekt: str = Field(description="Субъект РФ", default="")
    yavka_protsent: float = Field(description="Явка избирателей, %", default=0.0)
    vseh_izbirateley: int = Field(description="Всего избирателей", default=0)
    progalosovalo: int = Field(description="Проголосовало", default=0)
    deystvitelnykh_byulleteney: int = Field(description="Действительных бюллетеней", default=0)
    nedeystvitelnykh_byulleteney: int = Field(description="Недействительных бюллетеней", default=0)


class InformatsiyaPartii(BaseModel):
    """Информация о политической партии."""

    nazvanie: str = Field(description="Полное наименование партии")
    kratkoe_nazvanie: str = Field(description="Краткое наименование")
    tsvet: str = Field(description="Цвет партии (HEX)", default="")
    registratsiya: str = Field(description="Номер регистрации Минюста", default="")
