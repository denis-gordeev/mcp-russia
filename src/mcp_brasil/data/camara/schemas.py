"""Pydantic-схемы для ответов API Палаты депутатов (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Deputado(BaseModel):
    """Федеральный депутат (legacy -- Brazil)."""

    id: int | None = None
    nome: str | None = None
    sigla_partido: str | None = None
    sigla_uf: str | None = None
    email: str | None = None
    foto: str | None = None
    legislatura: int | None = None


class Proposicao(BaseModel):
    """Законодательное предложение (PL, PEC, MPV и т.д.) (legacy -- Brazil)."""

    id: int | None = None
    sigla_tipo: str | None = None
    numero: int | None = None
    ano: int | None = None
    ementa: str | None = None
    data_apresentacao: str | None = None
    situacao: str | None = None
    orgao_situacao: str | None = None
    autor: str | None = None
    autor_partido: str | None = None
    autor_uf: str | None = None
    regime: str | None = None
    url_inteiro_teor: str | None = None
    uri: str | None = None


class Tramitacao(BaseModel):
    """Событие законодательного процесса (legacy -- Brazil)."""

    data: str | None = None
    descricao: str | None = None
    orgao: str | None = None
    situacao: str | None = None
    despacho: str | None = None


class Votacao(BaseModel):
    """Голосование в пленарном зале или комиссии (legacy -- Brazil)."""

    id: str | None = None
    data: str | None = None
    descricao: str | None = None
    aprovacao: bool | None = None
    proposicao_id: int | None = None
    proposicao_descricao: str | None = None


class VotoNominal(BaseModel):
    """Индивидуальный голос депутата по вопросу голосования (legacy -- Brazil)."""

    deputado_id: int | None = None
    deputado_nome: str | None = None
    partido: str | None = None
    uf: str | None = None
    voto: str | None = None


class DespesaDeputado(BaseModel):
    """Расходы депутатского парламентского фонда (CEAP) (legacy -- Brazil)."""

    deputado_id: int | None = None
    deputado_nome: str | None = None
    tipo_despesa: str | None = None
    fornecedor: str | None = None
    cnpj_cpf: str | None = None
    valor_documento: float | None = None
    valor_liquido: float | None = None
    data_documento: str | None = None
    mes: int | None = None
    ano: int | None = None


class Evento(BaseModel):
    """Законодательное событие (сессия, слушание, заседание) (legacy -- Brazil)."""

    id: int | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    local: str | None = None
    situacao: str | None = None
    orgaos: str | None = None


class Orgao(BaseModel):
    """Законодательный орган (комиссия, CPI и т.д.) (legacy -- Brazil)."""

    id: int | None = None
    sigla: str | None = None
    nome: str | None = None
    tipo: str | None = None
    situacao: str | None = None


class FrenteParlamentar(BaseModel):
    """Парламентская фракция (legacy -- Brazil)."""

    id: int | None = None
    titulo: str | None = None
    legislatura: int | None = None
    coordenador: str | None = None
    situacao: str | None = None
