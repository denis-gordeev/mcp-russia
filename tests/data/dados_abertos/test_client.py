"""Tests for the Dados Abertos HTTP client."""

import httpx
import pytest
import respx

from mcp_russia.data.dados_abertos import client
from mcp_russia.data.dados_abertos.constants import CONJUNTOS_URL, ORGANIZACOES_URL, RECURSOS_URL

# ---------------------------------------------------------------------------
# buscar_conjuntos
# ---------------------------------------------------------------------------


class TestBuscarConjuntos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_conjuntos(self) -> None:
        respx.get(CONJUNTOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalRegistros": 1,
                    "registros": [
                        {
                            "id": "abc-123",
                            "titulo": "Dados de Saúde",
                            "descricao": "Indicadores SUS",
                            "organizacao": {"nome": "Ministério da Saúde"},
                            "temas": [{"titulo": "Saúde"}],
                            "tags": [{"nome": "sus"}],
                            "dataCriacao": "2023-01-15",
                            "dataAtualizacao": "2024-06-20",
                        }
                    ],
                },
            )
        )
        result = await client.buscar_conjuntos(query="saúde")
        assert result.total == 1
        assert len(result.conjuntos) == 1
        c = result.conjuntos[0]
        assert c.id == "abc-123"
        assert c.titulo == "Dados de Saúde"
        assert c.descricao == "Indicadores SUS"
        assert c.organizacao_nome == "Ministério da Saúde"
        assert c.temas == ["Saúde"]
        assert c.tags == ["sus"]
        assert c.data_criacao == "2023-01-15"
        assert c.data_atualizacao == "2024-06-20"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(CONJUNTOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={"totalRegistros": 0, "registros": []},
            )
        )
        result = await client.buscar_conjuntos(query="inexistente")
        assert result.total == 0
        assert result.conjuntos == []

    @pytest.mark.asyncio
    @respx.mock
    async def test_string_temas_and_tags(self) -> None:
        """Test fallback when temas/tags are plain strings instead of dicts."""
        respx.get(CONJUNTOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalRegistros": 1,
                    "registros": [
                        {
                            "id": "xyz-789",
                            "titulo": "Dados Simples",
                            "organizacao": {"nome": "IBGE"},
                            "temas": ["Economia", "Finanças"],
                            "tags": ["pib", "renda"],
                        }
                    ],
                },
            )
        )
        result = await client.buscar_conjuntos(query="economia")
        c = result.conjuntos[0]
        assert c.temas == ["Economia", "Finanças"]
        assert c.tags == ["pib", "renda"]


# ---------------------------------------------------------------------------
# detalhar_conjunto
# ---------------------------------------------------------------------------


class TestDetalharConjunto:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_detail(self) -> None:
        respx.get(f"{CONJUNTOS_URL}/abc-123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "abc-123",
                    "titulo": "Dados de Educação",
                    "descricao": "Indicadores educacionais",
                    "organizacao": {"nome": "MEC"},
                    "temas": [{"titulo": "Educação"}],
                    "tags": [{"nome": "inep"}],
                    "dataCriacao": "2022-05-10",
                    "dataAtualizacao": "2024-03-01",
                },
            )
        )
        result = await client.detalhar_conjunto("abc-123")
        assert result is not None
        assert result.id == "abc-123"
        assert result.titulo == "Dados de Educação"
        assert result.organizacao_nome == "MEC"
        assert result.temas == ["Educação"]
        assert result.tags == ["inep"]

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response_returns_none(self) -> None:
        respx.get(f"{CONJUNTOS_URL}/nao-existe").mock(return_value=httpx.Response(200, json={}))
        result = await client.detalhar_conjunto("nao-existe")
        assert result is None


# ---------------------------------------------------------------------------
# listar_organizacoes
# ---------------------------------------------------------------------------


class TestListarOrganizacoes:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_organizacoes(self) -> None:
        respx.get(ORGANIZACOES_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalRegistros": 2,
                    "registros": [
                        {
                            "id": "org-1",
                            "nome": "Ministério da Saúde",
                            "descricao": "Saúde pública",
                            "totalConjuntoDados": 150,
                        },
                        {
                            "id": "org-2",
                            "nome": "IBGE",
                            "descricao": "Estatísticas",
                            "totalConjuntoDados": 80,
                        },
                    ],
                },
            )
        )
        result = await client.listar_organizacoes()
        assert result.total == 2
        assert len(result.organizacoes) == 2
        o1 = result.organizacoes[0]
        assert o1.id == "org-1"
        assert o1.nome == "Ministério da Saúde"
        assert o1.total_conjuntos == 150
        o2 = result.organizacoes[1]
        assert o2.nome == "IBGE"
        assert o2.total_conjuntos == 80

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(ORGANIZACOES_URL).mock(
            return_value=httpx.Response(
                200,
                json={"totalRegistros": 0, "registros": []},
            )
        )
        result = await client.listar_organizacoes()
        assert result.total == 0
        assert result.organizacoes == []


# ---------------------------------------------------------------------------
# buscar_recursos
# ---------------------------------------------------------------------------


class TestBuscarRecursos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_recursos(self) -> None:
        respx.get(RECURSOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalRegistros": 2,
                    "registros": [
                        {
                            "id": "rec-1",
                            "titulo": "Dados CSV",
                            "link": "https://dados.gov.br/download/dados.csv",
                            "formato": "CSV",
                            "descricao": "Arquivo CSV completo",
                        },
                        {
                            "id": "rec-2",
                            "titulo": "API JSON",
                            "link": "https://api.dados.gov.br/v1",
                            "formato": "API",
                            "descricao": "Endpoint REST",
                        },
                    ],
                },
            )
        )
        result = await client.buscar_recursos("abc-123")
        assert result.total == 2
        assert len(result.recursos) == 2
        r1 = result.recursos[0]
        assert r1.id == "rec-1"
        assert r1.titulo == "Dados CSV"
        assert r1.link == "https://dados.gov.br/download/dados.csv"
        assert r1.formato == "CSV"
        assert r1.descricao == "Arquivo CSV completo"
        r2 = result.recursos[1]
        assert r2.titulo == "API JSON"
        assert r2.formato == "API"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(RECURSOS_URL).mock(
            return_value=httpx.Response(
                200,
                json={"totalRegistros": 0, "registros": []},
            )
        )
        result = await client.buscar_recursos("nao-existe")
        assert result.total == 0
        assert result.recursos == []
