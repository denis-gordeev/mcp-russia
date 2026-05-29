"""Pydantic-схемы для модуля закупок PNCP (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Contratacao(BaseModel):
    """Государственная закупка, возвращаемая PNCP (legacy -- Brazil)."""

    orgao_cnpj: str | None = None
    orgao_nome: str | None = None
    ano: int | None = None
    numero_sequencial: int | None = None
    numero_controle_pncp: str | None = None
    objeto: str | None = None
    modalidade_id: int | None = None
    modalidade_nome: str | None = None
    situacao_id: int | None = None
    situacao_nome: str | None = None
    valor_estimado: float | None = None
    valor_homologado: float | None = None
    data_publicacao: str | None = None
    data_abertura: str | None = None
    uf: str | None = None
    municipio: str | None = None
    esfera: str | None = None
    link_pncp: str | None = None


class ContratacaoResultado(BaseModel):
    """Страничный результат поиска закупок (legacy -- Brazil)."""

    total: int = 0
    contratacoes: list[Contratacao] = []


class Contrato(BaseModel):
    """Государственный контракт (legacy -- Brazil)."""

    orgao_cnpj: str | None = None
    orgao_nome: str | None = None
    numero_contrato: str | None = None
    objeto: str | None = None
    fornecedor_cnpj: str | None = None
    fornecedor_nome: str | None = None
    valor_inicial: float | None = None
    valor_final: float | None = None
    vigencia_inicio: str | None = None
    vigencia_fim: str | None = None
    data_publicacao: str | None = None
    situacao: str | None = None


class ContratoResultado(BaseModel):
    """Страничный результат поиска контрактов (legacy -- Brazil)."""

    total: int = 0
    contratos: list[Contrato] = []


class AtaRegistroPreco(BaseModel):
    """Протокол регистрации цен (legacy -- Brazil)."""

    orgao_cnpj: str | None = None
    orgao_nome: str | None = None
    numero_ata: str | None = None
    objeto: str | None = None
    fornecedor_cnpj: str | None = None
    fornecedor_nome: str | None = None
    valor_total: float | None = None
    vigencia_inicio: str | None = None
    vigencia_fim: str | None = None
    situacao: str | None = None


class AtaResultado(BaseModel):
    """Страничный результат поиска протоколов (legacy -- Brazil)."""

    total: int = 0
    atas: list[AtaRegistroPreco] = []


class Fornecedor(BaseModel):
    """Поставщик государственных закупок (legacy -- Brazil)."""

    cnpj: str | None = None
    razao_social: str | None = None
    nome_fantasia: str | None = None
    municipio: str | None = None
    uf: str | None = None
    porte: str | None = None
    data_abertura: str | None = None


class FornecedorResultado(BaseModel):
    """Страничный результат поиска поставщиков (legacy -- Brazil)."""

    total: int = 0
    fornecedores: list[Fornecedor] = []


class OrgaoContratante(BaseModel):
    """Закупающий орган в PNCP (legacy -- Brazil)."""

    cnpj: str | None = None
    razao_social: str | None = None
    esfera: str | None = None
    poder: str | None = None
    uf: str | None = None
    municipio: str | None = None


class OrgaoResultado(BaseModel):
    """Страничный результат поиска органов (legacy -- Brazil)."""

    total: int = 0
    orgaos: list[OrgaoContratante] = []
