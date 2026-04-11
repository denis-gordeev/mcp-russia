"""Pydantic-схемы для ответов API ANA (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Estacao(BaseModel):
    """Гидрологическая станция ANA (Hidroweb) (legacy -- Brazil)."""

    codigo_estacao: str
    nome_estacao: str
    codigo_rio: str = ""
    nome_rio: str = ""
    bacia: str = ""
    sub_bacia: str = ""
    municipio: str = ""
    estado: str = ""
    latitude: float | None = None
    longitude: float | None = None
    tipo_estacao: str = ""
    responsavel: str = ""


class DadoTelemetria(BaseModel):
    """Телеметрические данные станции (уровень, расход, осадки) (legacy -- Brazil)."""

    codigo_estacao: str
    data_hora: str
    nivel: float | None = None
    vazao: float | None = None
    chuva: float | None = None


class Reservatorio(BaseModel):
    """Данные мониторинга водохранилища (SAR/ANA) (legacy -- Brazil)."""

    nome_reservatorio: str
    rio: str = ""
    estado: str = ""
    data: str = ""
    volume_util: float | None = None
    cota_atual: float | None = None
    vazao_afluente: float | None = None
    vazao_defluente: float | None = None
