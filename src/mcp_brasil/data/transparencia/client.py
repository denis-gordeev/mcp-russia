"""HTTP client for the Portal da Transparência API.

Ported and expanded from mcp-dadosbr/lib/tools/government.ts
(executeTransparencia + executeCeisCnep).

All functions return typed Pydantic models. No LLM formatting here (ADR-001).
Auth is injected via the ``chave-api-dados`` header using ``http_get()``.

Endpoints:
    - /contratos/cpf-cnpj             → buscar_contratos
    - /despesas/recursos-recebidos     → consultar_despesas
    - /servidores                      → buscar_servidores
    - /licitacoes                      → buscar_licitacoes
    - /novo-bolsa-familia-por-municipio → consultar_bolsa_familia_municipio
    - /novo-bolsa-familia-sacado-por-nis → consultar_bolsa_familia_nis
    - /ceis, /cnep, /cepim, /ceaf      → buscar_sancoes
    - /emendas                         → buscar_emendas
    - /viagens-por-cpf                 → consultar_viagens
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Any

from mcp_brasil._shared.formatting import parse_rub_number
from mcp_brasil._shared.http_client import http_get
from mcp_brasil._shared.rate_limiter import RateLimiter
from mcp_brasil.exceptions import AuthError

from .constants import (
    ACORDOS_LENIENCIA_URL,
    AUTH_ENV_VAR,
    AUTH_HEADER_NAME,
    BENEFICIOS_CIDADAO_URL,
    BOLSA_FAMILIA_MUNICIPIO_URL,
    BOLSA_FAMILIA_NIS_URL,
    CARTOES_URL,
    CONTRATO_DETALHE_URL,
    CONTRATOS_URL,
    CONVENIOS_URL,
    DESPESAS_URL,
    EMENDAS_URL,
    LICITACOES_URL,
    NOTAS_FISCAIS_URL,
    PEP_URL,
    PESSOAS_FISICAS_URL,
    PESSOAS_JURIDICAS_URL,
    SANCOES_DATABASES,
    SERVIDOR_DETALHE_URL,
    SERVIDORES_URL,
    VIAGENS_URL,
)
from .schemas import (
    AcordoLeniencia,
    BeneficioSocial,
    BolsaFamiliaMunicipio,
    BolsaFamiliaSacado,
    CartaoPagamento,
    ContratoDetalhe,
    ContratoFornecedor,
    Convenio,
    Emenda,
    Licitacao,
    NotaFiscal,
    PessoaExpostaPoliticamente,
    PessoaFisicaVinculos,
    PessoaJuridicaVinculos,
    RecursoRecebido,
    Sancao,
    Servidor,
    ServidorDetalhe,
    Viagem,
)

logger = logging.getLogger(__name__)

# 80 req/min — conservative margin below the 90 req/min daytime limit
_rate_limiter = RateLimiter(max_requests=80, period=60.0)


def _get_api_key() -> str:
    """Return the API key or raise AuthError."""
    key = os.environ.get(AUTH_ENV_VAR, "")
    if not key:
        raise AuthError(
            f"Variável de ambiente {AUTH_ENV_VAR} não configurada. "
            "Cadastre-se em portaldatransparencia.gov.br/api-de-dados/cadastrar-email"
        )
    return key


def _auth_headers() -> dict[str, str]:
    """Build auth headers for the API."""
    return {AUTH_HEADER_NAME: _get_api_key()}


def _clean_cpf_cnpj(valor: str) -> str:
    """Remove non-digit characters from CPF/CNPJ."""
    return re.sub(r"\D", "", valor)


async def _get(url: str, params: dict[str, Any] | None = None) -> Any:
    """Make an authenticated GET request to the Portal da Transparência API."""
    from mcp_brasil.exceptions import HttpClientError

    async with _rate_limiter:
        try:
            return await http_get(url, params=params, headers=_auth_headers())
        except HttpClientError as exc:
            msg = str(exc)
            if "403" in msg:
                logger.warning(
                    "Acesso negado (HTTP 403) para %s — verifique permissões da "
                    "chave API (TRANSPARENCIA_API_KEY). Alguns endpoints exigem "
                    "permissões adicionais.",
                    url,
                )
            raise


def _safe_parse_list(
    data: Any,
    parser: Any,
    endpoint: str,
    **parser_kwargs: Any,
) -> list[Any]:
    """Parse a list response, logging a warning if the shape is unexpected."""
    if isinstance(data, list):
        return [parser(item, **parser_kwargs) for item in data]
    logger.warning(
        "Resposta inesperada (esperava list) do endpoint %s: %s",
        endpoint,
        type(data).__name__,
    )
    return []


# --- Parsing helpers --------------------------------------------------------


def _parse_contrato(raw: dict[str, Any]) -> ContratoFornecedor:
    """Parse a raw contract JSON into a ContratoFornecedor model."""
    fornecedor = raw.get("fornecedor") or {}
    orgao = raw.get("unidadeGestora") or raw.get("orgaoVinculado") or {}
    return ContratoFornecedor(
        id=raw.get("id"),
        numero=raw.get("numero"),
        objeto=raw.get("objeto"),
        valor_inicial=raw.get("valorInicial"),
        valor_final=raw.get("valorFinal"),
        data_inicio=raw.get("dataInicioVigencia"),
        data_fim=raw.get("dataFimVigencia"),
        orgao=orgao.get("nome") or orgao.get("descricao"),
        fornecedor=fornecedor.get("nome") or fornecedor.get("razaoSocialReceita"),
    )


def _parse_recurso(raw: dict[str, Any]) -> RecursoRecebido:
    """Parse a raw expense/resource JSON."""
    return RecursoRecebido(
        ano=raw.get("ano"),
        mes=raw.get("mes"),
        valor=raw.get("valor"),
        favorecido_nome=raw.get("nomeFavorecido"),
        orgao_nome=raw.get("nomeOrgao"),
        uf=raw.get("uf"),
    )


def _parse_servidor(raw: dict[str, Any]) -> Servidor:
    """Parse a raw server/public servant JSON."""
    orgao = raw.get("orgaoServidorExercicio") or raw.get("orgaoServidorLotacao") or {}
    return Servidor(
        id=raw.get("id"),
        cpf=raw.get("cpf"),
        nome=raw.get("nome"),
        tipo_servidor=raw.get("tipoServidor"),
        situacao=raw.get("situacao"),
        orgao=orgao.get("nome") or orgao.get("descricao"),
    )


def _parse_licitacao(raw: dict[str, Any]) -> Licitacao:
    """Parse a raw procurement/bid JSON."""
    orgao = raw.get("unidadeGestora") or raw.get("orgao") or {}
    return Licitacao(
        id=raw.get("id"),
        numero=raw.get("numero"),
        objeto=raw.get("objeto"),
        modalidade=raw.get("modalidadeLicitacao") or raw.get("modalidade"),
        situacao=raw.get("situacao"),
        valor_estimado=raw.get("valorEstimado"),
        data_abertura=raw.get("dataAbertura") or raw.get("dataResultadoCompra"),
        orgao=orgao.get("nome") or orgao.get("descricao"),
    )


def _parse_bolsa_municipio(raw: dict[str, Any]) -> BolsaFamiliaMunicipio:
    """Parse Bolsa Família municipality data."""
    raw_mun = raw.get("municipio")
    municipio = raw_mun if isinstance(raw_mun, dict) else {}
    return BolsaFamiliaMunicipio(
        municipio=municipio.get("nomeIBGE") or (raw_mun if isinstance(raw_mun, str) else None),
        uf=municipio.get("uf", {}).get("sigla") if isinstance(municipio.get("uf"), dict) else None,
        quantidade=raw.get("quantidadeBeneficiados"),
        valor=raw.get("valor"),
        data_referencia=raw.get("dataReferencia"),
    )


def _parse_bolsa_sacado(raw: dict[str, Any]) -> BolsaFamiliaSacado:
    """Parse Bolsa Família NIS beneficiary data."""
    raw_mun = raw.get("municipio")
    municipio = raw_mun if isinstance(raw_mun, dict) else {}
    return BolsaFamiliaSacado(
        nis=raw.get("nis"),
        nome=raw.get("nome"),
        municipio=municipio.get("nomeIBGE") if isinstance(municipio, dict) else None,
        uf=municipio.get("uf", {}).get("sigla")
        if isinstance(municipio, dict) and isinstance(municipio.get("uf"), dict)
        else None,
        valor=raw.get("valor"),
    )


def _parse_sancao(raw: dict[str, Any], fonte: str) -> Sancao:
    """Parse a sanction record from any of the 4 databases."""
    sancionado = raw.get("sancionado") or raw.get("pessoaSancionada") or {}
    orgao = raw.get("orgaoSancionador") or {}
    return Sancao(
        fonte=fonte,
        tipo=raw.get("tipoSancao") or raw.get("tipoPenalidade"),
        nome=sancionado.get("nome") or sancionado.get("razaoSocialReceita"),
        cpf_cnpj=sancionado.get("codigoFormatado") or sancionado.get("cnpjFormatado"),
        orgao=orgao.get("nome"),
        data_inicio=raw.get("dataInicioSancao") or raw.get("dataPublicacao"),
        data_fim=raw.get("dataFimSancao") or raw.get("dataFinalSancao"),
        fundamentacao=raw.get("fundamentacaoLegal") or raw.get("fundamentacao"),
    )


def _parse_emenda(raw: dict[str, Any]) -> Emenda:
    """Parse a parliamentary amendment record."""
    autor = raw.get("autor") or {}
    localidade = raw.get("localidadeDoGasto") or {}
    return Emenda(
        numero=raw.get("numero") or raw.get("codigoEmenda"),
        autor=autor.get("nome") if isinstance(autor, dict) else str(autor) if autor else None,
        tipo=raw.get("tipoEmenda"),
        localidade=localidade.get("nome")
        if isinstance(localidade, dict)
        else str(localidade)
        if localidade
        else None,
        valor_empenhado=parse_rub_number(raw.get("valorEmpenhado")),
        valor_pago=parse_rub_number(raw.get("valorPago")),
        ano=raw.get("ano"),
    )


def _parse_viagem(raw: dict[str, Any]) -> Viagem:
    """Parse a federal travel record."""
    return Viagem(
        id=raw.get("id"),
        cpf=raw.get("cpf"),
        nome=raw.get("nome") or raw.get("nomeProposto"),
        cargo=raw.get("cargo") or raw.get("funcao"),
        orgao=raw.get("nomeOrgao"),
        destino=raw.get("destinos") or raw.get("destino"),
        data_inicio=raw.get("dataInicio") or raw.get("dataInicioAfastamento"),
        data_fim=raw.get("dataFim") or raw.get("dataFimAfastamento"),
        valor_passagens=raw.get("valorPassagens"),
        valor_diarias=raw.get("valorDiarias"),
    )


# --- Public API functions ---------------------------------------------------


async def buscar_contratos(cpf_cnpj: str, pagina: int = 1) -> list[ContratoFornecedor]:
    """Busca contratos federais por CPF/CNPJ do fornecedor.

    Args:
        cpf_cnpj: CPF ou CNPJ do fornecedor (aceita formatado ou só dígitos).
        pagina: Número da página de resultados.
    """
    params = {"cpfCnpj": _clean_cpf_cnpj(cpf_cnpj), "pagina": pagina}
    data = await _get(CONTRATOS_URL, params)
    return _safe_parse_list(data, _parse_contrato, "contratos")


async def consultar_despesas(
    mes_ano_inicio: str,
    mes_ano_fim: str,
    codigo_favorecido: str | None = None,
    pagina: int = 1,
) -> list[RecursoRecebido]:
    """Consulta despesas/recursos recebidos por favorecido.

    Args:
        mes_ano_inicio: Mês/ano início no formato MM/AAAA.
        mes_ano_fim: Mês/ano fim no formato MM/AAAA.
        codigo_favorecido: CPF ou CNPJ do favorecido.
        pagina: Número da página.
    """
    params: dict[str, Any] = {
        "mesAnoInicio": mes_ano_inicio,
        "mesAnoFim": mes_ano_fim,
        "pagina": pagina,
    }
    if codigo_favorecido:
        params["codigoFavorecido"] = _clean_cpf_cnpj(codigo_favorecido)
    data = await _get(DESPESAS_URL, params)
    return _safe_parse_list(data, _parse_recurso, "despesas")


async def buscar_servidores(
    cpf: str | None = None,
    nome: str | None = None,
    codigo_orgao_lotacao: str | None = None,
    codigo_orgao_exercicio: str | None = None,
    pagina: int = 1,
) -> list[Servidor]:
    """Busca servidores públicos federais.

    A API exige pelo menos um filtro obrigatório: CPF, código de órgão de
    lotação ou código de órgão de exercício.

    Args:
        cpf: CPF do servidor.
        nome: Nome do servidor (usado como filtro adicional).
        codigo_orgao_lotacao: Código SIAPE do órgão de lotação.
        codigo_orgao_exercicio: Código SIAPE do órgão de exercício.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if cpf:
        params["cpf"] = _clean_cpf_cnpj(cpf)
    if codigo_orgao_lotacao:
        params["orgaoServidorLotacao"] = codigo_orgao_lotacao
    if codigo_orgao_exercicio:
        params["orgaoServidorExercicio"] = codigo_orgao_exercicio
    if nome:
        params["nome"] = nome
    data = await _get(SERVIDORES_URL, params)
    return _safe_parse_list(data, _parse_servidor, "servidores")


