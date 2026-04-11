"""Jurisprudencia feature server (legacy) — registers tools, resources, and prompts.

Brazilian Case Law API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_tema, pesquisa_jurisprudencial
from .resources import info_api, operadores_busca, tribunais_superiores
from .tools import (
    buscar_informativos,
    buscar_jurisprudencia_stf,
    buscar_jurisprudencia_stj,
    buscar_jurisprudencia_tst,
    buscar_repercussao_geral,
    buscar_sumulas,
)

mcp = FastMCP("mcp-russia-jurisprudencia-legacy")

# Tools (6)
mcp.tool(buscar_jurisprudencia_stf, tags={"поиск", "судебная-практика", "stf"})
mcp.tool(buscar_jurisprudencia_stj, tags={"поиск", "судебная-практика", "stj"})
mcp.tool(buscar_jurisprudencia_tst, tags={"поиск", "судебная-практика", "tst", "трудовой"})
mcp.tool(buscar_sumulas, tags={"поиск", "тезаурусы", "stf"})
mcp.tool(buscar_repercussao_geral, tags={"поиск", "общее-воздействие", "stf"})
mcp.tool(buscar_informativos, tags={"поиск", "информационные-бюллетени", "судебная-практика"})

# Resources
mcp.resource("data://tribunais-superiores", mime_type="application/json")(tribunais_superiores)
mcp.resource("data://operadores-busca", mime_type="application/json")(operadores_busca)
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Prompts
mcp.prompt(pesquisa_jurisprudencial)
mcp.prompt(analise_tema)
