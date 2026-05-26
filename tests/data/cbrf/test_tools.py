"""Тесты инструментов модуля ЦБ РФ."""

from unittest.mock import AsyncMock, patch

from mcp_brasil.data.cbrf import tools as cbrf_tools
from mcp_brasil.data.cbrf.schemas import ValorMoeda


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


def _mock_moeda(
    codigo="USD",
    nome="Доллар США",
    nominal=1,
    valor=90.0,
    valor_anterior=89.0,
    data="2025-01-15",
):
    return ValorMoeda(
        codigo=codigo,
        nome=nome,
        nominal=nominal,
        valor=valor,
        valor_anterior=valor_anterior,
        data=data,
    )


async def test_cursos_atuais():
    ctx = _mock_ctx()
    moedas = [
        _mock_moeda("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_moeda("EUR", "Евро", 1, 98.0, 97.5),
    ]
    with patch.object(cbrf_tools.client, "buscar_moedas_principais", return_value=moedas):
        result = await cbrf_tools.cursos_atuais(ctx)
    assert "ЦБ РФ" in result
    assert "USD" in result
    assert "EUR" in result


async def test_cursos_atuais_empty():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "buscar_moedas_principais", return_value=[]):
        result = await cbrf_tools.cursos_atuais(ctx)
    assert "Не удалось" in result


async def test_consultar_moeda():
    ctx = _mock_ctx()
    moeda = _mock_moeda("USD", "Доллар США", 1, 90.0, 89.0)
    with patch.object(cbrf_tools.client, "buscar_moeda", return_value=moeda):
        result = await cbrf_tools.consultar_moeda("USD", ctx)
    assert "Доллар США" in result
    assert "USD" in result
    assert "90" in result


async def test_consultar_moeda_not_found():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "buscar_moeda", return_value=None):
        result = await cbrf_tools.consultar_moeda("XYZ", ctx)
    assert "не найдена" in result


async def test_listar_moedas():
    ctx = _mock_ctx()
    raw = {
        "Valute": {
            "USD": {"Name": "Доллар США", "Nominal": 1, "Value": 90.0},
            "EUR": {"Name": "Евро", "Nominal": 1, "Value": 98.0},
        }
    }
    with patch.object(cbrf_tools.client, "buscar_todas_moedas", return_value=raw):
        result = await cbrf_tools.listar_moedas(ctx)
    assert "2 валют" in result
    assert "USD" in result
    assert "EUR" in result


async def test_converter_moeda():
    ctx = _mock_ctx()
    moeda = _mock_moeda("USD", "Доллар США", 1, 90.0)
    with patch.object(cbrf_tools.client, "buscar_moeda", return_value=moeda):
        result = await cbrf_tools.converter_moeda("USD", 100, ctx)
    assert "9.000" in result or "9 000" in result or "9000" in result
    assert "Конвертация" in result


async def test_converter_moeda_not_found():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "buscar_moeda", return_value=None):
        result = await cbrf_tools.converter_moeda("XYZ", 100, ctx)
    assert "не найдена" in result


async def test_comparar_moedas():
    ctx = _mock_ctx()
    moedas = [
        _mock_moeda("USD", "Доллар США", 1, 90.0, 89.0),
        _mock_moeda("EUR", "Евро", 1, 98.0, 97.0),
    ]
    with patch.object(cbrf_tools.client, "buscar_moedas_varios", return_value=moedas):
        result = await cbrf_tools.comparar_moedas(["USD", "EUR"], ctx)
    assert "Сравнение" in result
    assert "USD" in result
    assert "EUR" in result


async def test_comparar_moedas_default():
    ctx = _mock_ctx()
    with patch.object(cbrf_tools.client, "buscar_moedas_varios", return_value=[]):
        result = await cbrf_tools.comparar_moedas(ctx=ctx)
    assert "Не удалось" in result


async def test_comparar_moedas_too_many():
    codes = [f"C{i}" for i in range(11)]
    result = await cbrf_tools.comparar_moedas(codes)
    assert "не более 10" in result


async def test_cursos_por_pais():
    ctx = _mock_ctx()
    moedas = [
        _mock_moeda("USD", "Доллар США", 1, 90.0),
        _mock_moeda("CNY", "Китайский юань", 1, 12.5),
    ]
    with patch.object(cbrf_tools.client, "buscar_moedas_varios", return_value=moedas):
        result = await cbrf_tools.cursos_por_pais(ctx)
    assert "стран" in result.lower() or "партнёр" in result.lower()
    assert "USD" in result