async def buscar_licitacoes(
    codigo_orgao: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    pagina: int = 1,
) -> list[Licitacao]:
    """Busca licitações federais.

    Args:
        codigo_orgao: Código do órgão (SIAFI).
        data_inicial: Data inicial no formato DD/MM/AAAA.
        data_final: Data final no formato DD/MM/AAAA.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if codigo_orgao:
        params["codigoOrgao"] = codigo_orgao
    if data_inicial:
        params["dataInicial"] = data_inicial
    if data_final:
        params["dataFinal"] = data_final
    data = await _get(LICITACOES_URL, params)
    return _safe_parse_list(data, _parse_licitacao, "licitacoes")


async def consultar_bolsa_familia_municipio(
    mes_ano: str,
    codigo_ibge: str,
    pagina: int = 1,
) -> list[BolsaFamiliaMunicipio]:
    """Consulta dados do Novo Bolsa Família por município.

    Args:
        mes_ano: Mês/ano de referência no formato AAAAMM.
        codigo_ibge: Código IBGE do município.
        pagina: Número da página.
    """
    params: dict[str, Any] = {
        "mesAno": mes_ano,
        "codigoIbge": codigo_ibge,
        "pagina": pagina,
    }
    data = await _get(BOLSA_FAMILIA_MUNICIPIO_URL, params)
    return _safe_parse_list(data, _parse_bolsa_municipio, "bolsa-familia-municipio")


async def consultar_bolsa_familia_nis(
    mes_ano: str,
    nis: str,
    pagina: int = 1,
) -> list[BolsaFamiliaSacado]:
    """Consulta dados do Novo Bolsa Família por NIS do sacado.

    Args:
        mes_ano: Mês/ano de referência no formato AAAAMM.
        nis: Número de Identificação Social do beneficiário.
        pagina: Número da página.
    """
    params: dict[str, Any] = {
        "mesAno": mes_ano,
        "nis": nis,
        "pagina": pagina,
    }
    data = await _get(BOLSA_FAMILIA_NIS_URL, params)
    return _safe_parse_list(data, _parse_bolsa_sacado, "bolsa-familia-nis")


async def buscar_sancoes(
    consulta: str,
    bases: list[str] | None = None,
    pagina: int = 1,
) -> list[Sancao]:
    """Busca sanções em paralelo nas bases CEIS, CNEP, CEPIM e CEAF.

    Tenta primeiro por CPF/CNPJ; se falhar, tenta por nome.

    Args:
        consulta: CPF, CNPJ ou nome da pessoa/empresa.
        bases: Lista de bases a consultar (default: todas).
        pagina: Número da página.
    """
    bases_alvo = bases or list(SANCOES_DATABASES.keys())

    async def _consultar_base(base_key: str) -> list[Sancao]:
        db = SANCOES_DATABASES.get(base_key)
        if not db:
            return []

        url = db["url"]
        is_digits = consulta.strip().replace(".", "").replace("-", "").replace("/", "").isdigit()

        if is_digits:
            param_key = db["param_cpf_cnpj"]
            params: dict[str, Any] = {param_key: _clean_cpf_cnpj(consulta), "pagina": pagina}
        else:
            param_key = db["param_nome"]
            params = {param_key: consulta, "pagina": pagina}

        try:
            data = await _get(url, params=params)
            return _safe_parse_list(data, _parse_sancao, f"sancoes/{base_key}", fonte=db["nome"])
        except Exception:
            logger.warning("Falha ao consultar base %s para '%s'", base_key, consulta)
        return []

    results = await asyncio.gather(*[_consultar_base(b) for b in bases_alvo])
    return [sancao for sublist in results for sancao in sublist]


async def buscar_emendas(
    ano: int | None = None,
    nome_autor: str | None = None,
    pagina: int = 1,
) -> list[Emenda]:
    """Busca emendas parlamentares.

    Args:
        ano: Ano da emenda.
        nome_autor: Nome do autor da emenda.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if ano:
        params["ano"] = ano
    if nome_autor:
        params["nomeAutor"] = nome_autor
    data = await _get(EMENDAS_URL, params)
    return _safe_parse_list(data, _parse_emenda, "emendas")


