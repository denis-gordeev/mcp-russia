"""Tests for the TCU tool functions."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_russia.data.tcu import tools
from mcp_russia.data.tcu.schemas import (
    Acordao,
    CalculoDebitoResultado,
    CertidaoItem,
    CertidaoResultado,
    Inabilitado,
    InabilitadoResultado,
    Inidoneo,
    InidoneoResultado,
    PedidoCongresso,
    PedidoCongressoResultado,
    PessoaCadirreg,
    TermoContratual,
)

CLIENT_MODULE = "mcp_russia.data.tcu.client"


def _mock_ctx() -> MagicMock:
    ctx = MagicMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# ---------------------------------------------------------------------------
# buscar_acordaos
# ---------------------------------------------------------------------------


class TestBuscarAcordaos:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = [
            Acordao(
                key="ACORDAO-123",
                titulo="ACORDAO 100/2026 - PLENARIO",
                colegiado="Plenario",
                relator="BRUNO DANTAS",
                data_sessao="18/03/2026",
                situacao="OFICIALIZADO",
                sumario="Embargos de declaração em pedido de reconsideração",
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_acordaos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_acordaos(ctx)
        assert "ACORDAO 100/2026 - PLENARIO" in result
        assert "BRUNO DANTAS" in result
        assert "Plenario" in result
        assert "Embargos de declaração" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_acordaos",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.buscar_acordaos(ctx)
        assert "Nenhum acórdão encontrado" in result


# ---------------------------------------------------------------------------
# consultar_inabilitados
# ---------------------------------------------------------------------------


class TestConsultarInabilitados:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = InabilitadoResultado(
            items=[
                Inabilitado(
                    nome="FULANO DA SILVA",
                    cpf="123.456.789-00",
                    processo="026.615/2020-7",
                    deliberacao="AC-000738/2022-PL",
                    data_final="2027-07-16T03:00:00Z",
                    uf="MA",
                ),
            ],
            has_more=False,
            count=1,
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_inabilitados",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_inabilitados(ctx)
        assert "FULANO DA SILVA" in result
        assert "123.456.789-00" in result
        assert "026.615/2020-7" in result

    @pytest.mark.asyncio
    async def test_not_found_by_cpf(self) -> None:
        mock_data = InabilitadoResultado(items=[], count=0)
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_inabilitados",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_inabilitados(ctx, cpf="12345678900")
        assert "não consta" in result


# ---------------------------------------------------------------------------
# consultar_inidoneos
# ---------------------------------------------------------------------------


class TestConsultarInidoneos:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = InidoneoResultado(
            items=[
                Inidoneo(
                    nome="EMPRESA LTDA",
                    cpf_cnpj="07.405.573/0001-44",
                    processo="007.720/2012-2",
                    uf="DF",
                ),
            ],
            count=1,
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_inidoneos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_inidoneos(ctx)
        assert "EMPRESA LTDA" in result
        assert "07.405.573/0001-44" in result

    @pytest.mark.asyncio
    async def test_not_found_by_cnpj(self) -> None:
        mock_data = InidoneoResultado(items=[], count=0)
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_inidoneos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_inidoneos(ctx, cpf_cnpj="12345678000100")
        assert "não consta" in result


# ---------------------------------------------------------------------------
# consultar_certidoes_apf
# ---------------------------------------------------------------------------


class TestConsultarCertidoesApf:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = CertidaoResultado(
            razao_social="Banco do Brasil S.A.",
            nome_fantasia="BB",
            cnpj="00.000.000/0001-91",
            certidoes=[
                CertidaoItem(
                    emissor="TCU",
                    tipo="Inidoneos",
                    situacao="NADA_CONSTA",
                ),
                CertidaoItem(
                    emissor="CNJ",
                    tipo="CNIA",
                    situacao="NADA_CONSTA",
                ),
            ],
            cnpj_encontrado_base_tcu=True,
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_certidoes",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_certidoes_apf("00000000000191", ctx)
        assert "Banco do Brasil" in result
        assert "TCU" in result
        assert "Nada consta" in result


# ---------------------------------------------------------------------------
# calcular_debito_tcu
# ---------------------------------------------------------------------------


class TestCalcularDebitoTcu:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = CalculoDebitoResultado(
            data="22/03/2026",
            saldo_debito=1000.0,
            saldo_variacao_selic=577.38,
            saldo_juros=0.0,
            saldo_total=1577.38,
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.calcular_debito",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.calcular_debito_tcu("22/03/2026", "01/01/2020", 1000.0, ctx)
        assert "1 000,00 ₽" in result
        assert "577,38 ₽" in result
        assert "1 577,38 ₽" in result


# ---------------------------------------------------------------------------
# buscar_pedidos_congresso
# ---------------------------------------------------------------------------


class TestBuscarPedidosCongresso:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = PedidoCongressoResultado(
            items=[
                PedidoCongresso(
                    tipo="REQ",
                    numero=4,
                    autor="Dr. Hiran",
                    processo_scn="004.808/2026-6",
                    assunto="Requerimento de informações...",
                ),
            ],
            has_next=False,
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_pedidos_congresso",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_pedidos_congresso(ctx)
        assert "Dr. Hiran" in result
        assert "004.808/2026-6" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        mock_data = PedidoCongressoResultado(items=[])
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_pedidos_congresso",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_pedidos_congresso(ctx)
        assert "Nenhum pedido" in result


# ---------------------------------------------------------------------------
# buscar_contratos_tcu
# ---------------------------------------------------------------------------


class TestBuscarContratosTcu:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = [
            TermoContratual(
                tipo_contratacao="CONTRATACAO POR NOTA DE EMPENHO",
                numero=3,
                ano=2025,
                nome_fornecedor="LABORATORIO RICHET",
                objeto="Contratação de laboratório",
                valor_atualizado=5271.82,
                modalidade_licitacao="DISPENSA DE LICITACAO",
                numero_processo="017.866/2025-1",
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_contratos_tcu",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_contratos_tcu(ctx)
        assert "LABORATORIO RICHET" in result
        assert "5 271,82 ₽" in result
        assert "017.866/2025-1" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_contratos_tcu",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.buscar_contratos_tcu(ctx)
        assert "Nenhum contrato" in result


# ---------------------------------------------------------------------------
# consultar_cadirreg
# ---------------------------------------------------------------------------


class TestConsultarCadirreg:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = [
            PessoaCadirreg(
                nome_responsavel="FULANO DE TAL",
                cpf="12345678900",
                num_processo="012345",
                ano_processo="2020",
                julgamento="Contas irregulares",
                unidade_tecnica_processo="SECEX-MA",
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_cadirreg",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_cadirreg("12345678900", ctx)
        assert "FULANO DE TAL" in result
        assert "012345" in result
        assert "SECEX-MA" in result

    @pytest.mark.asyncio
    async def test_not_found(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_cadirreg",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.consultar_cadirreg("00000000000", ctx)
        assert "não consta" in result
