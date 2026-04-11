"""Pydantic-схемы для модуля официальных вестников (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class DiarioOficial(BaseModel):
    """Выпуск официального вестника, возвращаемый API (legacy -- Brazil)."""

    territory_id: str | None = None
    territory_name: str | None = None
    state_code: str | None = None
    date: str | None = None
    edition_number: str | None = None
    is_extra_edition: bool | None = None
    url: str | None = None
    txt_url: str | None = None
    excerpts: list[str] | None = None
    highlight_texts: list[str] | None = None


class DiarioResultado(BaseModel):
    """Страничный результат поиска вестников (legacy -- Brazil)."""

    total_gazettes: int = 0
    gazettes: list[DiarioOficial] = []


class Excerto(BaseModel):
    """Выдержка (фрагмент) из официального вестника (legacy -- Brazil)."""

    territory_id: str | None = None
    territory_name: str | None = None
    state_code: str | None = None
    date: str | None = None
    edition_number: str | None = None
    is_extra_edition: bool | None = None
    url: str | None = None
    txt_url: str | None = None
    excerpt: str | None = None
    subheadline: str | None = None


class ExcertoResultado(BaseModel):
    """Страничный результат поиска выдержек (legacy -- Brazil)."""

    total_excerpts: int = 0
    excerpts: list[Excerto] = []


class CidadeQueridoDiario(BaseModel):
    """Город, доступный в базе Querido Diario (legacy -- Brazil)."""

    territory_id: str
    territory_name: str
    state_code: str
    publication_urls: list[str] | None = None
    level: str | None = None