async def consultar_viagens(cpf: str, pagina: int = 1) -> list[Viagem]:
    """Consulta viagens a serviço por CPF do servidor.

    Args:
        cpf: CPF do servidor.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"cpf": _clean_cpf_cnpj(cpf), "pagina": pagina}
    data = await _get(VIAGENS_URL, params)
    return _safe_parse_list(data, _parse_viagem, "viagens")


# --- Parsing helpers (new endpoints) ----------------------------------------


def _parse_convenio(raw: dict[str, Any]) -> Convenio:
    """Parse a raw agreement/covenant JSON."""
    orgao = raw.get("orgaoConcedente") or raw.get("orgao") or {}
    convenente = raw.get("convenente") or {}
    return Convenio(
        numero=raw.get("numero"),
        objeto=raw.get("objeto"),
        situacao=raw.get("situacao"),
        valor_convenio=raw.get("valorConvenio") or raw.get("valor"),
        valor_liberado=raw.get("valorLiberado"),
        orgao=orgao.get("nome") if isinstance(orgao, dict) else str(orgao) if orgao else None,
        convenente=convenente.get("nome")
        if isinstance(convenente, dict)
        else str(convenente)
        if convenente
        else None,
        data_inicio=raw.get("dataInicioVigencia"),
        data_fim=raw.get("dataFimVigencia"),
    )


def _parse_cartao(raw: dict[str, Any]) -> CartaoPagamento:
    """Parse a raw government credit card payment JSON."""
    return CartaoPagamento(
        portador=raw.get("portador") or raw.get("nomePortador"),
        cpf=raw.get("cpfPortador") or raw.get("cpf"),
        orgao=raw.get("nomeOrgao") or raw.get("orgao"),
        valor=raw.get("valorTransacao") or raw.get("valor"),
        data=raw.get("dataTransacao") or raw.get("data"),
        tipo=raw.get("tipoCartao") or raw.get("tipo"),
        estabelecimento=raw.get("nomeEstabelecimento") or raw.get("estabelecimento"),
    )


def _parse_pep(raw: dict[str, Any]) -> PessoaExpostaPoliticamente:
    """Parse a Politically Exposed Person record."""
    orgao = raw.get("orgao") or {}
    return PessoaExpostaPoliticamente(
        cpf=raw.get("cpf"),
        nome=raw.get("nome"),
        orgao=orgao.get("nome") if isinstance(orgao, dict) else str(orgao) if orgao else None,
        funcao=raw.get("funcao") or raw.get("descricaoFuncao"),
        data_inicio=raw.get("dataInicioExercicio") or raw.get("dataInicio"),
        data_fim=raw.get("dataFimExercicio") or raw.get("dataFim"),
    )


def _parse_acordo_leniencia(raw: dict[str, Any]) -> AcordoLeniencia:
    """Parse a leniency agreement record."""
    empresa = raw.get("pessoa") or raw.get("empresa") or {}
    orgao = raw.get("orgaoResponsavel") or raw.get("orgao") or {}
    return AcordoLeniencia(
        empresa=empresa.get("nome") or empresa.get("razaoSocial")
        if isinstance(empresa, dict)
        else str(empresa)
        if empresa
        else None,
        cnpj=empresa.get("cnpj") or empresa.get("codigoFormatado")
        if isinstance(empresa, dict)
        else None,
        orgao=orgao.get("nome") if isinstance(orgao, dict) else str(orgao) if orgao else None,
        situacao=raw.get("situacao"),
        data_inicio=raw.get("dataInicioAcordo") or raw.get("dataInicio"),
        data_fim=raw.get("dataFimAcordo") or raw.get("dataFim"),
        valor=raw.get("valorMulta") or raw.get("valor"),
    )


def _parse_nota_fiscal(raw: dict[str, Any]) -> NotaFiscal:
    """Parse an electronic invoice record."""
    emitente = raw.get("emitente") or {}
    return NotaFiscal(
        numero=raw.get("numero"),
        serie=raw.get("serie"),
        emitente=emitente.get("nome") or emitente.get("razaoSocial")
        if isinstance(emitente, dict)
        else str(emitente)
        if emitente
        else None,
        cnpj_emitente=emitente.get("cnpj") if isinstance(emitente, dict) else None,
        valor=raw.get("valor") or raw.get("valorTotal"),
        data_emissao=raw.get("dataEmissao"),
    )


def _parse_beneficio_social(raw: dict[str, Any]) -> BeneficioSocial:
    """Parse a social benefit record."""
    municipio_raw = raw.get("municipio")
    municipio = municipio_raw if isinstance(municipio_raw, dict) else {}
    return BeneficioSocial(
        tipo=raw.get("tipoBeneficio") or raw.get("tipo"),
        nome_beneficiario=raw.get("nomeBeneficiario") or raw.get("nome"),
        cpf=raw.get("cpf"),
        nis=raw.get("nis"),
        valor=raw.get("valor"),
        mes_referencia=raw.get("mesReferencia") or raw.get("dataReferencia"),
        municipio=municipio.get("nomeIBGE")
        if isinstance(municipio, dict)
        else str(municipio_raw)
        if municipio_raw
        else None,
        uf=municipio.get("uf", {}).get("sigla")
        if isinstance(municipio, dict) and isinstance(municipio.get("uf"), dict)
        else None,
    )


def _parse_pessoa_fisica(raw: dict[str, Any]) -> PessoaFisicaVinculos:
    """Parse physical person linkage record."""
    return PessoaFisicaVinculos(
        cpf=raw.get("cpf"),
        nome=raw.get("nome"),
        tipo_vinculo=raw.get("tipoVinculo") or raw.get("tipo"),
        orgao=raw.get("orgao") or raw.get("nomeOrgao"),
        beneficios=raw.get("beneficios"),
    )


def _parse_pessoa_juridica(raw: dict[str, Any]) -> PessoaJuridicaVinculos:
    """Parse juridical person linkage record."""
    return PessoaJuridicaVinculos(
        cnpj=raw.get("cnpj"),
        razao_social=raw.get("razaoSocial") or raw.get("nome"),
        sancoes=raw.get("sancoes"),
        contratos=raw.get("contratos"),
    )


def _parse_contrato_detalhe(raw: dict[str, Any]) -> ContratoDetalhe:
    """Parse a detailed contract record."""
    fornecedor = raw.get("fornecedor") or {}
    orgao = raw.get("unidadeGestora") or raw.get("orgaoVinculado") or {}
    return ContratoDetalhe(
        id=raw.get("id"),
        numero=raw.get("numero"),
        objeto=raw.get("objeto"),
        valor_inicial=raw.get("valorInicial"),
        valor_final=raw.get("valorFinal"),
        data_inicio=raw.get("dataInicioVigencia"),
        data_fim=raw.get("dataFimVigencia"),
        orgao=orgao.get("nome") or orgao.get("descricao"),
        fornecedor=fornecedor.get("nome") or fornecedor.get("razaoSocialReceita"),
        modalidade=raw.get("modalidadeCompra") or raw.get("modalidade"),
        situacao=raw.get("situacao"),
        licitacao=raw.get("licitacao") or raw.get("numeroLicitacao"),
    )


def _parse_servidor_detalhe(raw: dict[str, Any]) -> ServidorDetalhe:
    """Parse a detailed public servant record with compensation."""
    orgao = raw.get("orgaoServidorExercicio") or raw.get("orgaoServidorLotacao") or {}
    return ServidorDetalhe(
        id=raw.get("id"),
        cpf=raw.get("cpf"),
        nome=raw.get("nome"),
        tipo_servidor=raw.get("tipoServidor"),
        situacao=raw.get("situacao"),
        orgao=orgao.get("nome") or orgao.get("descricao"),
        cargo=raw.get("cargo"),
        funcao=raw.get("funcao"),
        remuneracao_basica=raw.get("remuneracaoBasicaBruta"),
        remuneracao_apos_deducoes=raw.get("remuneracaoAposDeducoesObrigatorias"),
        honorarios=raw.get("honorariosAdvocaticios") or raw.get("honorarios"),
        outras_remuneracoes=raw.get("outrasRemuneracoesEventuais"),
        jetons=raw.get("jepiRemuneracao") or raw.get("jetons"),
    )


# --- Public API functions (new endpoints) -----------------------------------


async def buscar_convenios(
    orgao: str | None = None,
    convenente: str | None = None,
    pagina: int = 1,
) -> list[Convenio]:
    """Busca convênios e transferências voluntárias.

    Args:
        orgao: Código do órgão concedente.
        convenente: Nome ou CNPJ do convenente.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if orgao:
        params["codigoOrgao"] = orgao
    if convenente:
        params["convenente"] = convenente
    data = await _get(CONVENIOS_URL, params)
    return _safe_parse_list(data, _parse_convenio, "convenios")


