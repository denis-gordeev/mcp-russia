"""Pydantic-схемы для модуля здравоохранения (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Estabelecimento(BaseModel):
    """Медицинское учреждение CNES (legacy -- Brazil)."""

    codigo_cnes: str | None = None
    nome_fantasia: str | None = None
    nome_razao_social: str | None = None
    natureza_organizacao: str | None = None
    tipo_gestao: str | None = None
    codigo_tipo: str | None = None
    descricao_tipo: str | None = None
    codigo_municipio: str | None = None
    codigo_uf: str | None = None
    endereco: str | None = None


class Profissional(BaseModel):
    """Медицинский работник CNES (legacy -- Brazil)."""

    codigo_cnes: str | None = None
    nome: str | None = None
    cns: str | None = None
    cbo: str | None = None
    descricao_cbo: str | None = None


class TipoEstabelecimento(BaseModel):
    """Тип медицинского учреждения (legacy -- Brazil)."""

    codigo: str | None = None
    descricao: str | None = None


class Leito(BaseModel):
    """Больничная койка CNES (legacy -- Brazil)."""

    codigo_cnes: str | None = None
    tipo_leito: str | None = None
    especialidade: str | None = None
    existente: int | None = None
    sus: int | None = None
