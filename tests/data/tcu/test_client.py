"""Tests for the TCU HTTP client."""

import httpx
import pytest
import respx

from mcp_russia.data.tcu import client
from mcp_russia.data.tcu.constants import (
    ACORDAOS_URL,
    CADIRREG_URL,
    CALCULO_DEBITO_URL,
    CERTIDOES_URL,
    INABILITADOS_URL,
    INIDONEOS_URL,
    PEDIDOS_CONGRESSO_URL,
    TERMOS_CONTRATUAIS_URL,
    TIPOS_CERTIDOES_URL,
)
from mcp_russia.data.tcu.schemas import ParcelaDebito

# ---------------------------------------------------------------------------
# buscar_acordaos
# ---------------------------------------------------------------------------


class TestBuscarAcordaos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_acordaos(self) -> None:
        respx.get(ACORDAOS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "key": "ACORDAO-COMPLETO-123",
                        "tipo": "ACORDAO",
                        "anoAcordao": "2026",
                        "titulo": "ACORDAO 100/2026 ATA 2/2026 - PLENARIO",
                        "numeroAcordao": "100",
                        "numeroAta": "2/2026",
                        "colegiado": "Plenario",
                        "dataSessao": "18/03/2026",
                        "relator": "BRUNO DANTAS",
                        "situacao": "OFICIALIZADO",
                        "sumario": "Embargos de declaração...",
                        "urlAcordao": "https://contas.tcu.gov.br/...",
                    }
                ],
            )
        )
        result = await client.buscar_acordaos(inicio=0, quantidade=10)
        assert len(result) == 1
        assert result[0].key == "ACORDAO-COMPLETO-123"
        assert result[0].colegiado == "Plenario"
        assert result[0].relator == "BRUNO DANTAS"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(ACORDAOS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.buscar_acordaos()
        assert result == []


# ---------------------------------------------------------------------------
# consultar_inabilitados
# ---------------------------------------------------------------------------


class TestConsultarInabilitados:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_inabilitados(self) -> None:
        respx.get(INABILITADOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "nome": "FULANO DA SILVA",
                            "cpf": "123.456.789-00",
                            "processo": "026.615/2020-7",
                            "deliberacao": "AC-000738/2022-PL",
                            "data_transito_julgado": "2022-07-16T03:00:00Z",
                            "data_final": "2027-07-16T03:00:00Z",
                            "uf": "MA",
                            "municipio": "SANTA INES",
                        }
                    ],
                    "hasMore": True,
                    "limit": 25,
                    "offset": 0,
                    "count": 25,
                },
            )
        )
        result = await client.consultar_inabilitados()
        assert len(result.items) == 1
        assert result.items[0].nome == "FULANO DA SILVA"
        assert result.has_more is True

    @pytest.mark.asyncio
    @respx.mock
    async def test_by_cpf(self) -> None:
        respx.get(f"{INABILITADOS_URL}/12345678900").mock(
            return_value=httpx.Response(
                200,
                json={"items": [], "hasMore": False, "limit": 25, "offset": 0, "count": 0},
            )
        )
        result = await client.consultar_inabilitados(cpf="12345678900")
        assert result.items == []


# ---------------------------------------------------------------------------
# consultar_inidoneos
# ---------------------------------------------------------------------------


class TestConsultarInidoneos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_inidoneos(self) -> None:
        respx.get(INIDONEOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "nome": "EMPRESA LTDA",
                            "cpf_cnpj": "07.405.573/0001-44",
                            "processo": "007.720/2012-2",
                            "deliberacao": "AC-002099/2015-PL",
                            "data_final": "2026-09-30T03:00:00Z",
                            "uf": "DF",
                        }
                    ],
                    "hasMore": False,
                    "limit": 25,
                    "offset": 0,
                    "count": 1,
                },
            )
        )
        result = await client.consultar_inidoneos()
        assert len(result.items) == 1
        assert result.items[0].cpf_cnpj == "07.405.573/0001-44"
        assert result.has_more is False


# ---------------------------------------------------------------------------
# listar_tipos_certidoes
# ---------------------------------------------------------------------------


class TestListarTiposCertidoes:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_tipos(self) -> None:
        respx.get(TIPOS_CERTIDOES_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "orgaoEmissor": "TCU",
                        "sigla": "Inidoneos",
                        "descricao": "Licitantes Inidoneos",
                    },
                    {
                        "orgaoEmissor": "CNJ",
                        "sigla": "CNIA",
                        "descricao": "CNIA",
                    },
                ],
            )
        )
        result = await client.listar_tipos_certidoes()
        assert len(result) == 2
        assert result[0].sigla == "Inidoneos"
        assert result[1].orgao_emissor == "CNJ"


# ---------------------------------------------------------------------------
# consultar_certidoes
# ---------------------------------------------------------------------------