async def buscar_cartoes_pagamento(
    cpf_portador: str | None = None,
    codigo_orgao: str | None = None,
    mes_ano_inicio: str | None = None,
    mes_ano_fim: str | None = None,
    pagina: int = 1,
) -> list[CartaoPagamento]:
    """Busca pagamentos com cartão corporativo/suprimento de fundos.

    Args:
        cpf_portador: CPF do portador do cartão.
        codigo_orgao: Código do órgão.
        mes_ano_inicio: Mês/ano de início no formato MM/AAAA.
        mes_ano_fim: Mês/ano de fim no formato MM/AAAA.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if cpf_portador:
        params["cpfPortador"] = _clean_cpf_cnpj(cpf_portador)
    if codigo_orgao:
        params["codigoOrgao"] = codigo_orgao
    if mes_ano_inicio:
        params["mesExtratoInicio"] = mes_ano_inicio
    if mes_ano_fim:
        params["mesExtratoFim"] = mes_ano_fim
    data = await _get(CARTOES_URL, params)
    return _safe_parse_list(data, _parse_cartao, "cartoes")


async def buscar_pep(
    cpf: str | None = None,
    nome: str | None = None,
    pagina: int = 1,
) -> list[PessoaExpostaPoliticamente]:
    """Busca Pessoas Expostas Politicamente (PEP).

    Args:
        cpf: CPF da pessoa.
        nome: Nome da pessoa.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if cpf:
        params["cpf"] = _clean_cpf_cnpj(cpf)
    elif nome:
        params["nome"] = nome
    data = await _get(PEP_URL, params)
    return _safe_parse_list(data, _parse_pep, "pep")


