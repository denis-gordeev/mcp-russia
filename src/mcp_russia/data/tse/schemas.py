"""Pydantic-схемы для ответов API ВСТ (Tribunal Superior Eleitoral, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Eleicao(BaseModel):
    """Выборы (очередные или дополнительные) (legacy -- Brazil)."""

    id: int | None = None
    sigla_uf: str | None = None
    ano: int | None = None
    codigo: str | None = None
    nome: str | None = None
    tipo: str | None = None
    turno: str | None = None
    tipo_abrangencia: str | None = None
    data_eleicao: str | None = None
    descricao: str | None = None


class Cargo(BaseModel):
    """Выборная должность (legacy -- Brazil)."""

    codigo: int | None = None
    sigla: str | None = None
    nome: str | None = None
    titular: bool | None = None
    contagem: int | None = None


class CandidatoResumo(BaseModel):
    """Кандидат (сокращённый список) (legacy -- Brazil)."""

    id: int | None = None
    nome_urna: str | None = None
    numero: int | None = None
    partido: str | None = None
    situacao: str | None = None
    foto_url: str | None = None


class Candidato(BaseModel):
    """Кандидат с полной информацией (legacy -- Brazil)."""

    id: int | None = None
    nome_urna: str | None = None
    nome_completo: str | None = None
    numero: int | None = None
    cpf: str | None = None
    data_nascimento: str | None = None
    sexo: str | None = None
    estado_civil: str | None = None
    cor_raca: str | None = None
    nacionalidade: str | None = None
    grau_instrucao: str | None = None
    ocupacao: str | None = None
    uf_nascimento: str | None = None
    municipio_nascimento: str | None = None
    partido: str | None = None
    situacao: str | None = None
    situacao_candidato: str | None = None
    coligacao: str | None = None
    composicao_coligacao: str | None = None
    descricao_totalizacao: str | None = None
    total_votos: int | None = None
    gasto_campanha: float | None = None
    total_bens: float | None = None
    emails: list[str] | None = None
    sites: list[str] | None = None
    foto_url: str | None = None
    candidato_inapto: bool | None = None
    motivo_ficha_limpa: bool | None = None


class ResultadoCandidato(BaseModel):
    """Кандидат с результатами выборов (подсчёт голосов) (legacy -- Brazil)."""

    nome_urna: str | None = None
    numero: int | None = None
    partido: str | None = None
    total_votos: int | None = None
    percentual: str | None = None
    descricao_totalizacao: str | None = None


class BemCandidato(BaseModel):
    """Имущество, декларированное кандидатом (legacy -- Brazil)."""

    ordem: int | None = None
    descricao: str | None = None
    tipo: str | None = None
    valor: float | None = None


class ResultadoCDN(BaseModel):
    """Кандидат с результатами CDN ВСТ (legacy -- Brazil)."""

    sequencia: str | None = None
    nome: str | None = None
    numero: str | None = None
    nome_vice: str | None = None
    coligacao: str | None = None
    votos: int | None = None
    percentual: str | None = None
    eleito: bool = False
    situacao: str | None = None
    validade_voto: str | None = None


class ResultadoRegiao(BaseModel):
    """Результаты выборов в регионе (страна, штат или муниципалитет) (legacy -- Brazil)."""

    codigo: str | None = None
    tipo: str | None = None  # "br", "uf", "mu"
    uf: str | None = None
    data_eleicao: str | None = None
    total_secoes: int | None = None
    pct_apurado: str | None = None
    total_eleitores: int | None = None
    total_comparecimento: int | None = None
    total_abstencoes: int | None = None
    candidatos: list[ResultadoCDN] = []


class MunicipioEleitoral(BaseModel):
    """Муниципалитет с избирательными кодами ВСТ и IBGE (legacy -- Brazil)."""

    codigo_tse: str | None = None
    codigo_ibge: str | None = None
    nome: str | None = None
    capital: bool = False
    uf: str | None = None


class PrestaContas(BaseModel):
    """Сводка финансовой отчётности кампании (legacy -- Brazil)."""

    candidato_id: str | None = None
    nome: str | None = None
    partido: str | None = None
    cnpj: str | None = None
    total_recebido: float | None = None
    total_despesas: float | None = None
    total_bens: float | None = None
    limite_gastos: float | None = None
    divida_campanha: str | None = None
    sobra_financeira: str | None = None
    total_receita_pf: float | None = None
    total_receita_pj: float | None = None
    total_fundo_partidario: float | None = None
    total_fundo_especial: float | None = None
