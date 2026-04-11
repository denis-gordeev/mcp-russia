"""Pydantic-схемы для ответов API Портала прозрачности (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel


class ContratoFornecedor(BaseModel):
    """Федеральный контракт по CPF/CNPJ поставщика (legacy -- Brazil)."""

    id: int | None = None
    numero: str | None = None
    objeto: str | None = None
    valor_inicial: float | None = None
    valor_final: float | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    orgao: str | None = None
    fornecedor: str | None = None


class RecursoRecebido(BaseModel):
    """Полученные средства (расходы) по бенефициару (legacy -- Brazil)."""

    ano: int | None = None
    mes: int | None = None
    valor: float | None = None
    favorecido_nome: str | None = None
    orgao_nome: str | None = None
    uf: str | None = None


class Servidor(BaseModel):
    """Федеральный государственный служащий (legacy -- Brazil)."""

    id: int | None = None
    cpf: str | None = None
    nome: str | None = None
    tipo_servidor: str | None = None
    situacao: str | None = None
    orgao: str | None = None


class Licitacao(BaseModel):
    """Федеральный тендер (legacy -- Brazil)."""

    id: int | None = None
    numero: str | None = None
    objeto: str | None = None
    modalidade: str | None = None
    situacao: str | None = None
    valor_estimado: float | None = None
    data_abertura: str | None = None
    orgao: str | None = None


class BolsaFamiliaMunicipio(BaseModel):
    """Данные программы Novo Bolsa Familia по муниципалитету (legacy -- Brazil)."""

    municipio: str | None = None
    uf: str | None = None
    quantidade: int | None = None
    valor: float | None = None
    data_referencia: str | None = None


class BolsaFamiliaSacado(BaseModel):
    """Данные программы Novo Bolsa Familia по NIS получателя (legacy -- Brazil)."""

    nis: str | None = None
    nome: str | None = None
    municipio: str | None = None
    uf: str | None = None
    valor: float | None = None


class Sancao(BaseModel):
    """Санкция в отношении физического или юридического лица (legacy -- Brazil)."""

    fonte: str | None = None
    tipo: str | None = None
    nome: str | None = None
    cpf_cnpj: str | None = None
    orgao: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    fundamentacao: str | None = None


class Emenda(BaseModel):
    """Парламентская поправка (legacy -- Brazil)."""

    numero: str | None = None
    autor: str | None = None
    tipo: str | None = None
    localidade: str | None = None
    valor_empenhado: float | None = None
    valor_pago: float | None = None
    ano: int | None = None


class Viagem(BaseModel):
    """Служебная командировка федерального служащего (legacy -- Brazil)."""

    id: int | None = None
    cpf: str | None = None
    nome: str | None = None
    cargo: str | None = None
    orgao: str | None = None
    destino: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    valor_passagens: float | None = None
    valor_diarias: float | None = None


class Convenio(BaseModel):
    """Соглашение или добровольный трансфер (legacy -- Brazil)."""

    numero: str | None = None
    objeto: str | None = None
    situacao: str | None = None
    valor_convenio: float | None = None
    valor_liberado: float | None = None
    orgao: str | None = None
    convenente: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None


class CartaoPagamento(BaseModel):
    """Оплата корпоративной картой / авансовым фондом (legacy -- Brazil)."""

    portador: str | None = None
    cpf: str | None = None
    orgao: str | None = None
    valor: float | None = None
    data: str | None = None
    tipo: str | None = None
    estabelecimento: str | None = None


class PessoaExpostaPoliticamente(BaseModel):
    """Политически значимое лицо (PEP) (legacy -- Brazil)."""

    cpf: str | None = None
    nome: str | None = None
    orgao: str | None = None
    funcao: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None


class AcordoLeniencia(BaseModel):
    """Соглашение о смягчении (антикоррупция) (legacy -- Brazil)."""

    empresa: str | None = None
    cnpj: str | None = None
    orgao: str | None = None
    situacao: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    valor: float | None = None


class NotaFiscal(BaseModel):
    """Электронный фискальный счёт (legacy -- Brazil)."""

    numero: str | None = None
    serie: str | None = None
    emitente: str | None = None
    cnpj_emitente: str | None = None
    valor: float | None = None
    data_emissao: str | None = None


class BeneficioSocial(BaseModel):
    """Социальное пособие (BPC, пособие по безработице и т.д.) (legacy -- Brazil)."""

    tipo: str | None = None
    nome_beneficiario: str | None = None
    cpf: str | None = None
    nis: str | None = None
    valor: float | None = None
    mes_referencia: str | None = None
    municipio: str | None = None
    uf: str | None = None


class PessoaFisicaVinculos(BaseModel):
    """Связи и льготы физического лица по CPF (legacy -- Brazil)."""

    cpf: str | None = None
    nome: str | None = None
    tipo_vinculo: str | None = None
    orgao: str | None = None
    beneficios: str | None = None


class PessoaJuridicaVinculos(BaseModel):
    """Санкции и контракты юридического лица по CNPJ (legacy -- Brazil)."""

    cnpj: str | None = None
    razao_social: str | None = None
    sancoes: str | None = None
    contratos: str | None = None


class ContratoDetalhe(BaseModel):
    """Подробная информация о федеральном контракте (legacy -- Brazil)."""

    id: int | None = None
    numero: str | None = None
    objeto: str | None = None
    valor_inicial: float | None = None
    valor_final: float | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    orgao: str | None = None
    fornecedor: str | None = None
    modalidade: str | None = None
    situacao: str | None = None
    licitacao: str | None = None


class ServidorDetalhe(BaseModel):
    """Полная информация о служащем с указанием заработной платы (legacy -- Brazil)."""

    id: int | None = None
    cpf: str | None = None
    nome: str | None = None
    tipo_servidor: str | None = None
    situacao: str | None = None
    orgao: str | None = None
    cargo: str | None = None
    funcao: str | None = None
    remuneracao_basica: float | None = None
    remuneracao_apos_deducoes: float | None = None
    honorarios: float | None = None
    outras_remuneracoes: float | None = None
    jetons: float | None = None
