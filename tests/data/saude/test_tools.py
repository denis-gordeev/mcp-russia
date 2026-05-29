"""Tests for the Saúde tool functions.

Tools are tested by mocking client functions (never HTTP).
Context is mocked via MagicMock with async methods.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_russia.data.saude import tools
from mcp_russia.data.saude.schemas import (
    Estabelecimento,
    Leito,
    Profissional,
    TipoEstabelecimento,
)

CLIENT_MODULE = "mcp_russia.data.saude.client"


def _mock_ctx() -> MagicMock:
    """Create a mock Context with async log methods."""
    ctx = MagicMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# ---------------------------------------------------------------------------
# buscar_estabelecimentos
# ---------------------------------------------------------------------------


class TestBuscarEstabelecimentos:
    @pytest.mark.asyncio
    async def test_formats_table(self) -> None:
        mock_data = [
            Estabelecimento(
                codigo_cnes="1234567",
                nome_fantasia="UBS Central",
                descricao_tipo="Central de Regulação",
                tipo_gestao="Municipal",
                endereco="Rua ABC, 123",
            ),
            Estabelecimento(
                codigo_cnes="7654321",
                nome_fantasia="Hospital Geral",
                descricao_tipo="Hospital Geral",
                tipo_gestao="Estadual",
                endereco="Av XYZ, 456",
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_estabelecimentos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_estabelecimentos(ctx, codigo_municipio="355030")
        assert "UBS Central" in result
        assert "1234567" in result
        assert "Hospital Geral" in result
        assert "2 resultados" in result

    @pytest.mark.asyncio
    async def test_empty(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_estabelecimentos",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.buscar_estabelecimentos(ctx)
        assert "Nenhum estabelecimento" in result

    @pytest.mark.asyncio
    async def test_missing_fields_use_dash(self) -> None:
        mock_data = [Estabelecimento()]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_estabelecimentos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_estabelecimentos(ctx)
        assert "—" in result


# ---------------------------------------------------------------------------
# buscar_profissionais
# ---------------------------------------------------------------------------


class TestBuscarProfissionais:
    @pytest.mark.asyncio
    async def test_formats_table(self) -> None:
        mock_data = [
            Profissional(
                codigo_cnes="1234567",
                nome="João Silva",
                cbo="225125",
                descricao_cbo="Médico generalista",
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_profissionais",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_profissionais(ctx, cnes="1234567")
        assert "João Silva" in result
        assert "225125" in result
        assert "Médico generalista" in result
        assert "1 resultados" in result

    @pytest.mark.asyncio
    async def test_empty(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_profissionais",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.buscar_profissionais(ctx)
        assert "Nenhum profissional" in result


# ---------------------------------------------------------------------------
# listar_tipos_estabelecimento
# ---------------------------------------------------------------------------


class TestListarTiposEstabelecimento:
    @pytest.mark.asyncio
    async def test_formats_table(self) -> None:
        mock_data = [
            TipoEstabelecimento(codigo="01", descricao="Central de Regulação"),
            TipoEstabelecimento(codigo="02", descricao="Hospital Geral"),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.listar_tipos_estabelecimento",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.listar_tipos_estabelecimento(ctx)
        assert "Central de Regulação" in result
        assert "Hospital Geral" in result
        assert "2 tipos" in result

    @pytest.mark.asyncio
    async def test_empty(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.listar_tipos_estabelecimento",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.listar_tipos_estabelecimento(ctx)
        assert "Nenhum tipo" in result


# ---------------------------------------------------------------------------
# consultar_leitos
# ---------------------------------------------------------------------------


class TestConsultarLeitos:
    @pytest.mark.asyncio
    async def test_formats_table_with_totals(self) -> None:
        mock_data = [
            Leito(
                codigo_cnes="1234567",
                tipo_leito="Cirúrgico",
                especialidade="Cirurgia Geral",
                existente=20,
                sus=15,
            ),
            Leito(
                codigo_cnes="1234567",
                tipo_leito="Clínico",
                especialidade="Clínica Médica",
                existente=30,
                sus=25,
            ),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_leitos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_leitos(ctx, cnes="1234567")
        assert "Cirúrgico" in result
        assert "Clínico" in result
        assert "2 registros" in result
        # Check totals: 50 existentes, 40 SUS
        assert "50" in result
        assert "40" in result

    @pytest.mark.asyncio
    async def test_empty(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_leitos",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await tools.consultar_leitos(ctx)
        assert "Nenhum leito" in result

    @pytest.mark.asyncio
    async def test_none_values_handled(self) -> None:
        mock_data = [
            Leito(codigo_cnes="1234567", existente=None, sus=None),
        ]
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.consultar_leitos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.consultar_leitos(ctx)
        assert "—" in result
