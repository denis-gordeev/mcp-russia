"""Pydantic-схемы для данных Счётного суда Пиауи (TCE-PI, Brazil, legacy)."""

from pydantic import BaseModel


class Prefeitura(BaseModel):
    """Муниципалитет, зарегистрированный в TCE-PI (legacy -- Brazil)."""

    id: int
    nome: str
    codIBGE: str | None = None
    urlPrefeitura: str | None = None
    urlCamara: str | None = None


class Gestor(BaseModel):
    """Действующий мэр муниципалитета (legacy -- Brazil)."""

    nome: str
    inicio_gestao: str | None = None


class DespesaAnual(BaseModel):
    """Годовые итоги расходов муниципалитета или штата (legacy -- Brazil)."""

    exercicio: int
    empenhada: float = 0
    liquidada: float = 0
    paga: float = 0


class DespesaFuncao(BaseModel):
    """Разбивка расходов по государственным функциям (legacy -- Brazil)."""

    funcao: str
    paga: float = 0


class ReceitaAnual(BaseModel):
    """Годовые итоги доходов муниципалитета или штата (legacy -- Brazil)."""

    exercicio: int | None = None
    prevista: float = 0
    arrecadada: float = 0


class ReceitaDetalhe(BaseModel):
    """Детализация доходов за конкретный год (legacy -- Brazil)."""

    categoria: str | None = None
    origem: str | None = None
    receita: str | None = None
    detalhamento: str | None = None
    prevista: float = 0
    arrecadada: float = 0


class Orgao(BaseModel):
    """Государственный орган/учреждение, зарегистрированное в TCE-PI (legacy -- Brazil)."""

    id: str
    nome: str
    sigla: str | None = None


class Credor(BaseModel):
    """Крупнейший кредитор муниципалитета (legacy -- Brazil)."""

    nome: str
    pago: float = 0
