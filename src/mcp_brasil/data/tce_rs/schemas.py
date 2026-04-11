"""Pydantic-схемы для модуля Счётного суда Риу-Гранди-ду-Сул (TCE-RS, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Municipio(BaseModel):
    """Муниципалитет Риу-Гранди-ду-Сул (legacy -- Brazil)."""

    codigo: int | None = None
    nome: str | None = None
    uf: str | None = None
    codigo_ibge: int | None = None


class IndiceEducacao(BaseModel):
    """Индекс расходов на образование муниципалитета RS (legacy -- Brazil)."""

    ano: int | None = None
    codigo_orgao: int | None = None
    nome_orgao: str | None = None
    valor_despesa: float | None = None
    valor_receita: float | None = None
    indice: float | None = None


class IndiceSaude(BaseModel):
    """Индекс расходов на здравоохранение муниципалитета RS (legacy -- Brazil)."""

    ano: int | None = None
    codigo_orgao: int | None = None
    nome_orgao: str | None = None
    valor_despesa: float | None = None
    valor_receita: float | None = None
    indice: float | None = None


class GestaoFiscal(BaseModel):
    """Данные финансового управления (LRF) муниципальной исполнительной власти RS (legacy -- Brazil)."""

    ano: int | None = None
    codigo_orgao: int | None = None
    nome_orgao: str | None = None
    receita_corrente_liquida: float | None = None
    despesa_pessoal: float | None = None
    divida_consolidada: float | None = None
    operacoes_credito: float | None = None
    receita_mde: float | None = None
    despesa_mde: float | None = None
    receita_asps: float | None = None
    despesa_asps: float | None = None


class Dataset(BaseModel):
    """Набор данных портала CKAN TCE-RS (legacy -- Brazil)."""

    nome: str | None = None
    titulo: str | None = None
    grupo: str | None = None
    notas: str | None = None
    url: str | None = None
    num_recursos: int | None = None
