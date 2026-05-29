"""Pydantic-схемы для модуля судебной практики (STF, STJ, TST, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Jurisprudencia(BaseModel):
    """Результат поиска судебной практики (решение коллегии) (legacy -- Brazil)."""

    tribunal: str | None = None
    ementa: str | None = None
    relator: str | None = None
    numero_processo: str | None = None
    classe: str | None = None
    data_julgamento: str | None = None
    data_publicacao: str | None = None
    orgao_julgador: str | None = None
    decisao: str | None = None
    url: str | None = None


class Sumula(BaseModel):
    """Сумма (сводная правовая позиция) высшего суда (legacy -- Brazil)."""

    tribunal: str | None = None
    numero: int | None = None
    enunciado: str | None = None
    referencia_legislativa: str | None = None
    situacao: str | None = None
    data_aprovacao: str | None = None
    vinculante: bool | None = None


class RepercussaoGeral(BaseModel):
    """Тема общей реперкуссии STF (legacy -- Brazil)."""

    numero_tema: int | None = None
    titulo: str | None = None
    descricao: str | None = None
    relator: str | None = None
    leading_case: str | None = None
    situacao: str | None = None
    data_reconhecimento: str | None = None
    tese: str | None = None
