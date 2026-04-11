"""Pydantic-схемы для модуля Счётного суда Сеары (TCE-CE, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Municipio(BaseModel):
    """Муниципалитет Сеары под юрисдикцией TCE-CE (legacy -- Brazil)."""

    codigo_municipio: str | None = None
    nome_municipio: str | None = None


class Licitacao(BaseModel):
    """Муниципальный тендер в Сеаре (legacy -- Brazil)."""

    codigo_municipio: str | None = None
    numero_licitacao: str | None = None
    data_realizacao: str | None = None
    modalidade_licitacao: str | None = None
    objeto: str | None = None
    valor_orcado_estimado: float | None = None
    data_homologacao: str | None = None
    nome_responsavel_homologacao: str | None = None
    modalidade_processo_administrativo: str | None = None


class Contrato(BaseModel):
    """Муниципальный контракт в Сеаре (legacy -- Brazil)."""

    codigo_municipio: str | None = None
    numero_contrato: str | None = None
    data_contrato: str | None = None
    tipo_contrato: str | None = None
    modalidade_contrato: str | None = None
    objeto: str | None = None
    valor_total_contrato: float | None = None
    data_inicio_vigencia: str | None = None
    data_fim_vigencia: str | None = None


class ContratoResultado(BaseModel):
    """Страничный результат поиска контрактов (legacy -- Brazil)."""

    contratos: list[Contrato] = []
    total: int = 0


class Empenho(BaseModel):
    """Муниципальное обязательство (nota de empenho) в Сеаре (legacy -- Brazil)."""

    codigo_municipio: int | None = None
    numero_empenho: str | None = None
    data_emissao: str | None = None
    valor_empenho: float | None = None
    nome_negociante: str | None = None
    numero_documento_negociante: str | None = None
    historico: str | None = None
    codigo_orgao: str | None = None
    codigo_funcao: str | None = None


class EmpenhoResultado(BaseModel):
    """Страничный результат поиска обязательств (legacy -- Brazil)."""

    empenhos: list[Empenho] = []
    total: int = 0
