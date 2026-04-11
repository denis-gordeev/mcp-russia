"""Dados Abertos feature server (legacy) — registers tools, resources, and prompts.

Brazilian Open Data API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import explorar_dados
from .resources import formatos_disponiveis
from .tools import buscar_conjuntos, buscar_recursos, detalhar_conjunto, listar_organizacoes

mcp = FastMCP("mcp-russia-dados-abertos-legacy")

# Tools
mcp.tool(buscar_conjuntos, tags={"поиск", "наборы-данных", "открытые-данные"})
mcp.tool(detalhar_conjunto, tags={"подробности", "наборы-данных", "открытые-данные"})
mcp.tool(listar_organizacoes, tags={"список", "организации", "открытые-данные"})
mcp.tool(buscar_recursos, tags={"поиск", "ресурсы", "загрузки"})

# Resources
mcp.resource("data://formatos", mime_type="application/json")(formatos_disponiveis)

# Prompts
mcp.prompt(explorar_dados)
