"""Схемы Pydantic модуля Росгидромета."""

from __future__ import annotations

from pydantic import BaseModel


class PogodaDannye(BaseModel):
    """Данные о погоде."""

    stantsiya: str = ""
    gorod: str = ""
    subiekt: str = ""
    temperatura: float | None = None
    oshchushchaetsya_kak: float | None = None
    vlazhnost: float | None = None
    davlenie: float | None = None
    veter_skorost: float | None = None
    veter_napravlenie: str = ""
    osadki: float | None = None
    vidimost: float | None = None
    opisaniye: str = ""
    data_vremya: str = ""


class PrognozDannye(BaseModel):
    """Прогноз погоды."""

    gorod: str = ""
    data: str = ""
    temperatura_dnem: float | None = None
    temperatura_nochyu: float | None = None
    osadki_veroyatnost: float | None = None
    veter_skorost: float | None = None
    opisaniye: str = ""


class EkologiyaDannye(BaseModel):
    """Данные об экологической обстановке."""

    gorod: str = ""
    stantsiya: str = ""
    tip: str = ""  # воздух, вода, почва, радиация, шум
    pokazatel: str = ""
    znachenie: float | None = None
    norma_max: float | None = None
    norma_min: float | None = None
    prevyshenie: bool = False
    data_izmereniya: str = ""


class Preduprezhdenie(BaseModel):
    """Предупреждение об опасном явлении."""

    tip: str = ""
    subiekt: str = ""
    gorod: str = ""
    opisanie: str = ""
    data_nachala: str = ""
    data_okonchaniya: str = ""
    uroven_opasnosti: str = ""  # низкий, средний, высокий, экстремальный


class SputnikovyyMonitoring(BaseModel):
    """Данные спутникового мониторинга."""

    sputnik: str = ""
    data_syomki: str = ""
    subiekt: str = ""
    tip_dannykh: str = ""  # леса, вода, пожары, снежный покров
    razreshenie: str = ""
    izobrazhenie_ssylka: str = ""
