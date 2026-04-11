"""Pydantic-схемы для модуля Счётного суда Санта-Катарины (TCE-SC, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Municipio(BaseModel):
    """Муниципалитет Санта-Катарины (legacy -- Brazil)."""

    codigo_municipio: int | None = None
    nome_municipio: str | None = None


class UnidadeGestora(BaseModel):
    """Управляющая единица под юрисдикцией TCE-SC (legacy -- Brazil)."""

    codigo_unidade: int | None = None
    nome_unidade: str | None = None
    sigla_unidade: str | None = None
    nome_municipio: str | None = None
