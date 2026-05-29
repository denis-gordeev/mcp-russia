"""Pydantic-схемы для модуля Счётного суда Пернамбуку (TCE-PE, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class UnidadeJurisdicionada(BaseModel):
    """Подсудная единица (мэрия, палата и т.д.) (legacy -- Brazil)."""

    codigo: str | None = None
    nome: str | None = None
    natureza: str | None = None
    municipio: str | None = None
    codigo_municipio: str | None = None


class Licitacao(BaseModel):
    """Тендер, зарегистрированный в TCE-PE (SAGRES/LICON) (legacy -- Brazil)."""

    numero_licitacao: str | None = None
    ano_licitacao: int | None = None
    modalidade: str | None = None
    objeto: str | None = None
    valor_estimado: float | None = None
    situacao: str | None = None
    municipio: str | None = None
    unidade_gestora: str | None = None
    id_unidade_gestora: int | None = None


class Contrato(BaseModel):
    """Контракт, зарегистрированный в TCE-PE (legacy -- Brazil)."""

    numero_contrato: str | None = None
    ano_referencia: int | None = None
    objeto: str | None = None
    valor_contrato: float | None = None
    fornecedor: str | None = None
    cpf_cnpj: str | None = None
    municipio: str | None = None
    unidade_gestora: str | None = None
    id_unidade_gestora: int | None = None


class Despesa(BaseModel):
    """Муниципальный расход, зарегистрированный в TCE-PE (legacy -- Brazil)."""

    numero_empenho: str | None = None
    ano_referencia: int | None = None
    mes_referencia: int | None = None
    fornecedor: str | None = None
    cpf_cnpj: str | None = None
    historico: str | None = None
    valor_empenhado: float | None = None
    valor_liquidado: float | None = None
    valor_pago: float | None = None
    funcao: str | None = None
    elemento_despesa: str | None = None
    unidade_gestora: str | None = None
    codigo_municipio: str | None = None


class Fornecedor(BaseModel):
    """Поставщик, зарегистрированный в TCE-PE (legacy -- Brazil)."""

    cpf_cnpj: str | None = None
    nome: str | None = None
    tipo_credor: int | None = None
