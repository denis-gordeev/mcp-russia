"""Pydantic-схемы для модуля Счётного суда Сан-Паулу (TCE-SP, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Municipio(BaseModel):
    """Муниципалитет под юрисдикцией TCE-SP (legacy -- Brazil)."""

    municipio: str  # slug (ex: "campinas")
    municipio_extenso: str  # полное название (ex: "Campinas")


class Despesa(BaseModel):
    """Муниципальный расход, зарегистрированный в TCE-SP (legacy -- Brazil)."""

    orgao: str | None = None
    mes: str | None = None
    evento: str | None = None  # Empenhado, Valor Pago, Valor Liquidado, Anulacao
    nr_empenho: str | None = None
    id_fornecedor: str | None = None
    nm_fornecedor: str | None = None
    dt_emissao_despesa: str | None = None
    vl_despesa: float | None = None  # преобразовано из бразильского формата


class Receita(BaseModel):
    """Муниципальный доход, зарегистрированный в TCE-SP (legacy -- Brazil)."""

    orgao: str | None = None
    mes: str | None = None
    ds_fonte_recurso: str | None = None
    ds_cd_aplicacao_fixo: str | None = None
    ds_alinea: str | None = None
    ds_subalinea: str | None = None
    vl_arrecadacao: float | None = None  # преобразовано из бразильского формата