async def buscar_acordos_leniencia(
    nome_empresa: str | None = None,
    cnpj: str | None = None,
    pagina: int = 1,
) -> list[AcordoLeniencia]:
    """Busca acordos de leniência (anticorrupção).

    Args:
        nome_empresa: Nome da empresa.
        cnpj: CNPJ da empresa.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if nome_empresa:
        params["nomeEmpresa"] = nome_empresa
    if cnpj:
        params["cnpj"] = _clean_cpf_cnpj(cnpj)
    data = await _get(ACORDOS_LENIENCIA_URL, params)
    return _safe_parse_list(data, _parse_acordo_leniencia, "acordos-leniencia")


async def buscar_notas_fiscais(
    cnpj_emitente: str | None = None,
    data_emissao_de: str | None = None,
    data_emissao_ate: str | None = None,
    pagina: int = 1,
) -> list[NotaFiscal]:
    """Busca notas fiscais eletrônicas.

    Args:
        cnpj_emitente: CNPJ do emitente da nota.
        data_emissao_de: Data de emissão inicial DD/MM/AAAA.
        data_emissao_ate: Data de emissão final DD/MM/AAAA.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if cnpj_emitente:
        params["cnpjEmitente"] = _clean_cpf_cnpj(cnpj_emitente)
    if data_emissao_de:
        params["dataEmissaoDe"] = data_emissao_de
    if data_emissao_ate:
        params["dataEmissaoAte"] = data_emissao_ate
    data = await _get(NOTAS_FISCAIS_URL, params)
    return _safe_parse_list(data, _parse_nota_fiscal, "notas-fiscais")


