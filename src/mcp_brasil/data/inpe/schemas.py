"""Pydantic-схемы для ответов API INPE (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FocoQueimada(BaseModel):
    """Очаг пожара, обнаруженный спутником (legacy -- Brazil)."""

    id: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    data_hora: str = ""
    satelite: str = ""
    municipio: str = ""
    estado: str = ""
    bioma: str = ""
    dias_sem_chuva: int | None = None
    risco_fogo: float | None = None
    frp: float | None = Field(
        default=None, description="Мощность теплового излучения пожара (МВт) (legacy -- Brazil)"
    )


class AlertaDeter(BaseModel):
    """Предупреждение о вырубке леса DETER (legacy -- Brazil)."""

    id: str = ""
    data: str = ""
    area_km2: float = 0.0
    municipio: str = ""
    estado: str = ""
    bioma: str = ""
    classe: str = ""
    satelite: str = ""


class DadosProdes(BaseModel):
    """Исторические данные о вырубке леса PRODES (legacy -- Brazil)."""

    ano: int = 0
    bioma: str = ""
    area_km2: float = 0.0
    estado: str = ""
    municipio: str = ""


class Satelite(BaseModel):
    """Доступный спутник мониторинга (legacy -- Brazil)."""

    nome: str
    descricao: str = ""
