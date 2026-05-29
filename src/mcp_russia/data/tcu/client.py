"""HTTP client for the TCU APIs.

Endpoints:
    - dados-abertos.apps.tcu.gov.br/api/acordao   → buscar_acordaos
    - contas.tcu.gov.br/ords/condenacao            → consultar_inabilitados, consultar_inidoneos
    - certidoes-apf.apps.tcu.gov.br                → listar_tipos_certidoes, consultar_certidoes
    - divida.apps.tcu.gov.br                       → calcular_debito
    - contas.tcu.gov.br/ords/api/publica/scn       → buscar_pedidos_congresso
    - contas.tcu.gov.br/contrata2RS                → buscar_contratos_tcu
    - dados-abertos.apps.tcu.gov.br/api/cadirreg   → consultar_cadirreg
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get, http_post

from .constants import (
    ACORDAOS_URL,
    CADIRREG_URL,
    CALCULO_DEBITO_URL,
    CERTIDOES_URL,
    DEFAULT_QUANTIDADE_ACORDAOS,
    INABILITADOS_URL,
    INIDONEOS_URL,
    PEDIDOS_CONGRESSO_URL,
    TERMOS_CONTRATUAIS_URL,
    TIPOS_CERTIDOES_URL,
)
from .schemas import (
    Acordao,
    CalculoDebitoResultado,
    CertidaoItem,
    CertidaoResultado,
    Inabilitado,
    InabilitadoResultado,
    Inidoneo,
    InidoneoResultado,
    ParcelaDebito,
    PedidoCongresso,
    PedidoCongressoResultado,
    PessoaCadirreg,
    TermoContratual,
    TipoCertidao,
    UnidadeFiscalizadora,
)

# ---------------------------------------------------------------------------
# Acórdãos
# ---------------------------------------------------------------------------


async def buscar_acordaos(
    *,
    inicio: int = 0,
    quantidade: int = DEFAULT_QUANTIDADE_ACORDAOS,
) -> list[Acordao]:
    """Busca acórdãos do TCU com paginação."""
    params: dict[str, Any] = {"inicio": inicio, "quantidade": quantidade}
    data: list[dict[str, Any]] = await http_get(ACORDAOS_URL, params=params)
    return [
        Acordao(
            key=item.get("key"),
            tipo=item.get("tipo"),
            ano_acordao=item.get("anoAcordao"),
            titulo=item.get("titulo"),
            numero_acordao=item.get("numeroAcordao"),
            numero_ata=item.get("numeroAta"),
            colegiado=item.get("colegiado"),
            data_sessao=item.get("dataSessao"),
            relator=item.get("relator"),
            situacao=item.get("situacao"),
            sumario=item.get("sumario"),
            url_acordao=item.get("urlAcordao"),
        )
        for item in data
    ]


# ---------------------------------------------------------------------------
# Inabilitados
# ---------------------------------------------------------------------------


async def consultar_inabilitados(
    *,
    cpf: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> InabilitadoResultado:
    """Consulta pessoas inabilitadas para função pública."""
    url = f"{INABILITADOS_URL}/{cpf}" if cpf else INABILITADOS_URL
    params: dict[str, Any] = {"offset": offset, "limit": limit}
    data: dict[str, Any] = await http_get(url, params=params)
    items = [
        Inabilitado(
            nome=item.get("nome"),
            cpf=item.get("cpf"),
            processo=item.get("processo"),
            deliberacao=item.get("deliberacao"),
            data_transito_julgado=item.get("data_transito_julgado"),
            data_final=item.get("data_final"),
            data_acordao=item.get("data_acordao"),
            uf=item.get("uf"),
            municipio=item.get("municipio"),
        )
        for item in data.get("items", [])
    ]
    return InabilitadoResultado(
        items=items,
        has_more=data.get("hasMore", False),
        limit=data.get("limit", limit),
        offset=data.get("offset", offset),
        count=data.get("count", len(items)),
    )


# ---------------------------------------------------------------------------
# Inidôneos
# ---------------------------------------------------------------------------


async def consultar_inidoneos(
    *,
    cpf_cnpj: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> InidoneoResultado:
    """Consulta licitantes declarados inidôneos."""
    url = f"{INIDONEOS_URL}/{cpf_cnpj}" if cpf_cnpj else INIDONEOS_URL
    params: dict[str, Any] = {"offset": offset, "limit": limit}
    data: dict[str, Any] = await http_get(url, params=params)
    items = [
        Inidoneo(
            nome=item.get("nome"),
            cpf_cnpj=item.get("cpf_cnpj"),
            processo=item.get("processo"),
            deliberacao=item.get("deliberacao"),
            data_transito_julgado=item.get("data_transito_julgado"),
            data_final=item.get("data_final"),
            data_acordao=item.get("data_acordao"),
            uf=item.get("uf"),
            municipio=item.get("municipio"),
        )
        for item in data.get("items", [])
    ]
    return InidoneoResultado(
        items=items,
        has_more=data.get("hasMore", False),
        limit=data.get("limit", limit),
        offset=data.get("offset", offset),
        count=data.get("count", len(items)),
    )


# ---------------------------------------------------------------------------
# Certidões APF
# ---------------------------------------------------------------------------


async def listar_tipos_certidoes() -> list[TipoCertidao]:
    """Lista tipos de certidões disponíveis no sistema APF."""
    data: list[dict[str, Any]] = await http_get(TIPOS_CERTIDOES_URL)
    return [
        TipoCertidao(
            orgao_emissor=item.get("orgaoEmissor", ""),
            sigla=item.get("sigla", ""),
            descricao=item.get("descricao", ""),
        )
        for item in data
    ]


async def consultar_certidoes(cnpj: str) -> CertidaoResultado:
    """Consulta certidões consolidadas de pessoa jurídica (TCU + CNJ + CGU)."""
    data: dict[str, Any] = await http_get(f"{CERTIDOES_URL}/{cnpj}")
    certidoes = [
        CertidaoItem(
            emissor=c.get("emissor"),
            tipo=c.get("tipo"),
            data_hora_emissao=c.get("dataHoraEmissao"),
            descricao=c.get("descricao"),
            situacao=c.get("situacao"),
            observacao=c.get("observacao"),
            link_consulta_manual=c.get("linkConsultaManual"),
        )
        for c in data.get("certidoes", [])
    ]
    return CertidaoResultado(
        razao_social=data.get("razaoSocial"),
        nome_fantasia=data.get("nomeFantasia"),
        cnpj=data.get("cnpj"),
        uf=data.get("uf"),
        certidoes=certidoes,
        cnpj_encontrado_base_tcu=data.get("seCnpjEncontradoNaBaseTcu", False),
    )


# ---------------------------------------------------------------------------
# Cálculo de débito
# ---------------------------------------------------------------------------


async def calcular_debito(
    data_atualizacao: str,
    aplica_juros: bool,
    parcelas: list[ParcelaDebito],
) -> CalculoDebitoResultado:
    """Calcula débito atualizado com correção monetária (SELIC)."""
    body = {
        "dataAtualizacao": data_atualizacao,
        "aplicaJuros": aplica_juros,
        "parcelasDebito": [
            {
                "dataFato": p.data_fato,
                "indicativoDebitoCredito": p.indicativo_debito_credito,
                "valorOriginal": p.valor_original,
            }
            for p in parcelas
        ],
    }
    data: dict[str, Any] = await http_post(CALCULO_DEBITO_URL, json_body=body)
    return CalculoDebitoResultado(
        data=data.get("data"),
        saldo_debito=data.get("saldoDebito", 0.0),
        saldo_variacao_selic=data.get("saldoVariacaoSelic", 0.0),
        saldo_juros=data.get("saldoJuros", 0.0),
        saldo_total=data.get("saldoTotal", 0.0),
    )


# ---------------------------------------------------------------------------
# Pedidos do Congresso
# ---------------------------------------------------------------------------


async def buscar_pedidos_congresso(
    *,
    processo: str | None = None,
    page: int | None = None,
) -> PedidoCongressoResultado:
    """Busca pedidos do Congresso Nacional ao TCU."""
    url = f"{PEDIDOS_CONGRESSO_URL}/{processo}" if processo else PEDIDOS_CONGRESSO_URL
    params: dict[str, Any] = {}
    if page is not None:
        params["page"] = page
    data: dict[str, Any] = await http_get(url, params=params)
    items = [
        PedidoCongresso(
            tipo=item.get("tipo"),
            numero=item.get("numero"),
            data_aprovacao=item.get("data_aprovacao"),
            assunto=item.get("assunto"),
            autor=item.get("autor"),
            processo_scn=item.get("processo_scn"),
            link_proposicao=item.get("link_proposicao"),
        )
        for item in data.get("items", [])
    ]
    has_next = data.get("next") is not None
    return PedidoCongressoResultado(items=items, has_next=has_next)


# ---------------------------------------------------------------------------
# Termos contratuais do TCU
# ---------------------------------------------------------------------------


async def buscar_contratos_tcu() -> list[TermoContratual]:
    """Busca todos os termos contratuais do TCU."""
    data: list[dict[str, Any]] = await http_get(TERMOS_CONTRATUAIS_URL)
    return [
        TermoContratual(
            tipo_contratacao=item.get("tipoContratacao"),
            numero=item.get("numero"),
            ano=item.get("ano"),
            unidade_gestora=item.get("unidadeGestora"),
            nome_fornecedor=item.get("nomeFornecedor"),
            cnpj_fornecedor=item.get("cnpjFornecedor"),
            objeto=item.get("objeto"),
            valor_inicial=item.get("valorInicial"),
            valor_atualizado=item.get("valorAtualizado"),
            data_assinatura=item.get("dataAssinatura"),
            data_inicio_vigencia=item.get("dataInicioVigencia"),
            data_termino_vigencia=item.get("dataTerminoVigencia"),
            modalidade_licitacao=item.get("modalidadeLicitacao"),
            numero_processo=item.get("numeroProcesso"),
            numero_aditamentos=item.get("numeroAditamentos"),
            unidades_fiscalizadoras=[
                UnidadeFiscalizadora(
                    codigo=u.get("codigo"),
                    sigla=u.get("sigla"),
                    nome=u.get("nome"),
                )
                for u in item.get("unidadesFiscalizadoras", [])
            ],
        )
        for item in data
    ]


# ---------------------------------------------------------------------------
# CADIRREG
# ---------------------------------------------------------------------------


async def consultar_cadirreg(cpf: str) -> list[PessoaCadirreg]:
    """Consulta pessoa no CADIRREG (contas irregulares)."""
    data: list[dict[str, Any]] = await http_get(f"{CADIRREG_URL}/{cpf}")
    return [
        PessoaCadirreg(
            nome_responsavel=item.get("nomeResponsavel"),
            cpf=item.get("numCPF"),
            num_processo=item.get("numProcesso"),
            ano_processo=item.get("anoProcesso"),
            julgamento=item.get("julgamento"),
            unidade_tecnica_processo=item.get("unidadeTecnicaProcesso"),
            se_detentor_cargo_funcao_publica=item.get("seDetentorCargoFuncaoPublica"),
            se_falecido=item.get("seFalecido"),
        )
        for item in data
    ]
