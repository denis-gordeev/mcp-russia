"""Câmara feature server (legacy) — registers tools, resources, and prompts.

Brazilian Chamber of Deputies API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import acompanhar_proposicao, analise_votacao, perfil_deputado
from .resources import info_api, legislaturas_recentes, tipos_proposicao
from .tools import (
    agenda_legislativa,
    buscar_comissoes,
    buscar_deputado,
    buscar_proposicao,
    buscar_votacao,
    consultar_tramitacao,
    despesas_deputado,
    detalhar_proposicao,
    frentes_parlamentares,
    listar_deputados,
    votos_nominais,
)

mcp = FastMCP("mcp-russia-camara-legacy")

# Tools (11)
mcp.tool(listar_deputados, tags={"список", "депутаты", "парламентарии"})
mcp.tool(buscar_deputado, tags={"подробности", "депутаты", "парламентарии"})
mcp.tool(buscar_proposicao, tags={"поиск", "предложения", "законодательство"})
mcp.tool(detalhar_proposicao, tags={"подробности", "предложения", "законодательство"})
mcp.tool(consultar_tramitacao, tags={"запрос", "движение", "предложения"})
mcp.tool(buscar_votacao, tags={"поиск", "голосования", "пленум"})
mcp.tool(votos_nominais, tags={"подробности", "голосования", "пленум"})
mcp.tool(despesas_deputado, tags={"запрос", "расходы", "парламентские-расходы"})
mcp.tool(agenda_legislativa, tags={"запрос", "повестка", "сессии"})
mcp.tool(buscar_comissoes, tags={"поиск", "комиссии", "комиссия-расследования"})
mcp.tool(frentes_parlamentares, tags={"список", "фронты", "парламентарии"})

# Resources (URIs without namespace prefix — mount adds "camara/" automatically)
mcp.resource("data://tipos-proposicao", mime_type="application/json")(tipos_proposicao)
mcp.resource("data://legislaturas", mime_type="application/json")(legislaturas_recentes)
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Prompts
mcp.prompt(acompanhar_proposicao)
mcp.prompt(perfil_deputado)
mcp.prompt(analise_votacao)
