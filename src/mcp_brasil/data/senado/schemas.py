"""Pydantic-схемы для ответов API Федерального сената (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class SenadorResumo(BaseModel):
    """Сенатор в сокращённом списке (legacy -- Brazil)."""

    codigo: str | None = None
    nome: str | None = None
    nome_completo: str | None = None
    partido: str | None = None
    uf: str | None = None
    foto: str | None = None
    em_exercicio: bool | None = None


class SenadorDetalhe(BaseModel):
    """Подробная информация о сенаторе (legacy -- Brazil)."""

    codigo: str | None = None
    nome: str | None = None
    nome_completo: str | None = None
    partido: str | None = None
    uf: str | None = None
    email: str | None = None
    foto: str | None = None
    telefone: str | None = None
    mandato_inicio: str | None = None
    mandato_fim: str | None = None


class MateriaResumo(BaseModel):
    """Законодательный акт в сокращённом списке (legacy -- Brazil)."""

    codigo: str | None = None
    sigla_tipo: str | None = None
    numero: str | None = None
    ano: str | None = None
    ementa: str | None = None
    data_apresentacao: str | None = None
    autor: str | None = None
    situacao: str | None = None


class MateriaDetalhe(BaseModel):
    """Подробная информация о законодательном акте (legacy -- Brazil)."""

    codigo: str | None = None
    sigla_tipo: str | None = None
    numero: str | None = None
    ano: str | None = None
    ementa: str | None = None
    ementa_completa: str | None = None
    data_apresentacao: str | None = None
    autor: str | None = None
    situacao: str | None = None
    casa_origem: str | None = None


class Tramitacao(BaseModel):
    """Событие законодательного процесса (legacy -- Brazil)."""

    data: str | None = None
    descricao: str | None = None
    local: str | None = None
    situacao: str | None = None


class VotacaoResumo(BaseModel):
    """Сокращённая информация о голосовании (legacy -- Brazil)."""

    codigo: str | None = None
    data: str | None = None
    descricao: str | None = None
    resultado: str | None = None


class VotacaoDetalhe(BaseModel):
    """Подробная информация о голосовании (legacy -- Brazil)."""

    codigo: str | None = None
    data: str | None = None
    descricao: str | None = None
    resultado: str | None = None
    materia_codigo: str | None = None
    materia_descricao: str | None = None
    sim: int | None = None
    nao: int | None = None
    abstencao: int | None = None


class VotoNominal(BaseModel):
    """Индивидуальный голос сенатора (legacy -- Brazil)."""

    senador_codigo: str | None = None
    senador_nome: str | None = None
    partido: str | None = None
    uf: str | None = None
    voto: str | None = None


class ComissaoResumo(BaseModel):
    """Комиссия в сокращённом списке (legacy -- Brazil)."""

    codigo: str | None = None
    sigla: str | None = None
    nome: str | None = None
    tipo: str | None = None


class ComissaoDetalhe(BaseModel):
    """Подробная информация о комиссии (legacy -- Brazil)."""

    codigo: str | None = None
    sigla: str | None = None
    nome: str | None = None
    tipo: str | None = None
    finalidade: str | None = None
    data_criacao: str | None = None
    data_extincao: str | None = None


class MembroComissao(BaseModel):
    """Член комиссии (legacy -- Brazil)."""

    codigo_senador: str | None = None
    nome: str | None = None
    partido: str | None = None
    uf: str | None = None
    cargo: str | None = None


class ReuniaoComissao(BaseModel):
    """Заседание комиссии (legacy -- Brazil)."""

    data: str | None = None
    tipo: str | None = None
    comissao: str | None = None
    pauta: str | None = None
    local: str | None = None


class SessaoPlenario(BaseModel):
    """Пленарное заседание (legacy -- Brazil)."""

    data: str | None = None
    tipo: str | None = None
    numero: str | None = None
    situacao: str | None = None


class LegislaturaInfo(BaseModel):
    """Информация о созыве (legacy -- Brazil)."""

    numero: int | None = None
    data_inicio: str | None = None
    data_fim: str | None = None


class Emenda(BaseModel):
    """Поправка к законодательному акту (legacy -- Brazil)."""

    codigo: str | None = None
    numero: str | None = None
    identificacao: str | None = None
    tipo: str | None = None
    data_apresentacao: str | None = None
    autor: str | None = None
    colegiado: str | None = None
    decisao: str | None = None
    data_decisao: str | None = None
    url_documento: str | None = None


class BlocoParlamentar(BaseModel):
    """Парламентский блок (коалиция) (legacy -- Brazil)."""

    codigo: str | None = None
    nome: str | None = None
    apelido: str | None = None
    data_criacao: str | None = None
    partidos: list[str] | None = None


class Lideranca(BaseModel):
    """Руководство в Сенате (legacy -- Brazil)."""

    codigo_parlamentar: str | None = None
    nome_parlamentar: str | None = None
    partido: str | None = None
    tipo_lideranca: str | None = None
    unidade_lideranca: str | None = None
    data_designacao: str | None = None


class Relatoria(BaseModel):
    """Докладчик по законодательному акту (legacy -- Brazil)."""

    codigo_materia: str | None = None
    identificacao: str | None = None
    ementa: str | None = None
    autor: str | None = None
    tipo_relator: str | None = None
    data_designacao: str | None = None
    colegiado: str | None = None
    tramitando: bool | None = None
