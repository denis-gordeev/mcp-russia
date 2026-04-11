"""Pydantic-схемы для ответов API DataJud (CNJ, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Processo(BaseModel):
    """Судебное дело, возвращаемое API DataJud (legacy -- Brazil)."""

    numero: str | None = None
    classe: str | None = None
    assunto: str | None = None
    tribunal: str | None = None
    orgao_julgador: str | None = None
    data_ajuizamento: str | None = None
    data_ultima_atualizacao: str | None = None
    grau: str | None = None
    nivel_sigilo: int | None = None
    formato_numero: str | None = None


class Movimentacao(BaseModel):
    """Движение судебного дела (legacy -- Brazil)."""

    data: str | None = None
    nome: str | None = None
    codigo: int | None = None
    complemento: str | None = None


class Assunto(BaseModel):
    """Предмет судебного спора (legacy -- Brazil)."""

    codigo: int | None = None
    nome: str | None = None


class Parte(BaseModel):
    """Сторона судебного дела (истец, ответчик и т.д.) (legacy -- Brazil)."""

    nome: str | None = None
    tipo: str | None = None
    polo: str | None = None
    documento: str | None = None


class ProcessoDetalhe(BaseModel):
    """Полная информация о судебном деле (legacy -- Brazil)."""

    numero: str | None = None
    classe: str | None = None
    assuntos: list[Assunto] | None = None
    tribunal: str | None = None
    orgao_julgador: str | None = None
    data_ajuizamento: str | None = None
    data_ultima_atualizacao: str | None = None
    grau: str | None = None
    partes: list[Parte] | None = None
    movimentacoes: list[Movimentacao] | None = None
    nivel_sigilo: int | None = None