class TestConsultarCertidoes:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_certidoes(self) -> None:
        respx.get(f"{CERTIDOES_URL}/00000000000191").mock(
            return_value=httpx.Response(
                200,
                json={
                    "razaoSocial": "Banco do Brasil S.A.",
                    "nomeFantasia": "BB",
                    "cnpj": "00.000.000/0001-91",
                    "uf": None,
                    "certidoes": [
                        {
                            "emissor": "TCU",
                            "tipo": "Inidoneos",
                            "dataHoraEmissao": "22/03/2026 23:14",
                            "descricao": "Licitantes Inidoneos",
                            "situacao": "NADA_CONSTA",
                            "observacao": None,
                            "linkConsultaManual": "https://contas.tcu.gov.br/...",
                        }
                    ],
                    "seCnpjEncontradoNaBaseTcu": True,
                },
            )
        )
        result = await client.consultar_certidoes("00000000000191")
        assert result.razao_social == "Banco do Brasil S.A."
        assert len(result.certidoes) == 1
        assert result.certidoes[0].situacao == "NADA_CONSTA"
        assert result.cnpj_encontrado_base_tcu is True


# ---------------------------------------------------------------------------
# calcular_debito
# ---------------------------------------------------------------------------


class TestCalcularDebito:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_calculo(self) -> None:
        respx.post(CALCULO_DEBITO_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": "22/03/2026",
                    "saldoDebito": 1000.0,
                    "saldoVariacaoSelic": 577.38,
                    "saldoJuros": 0.0,
                    "saldoTotal": 1577.38,
                },
            )
        )
        parcela = ParcelaDebito(
            data_fato="01/01/2020",
            indicativo_debito_credito="D",
            valor_original=1000.0,
        )
        result = await client.calcular_debito(
            data_atualizacao="22/03/2026",
            aplica_juros=True,
            parcelas=[parcela],
        )
        assert result.saldo_total == 1577.38
        assert result.saldo_variacao_selic == 577.38


# ---------------------------------------------------------------------------
# buscar_pedidos_congresso
# ---------------------------------------------------------------------------


class TestBuscarPedidosCongresso:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_pedidos(self) -> None:
        respx.get(PEDIDOS_CONGRESSO_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "tipo": "REQ",
                            "numero": 4,
                            "data_aprovacao": "2026-02-19T03:00:00Z",
                            "assunto": "Requerimento de informações...",
                            "autor": "Dr. Hiran",
                            "processo_scn": "004.808/2026-6",
                            "link_proposicao": "https://senado.leg.br/...",
                        }
                    ],
                    "next": {"$ref": "http://contas.tcu.gov.br/...?page=1"},
                },
            )
        )
        result = await client.buscar_pedidos_congresso()
        assert len(result.items) == 1
        assert result.items[0].autor == "Dr. Hiran"
        assert result.has_next is True

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(PEDIDOS_CONGRESSO_URL).mock(return_value=httpx.Response(200, json={"items": []}))
        result = await client.buscar_pedidos_congresso()
        assert result.items == []
        assert result.has_next is False


# ---------------------------------------------------------------------------
# buscar_contratos_tcu
# ---------------------------------------------------------------------------


class TestBuscarContratosTcu:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_contratos(self) -> None:
        respx.get(TERMOS_CONTRATUAIS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "tipoContratacao": "CONTRATACAO POR NOTA DE EMPENHO",
                        "numero": 3,
                        "ano": 2025,
                        "unidadeGestora": "SEC-RJ",
                        "nomeFornecedor": "LABORATORIO RICHET",
                        "cnpjFornecedor": "31887136000199",
                        "objeto": "Contratação de laboratório",
                        "valorInicial": 5271.82,
                        "valorAtualizado": 5271.82,
                        "dataAssinatura": "2025-10-20T00:00:00-0300",
                        "dataInicioVigencia": "2025-10-28T00:00:00-0300",
                        "dataTerminoVigencia": "2025-12-31T00:00:00-0300",
                        "modalidadeLicitacao": "DISPENSA DE LICITACAO",
                        "numeroProcesso": "017.866/2025-1",
                        "numeroAditamentos": 0,
                        "unidadesFiscalizadoras": [
                            {"codigo": 300046, "sigla": "SEC-RJ", "nome": "Sec RJ"}
                        ],
                    }
                ],
            )
        )
        result = await client.buscar_contratos_tcu()
        assert len(result) == 1
        assert result[0].nome_fornecedor == "LABORATORIO RICHET"
        assert result[0].valor_inicial == 5271.82
        assert len(result[0].unidades_fiscalizadoras) == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(TERMOS_CONTRATUAIS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.buscar_contratos_tcu()
        assert result == []


# ---------------------------------------------------------------------------
# consultar_cadirreg
# ---------------------------------------------------------------------------


class TestConsultarCadirreg:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_registros(self) -> None:
        respx.get(f"{CADIRREG_URL}/12345678900").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "nomeResponsavel": "FULANO DE TAL",
                        "numCPF": "12345678900",
                        "numProcesso": "012345",
                        "anoProcesso": "2020",
                        "julgamento": "Contas irregulares",
                        "unidadeTecnicaProcesso": "SECEX-MA",
                        "seDetentorCargoFuncaoPublica": "Sim",
                        "seFalecido": "Nao",
                    }
                ],
            )
        )
        result = await client.consultar_cadirreg("12345678900")
        assert len(result) == 1
        assert result[0].nome_responsavel == "FULANO DE TAL"
        assert result[0].cpf == "12345678900"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(f"{CADIRREG_URL}/00000000000").mock(return_value=httpx.Response(200, json=[]))
        result = await client.consultar_cadirreg("00000000000")
        assert result == []
