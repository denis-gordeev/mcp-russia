"""Diário Oficial feature server (legacy) — registers tools, resources, and prompts.

Brazilian Official Gazette API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import investigar_empresa
from .resources import capitais_cobertas
from .tools import buscar_cidades, buscar_diarios, buscar_trechos, listar_territorios

mcp = FastMCP("mcp-russia-diario-oficial-legacy")

# Tools
mcp.tool(buscar_diarios, tags={"поиск", "официальные-бюллетени", "публикации"})
mcp.tool(buscar_trechos, tags={"поиск", "фрагменты", "официальные-бюллетени"})
mcp.tool(buscar_cidades, tags={"поиск", "муниципалитеты", "охват"})
mcp.tool(listar_territorios, tags={"список", "муниципалитеты", "охват"})

# Resources
mcp.resource("data://capitais-cobertas", mime_type="application/json")(capitais_cobertas)

# Prompts
mcp.prompt(investigar_empresa)
