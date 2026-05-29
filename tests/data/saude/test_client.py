"""Tests for the Saúde HTTP client."""

import httpx
import pytest
import respx

from mcp_russia.data.saude import client
from mcp_russia.data.saude.constants import (
    ESTABELECIMENTOS_URL,
    LEITOS_URL,
    PROFISSIONAIS_URL,
    TIPOS_URL,
)

# ---------------------------------------------------------------------------
# buscar_estabelecimentos
# ---------------------------------------------------------------------------


class TestBuscarEstabelecimentos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_establishments(self) -> None:
        respx.get(ESTABELECIMENTOS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "codigo_cnes": "1234567",
                        "nome_fantasia": "UBS Central",
                        "nome_razao_social": "Unidade Básica de Saúde Central",
                        "natureza_organizacao": "Administração Pública",
                        "tipo_gestao": "Municipal",
                        "codigo_tipo_estabelecimento": "01",
                        "descricao_tipo_estabelecimento": "Central de Regulação",
                        "codigo_municipio": "355030",
                        "codigo_uf": "35",
                        "endereco": "Rua ABC, 123",
                    }
                ],
            )
        )
        result = await client.buscar_estabelecimentos(codigo_municipio="355030")
        assert len(result) == 1
        assert result[0].codigo_cnes == "1234567"
        assert result[0].nome_fantasia == "UBS Central"
        assert result[0].codigo_municipio == "355030"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(ESTABELECIMENTOS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.buscar_estabelecimentos()
        assert result == []

    @pytest.mark.asyncio
    @respx.mock
    async def test_sends_query_params(self) -> None:
        route = respx.get(ESTABELECIMENTOS_URL).mock(return_value=httpx.Response(200, json=[]))
        await client.buscar_estabelecimentos(
            codigo_municipio="355030", codigo_uf="35", status=1, limit=10, offset=5
        )
        req_url = str(route.calls[0].request.url)
        assert "codigo_municipio=355030" in req_url
        assert "codigo_uf=35" in req_url
        assert "status=1" in req_url
        assert "limit=10" in req_url
        assert "offset=5" in req_url

    @pytest.mark.asyncio
    @respx.mock
    async def test_limit_capped_at_max(self) -> None:
        route = respx.get(ESTABELECIMENTOS_URL).mock(return_value=httpx.Response(200, json=[]))
        await client.buscar_estabelecimentos(limit=999)
        req_url = str(route.calls[0].request.url)
        assert "limit=100" in req_url


# ---------------------------------------------------------------------------
# buscar_profissionais
# ---------------------------------------------------------------------------


class TestBuscarProfissionais:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_professionals(self) -> None:
        respx.get(PROFISSIONAIS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "codigo_cnes": "1234567",
                        "nome": "João Silva",
                        "cns": "123456789012345",
                        "cbo": "225125",
                        "descricao_cbo": "Médico generalista",
                    }
                ],
            )
        )
        result = await client.buscar_profissionais(cnes="1234567")
        assert len(result) == 1
        assert result[0].nome == "João Silva"
        assert result[0].cbo == "225125"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(PROFISSIONAIS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.buscar_profissionais()
        assert result == []

    @pytest.mark.asyncio
    @respx.mock
    async def test_sends_query_params(self) -> None:
        route = respx.get(PROFISSIONAIS_URL).mock(return_value=httpx.Response(200, json=[]))
        await client.buscar_profissionais(
            codigo_municipio="355030", cnes="1234567", limit=10, offset=5
        )
        req_url = str(route.calls[0].request.url)
        assert "codigo_municipio=355030" in req_url
        assert "cnes=1234567" in req_url
        assert "limit=10" in req_url
        assert "offset=5" in req_url


# ---------------------------------------------------------------------------
# listar_tipos_estabelecimento
# ---------------------------------------------------------------------------


class TestListarTiposEstabelecimento:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_types(self) -> None:
        respx.get(TIPOS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "codigo_tipo_estabelecimento": "01",
                        "descricao_tipo_estabelecimento": "Central de Regulação",
                    },
                    {
                        "codigo_tipo_estabelecimento": "02",
                        "descricao_tipo_estabelecimento": "Hospital Geral",
                    },
                ],
            )
        )
        result = await client.listar_tipos_estabelecimento()
        assert len(result) == 2
        assert result[0].codigo == "01"
        assert result[0].descricao == "Central de Regulação"
        assert result[1].codigo == "02"

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(TIPOS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.listar_tipos_estabelecimento()
        assert result == []


# ---------------------------------------------------------------------------
# consultar_leitos
# ---------------------------------------------------------------------------


class TestConsultarLeitos:
    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_parsed_beds(self) -> None:
        respx.get(LEITOS_URL).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "codigo_cnes": "1234567",
                        "tipo_leito": "Cirúrgico",
                        "especialidade": "Cirurgia Geral",
                        "existente": 20,
                        "sus": 15,
                    }
                ],
            )
        )
        result = await client.consultar_leitos(cnes="1234567")
        assert len(result) == 1
        assert result[0].tipo_leito == "Cirúrgico"
        assert result[0].existente == 20
        assert result[0].sus == 15

    @pytest.mark.asyncio
    @respx.mock
    async def test_empty_response(self) -> None:
        respx.get(LEITOS_URL).mock(return_value=httpx.Response(200, json=[]))
        result = await client.consultar_leitos()
        assert result == []

    @pytest.mark.asyncio
    @respx.mock
    async def test_sends_query_params(self) -> None:
        route = respx.get(LEITOS_URL).mock(return_value=httpx.Response(200, json=[]))
        await client.consultar_leitos(
            codigo_municipio="355030", cnes="1234567", limit=50, offset=10
        )
        req_url = str(route.calls[0].request.url)
        assert "codigo_municipio=355030" in req_url
        assert "cnes=1234567" in req_url
        assert "limit=50" in req_url
        assert "offset=10" in req_url


# ---------------------------------------------------------------------------
# Parse functions
# ---------------------------------------------------------------------------


class TestParseEstabelecimento:
    def test_handles_missing_fields(self) -> None:
        result = client._parse_estabelecimento({})
        assert result.codigo_cnes == ""
        assert result.nome_fantasia is None

    def test_converts_numeric_codes_to_str(self) -> None:
        result = client._parse_estabelecimento(
            {"codigo_cnes": 1234567, "codigo_municipio": 355030, "codigo_uf": 35}
        )
        assert result.codigo_cnes == "1234567"
        assert result.codigo_municipio == "355030"
        assert result.codigo_uf == "35"


class TestParseProfissional:
    def test_handles_missing_fields(self) -> None:
        result = client._parse_profissional({})
        assert result.codigo_cnes == ""
        assert result.nome is None


class TestParseTipo:
    def test_handles_missing_fields(self) -> None:
        result = client._parse_tipo({})
        assert result.codigo == ""
        assert result.descricao is None


class TestParseLeito:
    def test_handles_missing_fields(self) -> None:
        result = client._parse_leito({})
        assert result.codigo_cnes == ""
        assert result.existente is None
        assert result.sus is None
