"""Pydantic-схемы для модуля Счётного суда (TCU, Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Решения коллегии (Acordaos)
# ---------------------------------------------------------------------------


class Acordao(BaseModel):
    """Решение коллегии (acordao) Счётного суда (legacy -- Brazil)."""

    key: str | None = None
    tipo: str | None = None
    ano_acordao: str | None = None
    titulo: str | None = None
    numero_acordao: str | None = None
    numero_ata: str | None = None
    colegiado: str | None = None
    data_sessao: str | None = None
    relator: str | None = None
    situacao: str | None = None
    sumario: str | None = None
    url_acordao: str | None = None


# ---------------------------------------------------------------------------
# Недопущенные лица
# ---------------------------------------------------------------------------


class Inabilitado(BaseModel):
    """Лицо, недопущенное к государственной должности по решению Счётного суда (legacy -- Brazil)."""

    nome: str | None = None
    cpf: str | None = None
    processo: str | None = None
    deliberacao: str | None = None
    data_transito_julgado: str | None = None
    data_final: str | None = None
    data_acordao: str | None = None
    uf: str | None = None
    municipio: str | None = None


class InabilitadoResultado(BaseModel):
    """Страничный результат поиска недопущенных лиц (ORDS) (legacy -- Brazil)."""

    items: list[Inabilitado] = []
    has_more: bool = False
    limit: int = 25
    offset: int = 0
    count: int = 0


# ---------------------------------------------------------------------------
# Недобросовестные участники
# ---------------------------------------------------------------------------


class Inidoneo(BaseModel):
    """Участник тендера, признанный недобросовестным Счётным судом (legacy -- Brazil)."""

    nome: str | None = None
    cpf_cnpj: str | None = None
    processo: str | None = None
    deliberacao: str | None = None
    data_transito_julgado: str | None = None
    data_final: str | None = None
    data_acordao: str | None = None
    uf: str | None = None
    municipio: str | None = None


class InidoneoResultado(BaseModel):
    """Страничный результат поиска недобросовестных участников (ORDS) (legacy -- Brazil)."""

    items: list[Inidoneo] = []
    has_more: bool = False
    limit: int = 25
    offset: int = 0
    count: int = 0


# ---------------------------------------------------------------------------
# Справки APF
# ---------------------------------------------------------------------------


class TipoCertidao(BaseModel):
    """Тип справки, доступной в системе APF (legacy -- Brazil)."""

    orgao_emissor: str
    sigla: str
    descricao: str


class CertidaoItem(BaseModel):
    """Индивидуальная справка в консолидированном результате (legacy -- Brazil)."""

    emissor: str | None = None
    tipo: str | None = None
    data_hora_emissao: str | None = None
    descricao: str | None = None
    situacao: str | None = None
    observacao: str | None = None
    link_consulta_manual: str | None = None


class CertidaoResultado(BaseModel):
    """Консолидированный результат справок для CNPJ (legacy -- Brazil)."""

    razao_social: str | None = None
    nome_fantasia: str | None = None
    cnpj: str | None = None
    uf: str | None = None
    certidoes: list[CertidaoItem] = []
    cnpj_encontrado_base_tcu: bool = False


# ---------------------------------------------------------------------------
# Расчёт задолженности
# ---------------------------------------------------------------------------


class ParcelaDebito(BaseModel):
    """Часть задолженности для расчёта (legacy -- Brazil)."""

    data_fato: str
    indicativo_debito_credito: str = "D"
    valor_original: float


class CalculoDebitoResultado(BaseModel):
    """Результат расчёта обновлённой задолженности (legacy -- Brazil)."""

    data: str | None = None
    saldo_debito: float = 0.0
    saldo_variacao_selic: float = 0.0
    saldo_juros: float = 0.0
    saldo_total: float = 0.0


# ---------------------------------------------------------------------------
# Запросы Конгресса
# ---------------------------------------------------------------------------


class PedidoCongresso(BaseModel):
    """Запрос Национального конгресса в Счётный суд (legacy -- Brazil)."""

    tipo: str | None = None
    numero: int | None = None
    data_aprovacao: str | None = None
    assunto: str | None = None
    autor: str | None = None
    processo_scn: str | None = None
    link_proposicao: str | None = None


class PedidoCongressoResultado(BaseModel):
    """Страничный результат поиска запросов Конгресса (legacy -- Brazil)."""

    items: list[PedidoCongresso] = []
    has_next: bool = False


# ---------------------------------------------------------------------------
# Договоры Счётного суда
# ---------------------------------------------------------------------------


class UnidadeFiscalizadora(BaseModel):
    """Контролирующая единица Счётного суда (legacy -- Brazil)."""

    codigo: int | None = None
    sigla: str | None = None
    nome: str | None = None


class TermoContratual(BaseModel):
    """Контракт, заключённый Счётным судом (legacy -- Brazil)."""

    tipo_contratacao: str | None = None
    numero: int | None = None
    ano: int | None = None
    unidade_gestora: str | None = None
    nome_fornecedor: str | None = None
    cnpj_fornecedor: str | None = None
    objeto: str | None = None
    valor_inicial: float | None = None
    valor_atualizado: float | None = None
    data_assinatura: str | None = None
    data_inicio_vigencia: str | None = None
    data_termino_vigencia: str | None = None
    modalidade_licitacao: str | None = None
    numero_processo: str | None = None
    numero_aditamentos: int | None = None
    unidades_fiscalizadoras: list[UnidadeFiscalizadora] = []


# ---------------------------------------------------------------------------
# CADIRREG
# ---------------------------------------------------------------------------


class PessoaCadirreg(BaseModel):
    """Лицо с нерегулярными счетами, признанными Счётным судом (legacy -- Brazil)."""

    nome_responsavel: str | None = None
    cpf: str | None = None
    num_processo: str | None = None
    ano_processo: str | None = None
    julgamento: str | None = None
    unidade_tecnica_processo: str | None = None
    se_detentor_cargo_funcao_publica: str | None = None
    se_falecido: str | None = None
