"""Pydantic-схемы для модуля Счётного суда Рио-де-Жанейро (TCE-RJ, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Тендеры
# ---------------------------------------------------------------------------


class Licitacao(BaseModel):
    """Муниципальный тендер в Рио-де-Жанейро (legacy -- Brazil)."""

    ente: str | None = None
    unidade: str | None = None
    ano: int | None = None
    modalidade: str | None = None
    tipo: str | None = None
    processo_licitatorio: str | None = None
    numero_edital: str | None = None
    objeto: str | None = None
    valor_estimado: float | None = None
    data_publicacao_oficial: str | None = None
    data_homologacao: str | None = None


class LicitacaoResultado(BaseModel):
    """Страничный результат поиска тендеров (legacy -- Brazil)."""

    licitacoes: list[Licitacao] = []
    total: int = 0


# ---------------------------------------------------------------------------
# Муниципальные контракты
# ---------------------------------------------------------------------------


class ContratoMunicipio(BaseModel):
    """Муниципальный контракт в Рио-де-Жанейро (legacy -- Brazil)."""

    ente: str | None = None
    numero_contrato: str | None = None
    ano_contrato: int | None = None
    contratado: str | None = None
    cpf_cnpj_contratado: str | None = None
    objeto: str | None = None
    tipo_contrato: str | None = None
    valor_contrato: float | None = None
    data_assinatura_contrato: str | None = None
    data_vencimento_contrato: str | None = None


class ContratoMunicipioResultado(BaseModel):
    """Страничный результат поиска муниципальных контрактов (legacy -- Brazil)."""

    contratos: list[ContratoMunicipio] = []
    total: int = 0


# ---------------------------------------------------------------------------
# Прямые закупки
# ---------------------------------------------------------------------------


class CompraDireta(BaseModel):
    """Прямая закупка (отмена/необходимость) (legacy -- Brazil)."""

    processo: str | None = None
    ano_processo: str | None = None
    unidade: str | None = None
    objeto: str | None = None
    afastamento: str | None = None
    fornecedor_vencedor: str | None = None
    valor_processo: float | None = None
    data_aprovacao: str | None = None
    enquadramento_legal: str | None = None


# ---------------------------------------------------------------------------
# Приостановленные стройки
# ---------------------------------------------------------------------------


class ObraParalisada(BaseModel):
    """Приостановленное общественное строительство (legacy -- Brazil)."""

    ente: str | None = None
    tipo_ente: str | None = None
    nome: str | None = None
    funcao_governo: str | None = None
    numero_contrato: str | None = None
    nome_contratada: str | None = None
    cnpj_contratada: str | None = None
    valor_total_contrato: float | None = None
    valor_pago_obra: float | None = None
    tempo_paralisacao: str | None = None
    motivo_paralisacao: str | None = None
    data_paralisacao: str | None = None
    data_inicio_obra: str | None = None
    status_contrato: str | None = None
    classificacao_obra: str | None = None


# ---------------------------------------------------------------------------
# Штрафы
# ---------------------------------------------------------------------------


class Penalidade(BaseModel):
    """Штраф или возмещение, применённые TCE-RJ (legacy -- Brazil)."""

    processo: str | None = None
    ano_condenacao: int | None = None
    valor_penalidade: float | None = None
    condenacao: str | None = None
    ente: str | None = None
    nome_orgao: str | None = None
    tipo_ente: str | None = None
    grupo_natureza: str | None = None
    data_sessao: str | None = None


# ---------------------------------------------------------------------------
# Финансовая отчётность
# ---------------------------------------------------------------------------


class PrestacaoContas(BaseModel):
    """Муниципальная финансовая отчётность (legacy -- Brazil)."""

    municipio: str | None = None
    regiao: str | None = None
    ano: int | None = None
    indicador: str | None = None
    processo: str | None = None
    responsavel: str | None = None


# ---------------------------------------------------------------------------
# Публичные концессии
# ---------------------------------------------------------------------------


class Concessao(BaseModel):
    """Муниципальная публичная концессия (legacy -- Brazil)."""

    ente: str | None = None
    unidade: str | None = None
    numero: str | None = None
    objeto: str | None = None
    data_assinatura: str | None = None
    data_execucao_final: str | None = None
    situacao_concessao: str | None = None
    natureza: str | None = None
    segmento_servico: str | None = None
    nome_razao_social: str | None = None
    valor_total_outorga: float | None = None


class ConcessaoMunicipio(BaseModel):
    """Концессии, сгруппированные по муниципалитету (legacy -- Brazil)."""

    municipio: str
    concessoes: list[Concessao] = []
