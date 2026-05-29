"""Tests for the Dados Abertos tool functions.

Tools are tested by mocking client functions (never HTTP).
Context is mocked via MagicMock with async methods.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_russia.data.dados_abertos import tools
from mcp_russia.data.dados_abertos.schemas import (
    ConjuntoDados,
    ConjuntoResultado,
    Organizacao,
    OrganizacaoResultado,
    RecursoDados,
    RecursoResultado,
)

CLIENT_MODULE = "mcp_russia.data.dados_abertos.client"


def _mock_ctx() -> MagicMock:
    """Create a mock Context with async log methods."""
    ctx = MagicMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


# ---------------------------------------------------------------------------
# buscar_conjuntos
# ---------------------------------------------------------------------------


class TestBuscarConjuntos:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = ConjuntoResultado(
            total=1,
            conjuntos=[
                ConjuntoDados(
                    id="abc-123",
                    titulo="Dados de Saúde Pública",
                    descricao="Indicadores de saúde do SUS",
                    organizacao_nome="Ministério da Saúde",
                    temas=["Saúde", "SUS"],
                    tags=["saude", "indicadores"],
                    data_criacao="2023-01-15",
                    data_atualizacao="2024-06-20",
                ),
            ],
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_conjuntos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_conjuntos("saúde", ctx)
        assert "Dados de Saúde Pública" in result
        assert "Ministério da Saúde" in result
        assert "abc-123" in result
        assert "Saúde" in result
        assert "2024-06-20" in result
        assert "1 conjuntos de dados" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        mock_data = ConjuntoResultado(total=0, conjuntos=[])
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_conjuntos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_conjuntos("xyzinexistente", ctx)
        assert "Nenhum conjunto de dados encontrado" in result
        assert "xyzinexistente" in result

    @pytest.mark.asyncio
    async def test_pagination_hint(self) -> None:
        mock_data = ConjuntoResultado(
            total=25,
            conjuntos=[ConjuntoDados(id=f"id-{i}", titulo=f"Dataset {i}") for i in range(10)],
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_conjuntos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_conjuntos("dados", ctx, pagina=1)
        assert "pagina=2" in result


# ---------------------------------------------------------------------------
# detalhar_conjunto
# ---------------------------------------------------------------------------


class TestDetalharConjunto:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = ConjuntoDados(
            id="abc-123",
            titulo="Dados de Educação",
            descricao="Indicadores educacionais do INEP",
            organizacao_nome="Ministério da Educação",
            temas=["Educação"],
            tags=["inep", "censo-escolar"],
            data_criacao="2022-05-10",
            data_atualizacao="2024-03-01",
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.detalhar_conjunto",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.detalhar_conjunto("abc-123", ctx)
        assert "Dados de Educação" in result
        assert "Indicadores educacionais do INEP" in result
        assert "Ministério da Educação" in result
        assert "Educação" in result
        assert "inep" in result
        assert "censo-escolar" in result
        assert "2022-05-10" in result
        assert "2024-03-01" in result
        assert "buscar_recursos" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.detalhar_conjunto",
            new_callable=AsyncMock,
            return_value=None,
        ):
            result = await tools.detalhar_conjunto("nao-existe", ctx)
        assert "não encontrado" in result
        assert "nao-existe" in result


# ---------------------------------------------------------------------------
# listar_organizacoes
# ---------------------------------------------------------------------------


class TestListarOrganizacoes:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = OrganizacaoResultado(
            total=2,
            organizacoes=[
                Organizacao(
                    id="org-1",
                    nome="Ministério da Saúde",
                    descricao="Saúde pública",
                    total_conjuntos=150,
                ),
                Organizacao(
                    id="org-2",
                    nome="IBGE",
                    descricao="Estatísticas",
                    total_conjuntos=80,
                ),
            ],
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.listar_organizacoes",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.listar_organizacoes(ctx)
        assert "Ministério da Saúde" in result
        assert "IBGE" in result
        assert "150" in result
        assert "80" in result
        assert "2 organizações" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        mock_data = OrganizacaoResultado(total=0, organizacoes=[])
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.listar_organizacoes",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.listar_organizacoes(ctx)
        assert "Nenhuma organização encontrada" in result


# ---------------------------------------------------------------------------
# buscar_recursos
# ---------------------------------------------------------------------------


class TestBuscarRecursos:
    @pytest.mark.asyncio
    async def test_formats_results(self) -> None:
        mock_data = RecursoResultado(
            total=2,
            recursos=[
                RecursoDados(
                    id="rec-1",
                    titulo="Dados CSV 2024",
                    link="https://dados.gov.br/download/arquivo.csv",
                    formato="CSV",
                    descricao="Arquivo com dados completos",
                ),
                RecursoDados(
                    id="rec-2",
                    titulo="API REST",
                    link="https://api.dados.gov.br/endpoint",
                    formato="API",
                    descricao="Interface programática",
                ),
            ],
        )
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_recursos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_recursos("abc-123", ctx)
        assert "Dados CSV 2024" in result
        assert "CSV" in result
        assert "https://dados.gov.br/download/arquivo.csv" in result
        assert "API REST" in result
        assert "API" in result
        assert "2 recursos" in result

    @pytest.mark.asyncio
    async def test_empty_results(self) -> None:
        mock_data = RecursoResultado(total=0, recursos=[])
        ctx = _mock_ctx()
        with patch(
            f"{CLIENT_MODULE}.buscar_recursos",
            new_callable=AsyncMock,
            return_value=mock_data,
        ):
            result = await tools.buscar_recursos("nao-existe", ctx)
        assert "Nenhum recurso encontrado" in result
        assert "nao-existe" in result