async def consultar_beneficio_social(
    cpf: str | None = None,
    nis: str | None = None,
    mes_ano: str | None = None,
    pagina: int = 1,
) -> list[BeneficioSocial]:
    """Consulta benefícios sociais (BPC, seguro-desemprego, etc.) por CPF/NIS.

    Args:
        cpf: CPF do beneficiário.
        nis: NIS do beneficiário.
        mes_ano: Mês/ano de referência no formato AAAAMM.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"pagina": pagina}
    if cpf:
        params["cpf"] = _clean_cpf_cnpj(cpf)
    if nis:
        params["nis"] = nis
    if mes_ano:
        params["mesAno"] = mes_ano
    data = await _get(BENEFICIOS_CIDADAO_URL, params)
    return _safe_parse_list(data, _parse_beneficio_social, "beneficios-cidadao")


async def consultar_cpf(cpf: str, pagina: int = 1) -> list[PessoaFisicaVinculos]:
    """Consulta vínculos e benefícios por CPF.

    Args:
        cpf: CPF da pessoa física.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"cpf": _clean_cpf_cnpj(cpf), "pagina": pagina}
    data = await _get(PESSOAS_FISICAS_URL, params)
    return _safe_parse_list(data, _parse_pessoa_fisica, "pessoas-fisicas")


