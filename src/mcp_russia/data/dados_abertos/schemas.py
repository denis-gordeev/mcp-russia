"""Pydantic-схемы для модуля открытых данных (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class ConjuntoDados(BaseModel):
    """Набор данных портала открытых данных (legacy -- Brazil)."""

    id: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    organizacao_nome: str | None = None
    temas: list[str] = []
    tags: list[str] = []
    data_criacao: str | None = None
    data_atualizacao: str | None = None


class ConjuntoResultado(BaseModel):
    """Страничный результат поиска наборов данных (legacy -- Brazil)."""

    total: int = 0
    conjuntos: list[ConjuntoDados] = []


class Organizacao(BaseModel):
    """Организация, публикующая данные (legacy -- Brazil)."""

    id: str | None = None
    nome: str | None = None
    descricao: str | None = None
    total_conjuntos: int | None = None


class OrganizacaoResultado(BaseModel):
    """Страничный результат поиска организаций (legacy -- Brazil)."""

    total: int = 0
    organizacoes: list[Organizacao] = []


class RecursoDados(BaseModel):
    """Ресурс (файл/API) набора данных (legacy -- Brazil)."""

    id: str | None = None
    titulo: str | None = None
    link: str | None = None
    formato: str | None = None
    descricao: str | None = None


class RecursoResultado(BaseModel):
    """Страничный результат поиска ресурсов (legacy -- Brazil)."""

    total: int = 0
    recursos: list[RecursoDados] = []
