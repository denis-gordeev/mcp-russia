"""Pydantic-схемы для API открытых данных Compras.gov.br (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class Licitacao(BaseModel):
    """Тендер унаследованной системы SIASG/ComprasNet (legacy -- Brazil)."""

    id_compra: str | None = None
    identificador: str | None = None
    numero_processo: str | None = None
    uasg: int | None = None
    modalidade: int | None = None
    nome_modalidade: str | None = None
    numero_aviso: int | None = None
    situacao_aviso: str | None = None
    tipo_pregao: str | None = None
    objeto: str | None = None
    valor_estimado_total: float | None = None
    valor_homologado_total: float | None = None
    numero_itens: int | None = None
    data_publicacao: str | None = None
    data_abertura_proposta: str | None = None
    nome_responsavel: str | None = None
    funcao_responsavel: str | None = None
    endereco_entrega_edital: str | None = None


class LicitacaoResultado(BaseModel):
    """Страничный результат поиска тендеров (legacy -- Brazil)."""

    total: int = 0
    licitacoes: list[Licitacao] = []


class ContratoDA(BaseModel):
    """Контракт Compras.gov.br (Открытые данные) (legacy -- Brazil)."""

    codigo_orgao: str | None = None
    nome_orgao: str | None = None
    codigo_unidade_gestora: str | None = None
    nome_unidade_gestora: str | None = None
    numero_contrato: str | None = None
    nome_modalidade_compra: str | None = None
    nome_tipo: str | None = None
    nome_categoria: str | None = None
    ni_fornecedor: str | None = None
    nome_fornecedor: str | None = None
    processo: str | None = None
    objeto: str | None = None
    data_vigencia_inicial: str | None = None
    data_vigencia_final: str | None = None
    valor_global: float | None = None
    valor_parcela: float | None = None
    valor_acumulado: float | None = None


class ContratoDAResultado(BaseModel):
    """Страничный результат поиска контрактов (legacy -- Brazil)."""

    total: int = 0
    contratos: list[ContratoDA] = []


class FornecedorDA(BaseModel):
    """Поставщик, зарегистрированный в Compras.gov.br (legacy -- Brazil)."""

    cnpj: str | None = None
    cpf: str | None = None
    nome_razao_social: str | None = None
    uf_sigla: str | None = None
    nome_municipio: str | None = None
    porte_empresa_nome: str | None = None
    natureza_juridica_nome: str | None = None
    nome_cnae: str | None = None
    ativo: bool | None = None
    habilitado_licitar: bool | None = None


class FornecedorDAResultado(BaseModel):
    """Страничный результат поиска поставщиков (legacy -- Brazil)."""

    total: int = 0
    fornecedores: list[FornecedorDA] = []


class GrupoMaterial(BaseModel):
    """Группа материалов CATMAT (legacy -- Brazil)."""

    codigo_grupo: int | None = None
    nome_grupo: str | None = None
    status_grupo: bool | None = None


class GrupoMaterialResultado(BaseModel):
    """Результат поиска групп материалов (legacy -- Brazil)."""

    total: int = 0
    grupos: list[GrupoMaterial] = []


class ItemMaterial(BaseModel):
    """Единица материала CATMAT (legacy -- Brazil)."""

    codigo_item: int | None = None
    descricao_item: str | None = None
    codigo_grupo: int | None = None
    codigo_classe: int | None = None
    codigo_pdm: int | None = None
    status_item: bool | None = None


class ItemMaterialResultado(BaseModel):
    """Страничный результат поиска единиц материалов (legacy -- Brazil)."""

    total: int = 0
    itens: list[ItemMaterial] = []


class ItemServico(BaseModel):
    """Единица услуги CATSER (legacy -- Brazil)."""

    codigo_servico: int | None = None
    nome_servico: str | None = None
    codigo_secao: int | None = None
    codigo_divisao: int | None = None
    codigo_grupo: int | None = None
    codigo_classe: int | None = None
    status_servico: bool | None = None


class ItemServicoResultado(BaseModel):
    """Страничный результат поиска единиц услуг (legacy -- Brazil)."""

    total: int = 0
    itens: list[ItemServico] = []


class Uasg(BaseModel):
    """Административная единица обслуживания общего назначения (legacy -- Brazil)."""

    codigo_uasg: str | None = None
    nome_uasg: str | None = None
    cnpj_cpf_orgao: str | None = None
    sigla_uf: str | None = None
    nome_municipio: str | None = None
    uso_sisg: bool | None = None
    status_uasg: bool | None = None


class UasgResultado(BaseModel):
    """Страничный результат поиска UASG (legacy -- Brazil)."""

    total: int = 0
    uasgs: list[Uasg] = []