async def consultar_cnpj(cnpj: str, pagina: int = 1) -> list[PessoaJuridicaVinculos]:
    """Consulta sanções e contratos por CNPJ.

    Args:
        cnpj: CNPJ da pessoa jurídica.
        pagina: Número da página.
    """
    params: dict[str, Any] = {"cnpj": _clean_cpf_cnpj(cnpj), "pagina": pagina}
    data = await _get(PESSOAS_JURIDICAS_URL, params)
    return _safe_parse_list(data, _parse_pessoa_juridica, "pessoas-juridicas")


async def detalhar_contrato(id_contrato: int) -> ContratoDetalhe | None:
    """Busca detalhe de um contrato específico por ID.

    Args:
        id_contrato: ID do contrato no Portal da Transparência.
    """
    url = f"{CONTRATO_DETALHE_URL}/{id_contrato}"
    data = await _get(url)
    if isinstance(data, dict):
        return _parse_contrato_detalhe(data)
    return None


async def detalhar_servidor(id_servidor: int) -> ServidorDetalhe | None:
    """Busca detalhe completo de um servidor com remuneração.

    Args:
        id_servidor: ID do servidor no Portal da Transparência.
    """
    url = f"{SERVIDOR_DETALHE_URL}/{id_servidor}"
    data = await _get(url)
    if isinstance(data, dict):
        return _parse_servidor_detalhe(data)
    return None
