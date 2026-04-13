"""⚠️ DEPRECATED — TSE feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.cekrf`` (ЦИК РФ) для российских избирательных данных.

Brazilian Superior Electoral Court API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_candidato, comparativo_eleicao
from .resources import cargos_eleitorais, info_api
from .tools import (
    anos_eleitorais,
    apuracao_status,
    buscar_candidato,
    consultar_prestacao_contas,
    listar_candidatos,
    listar_cargos,
    listar_eleicoes,
    listar_eleicoes_suplementares,
    listar_estados_suplementares,
    listar_municipios_eleitorais,
    mapa_resultado_estados,
    resultado_eleicao,
    resultado_nacional,
    resultado_por_estado,
    resultado_por_municipio,
)

mcp = FastMCP("mcp-russia-tse-legacy (⚠️ DEPRECATED — use 'cekrf' for Russian elections)")

# Tools — DivulgaCandContas (9)
mcp.tool(anos_eleitorais, tags={"список", "выборы"})
mcp.tool(listar_eleicoes, tags={"список", "выборы"})
mcp.tool(listar_eleicoes_suplementares, tags={"список", "выборы", "дополнительные"})
mcp.tool(listar_estados_suplementares, tags={"список", "выборы", "дополнительные"})
mcp.tool(listar_cargos, tags={"список", "должности", "выборы"})
mcp.tool(listar_candidatos, tags={"список", "кандидаты", "выборы"})
mcp.tool(buscar_candidato, tags={"подробности", "кандидаты", "выборы"})
mcp.tool(resultado_eleicao, tags={"запрос", "результаты", "голоса"})
mcp.tool(consultar_prestacao_contas, tags={"запрос", "отчётность", "кампания"})

# Tools — CDN результатов (6)
mcp.tool(resultado_nacional, tags={"запрос", "результаты", "голоса", "национальный"})
mcp.tool(resultado_por_estado, tags={"запрос", "результаты", "голоса", "штаты"})
mcp.tool(resultado_por_municipio, tags={"запрос", "результаты", "голоса", "муниципалитеты"})
mcp.tool(mapa_resultado_estados, tags={"запрос", "результаты", "electoral-map"})
mcp.tool(apuracao_status, tags={"запрос", "подсчет", "выборы"})
mcp.tool(listar_municipios_eleitorais, tags={"список", "муниципалитеты", "выборы"})

# Resources
mcp.resource("data://cargos-eleitorais", mime_type="application/json")(cargos_eleitorais)
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Prompts
mcp.prompt(analise_candidato)
mcp.prompt(comparativo_eleicao)
