"""ANA feature server (legacy) — registers tools, resources, and prompts.

Brazilian National Water Agency API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_bacia
from .resources import tipos_estacao
from .tools import buscar_estacoes, consultar_telemetria, monitorar_reservatorios

mcp = FastMCP("mcp-russia-ana-legacy")

# Tools
mcp.tool(buscar_estacoes, tags={"поиск", "станции", "гидрология"})
mcp.tool(consultar_telemetria, tags={"запрос", "телеметрия", "уровень-воды", "расход"})
mcp.tool(monitorar_reservatorios, tags={"запрос", "водохранилища", "объем"})

# Resources (URIs without namespace prefix — mount adds "ana/" automatically)
mcp.resource("data://tipos-estacao", mime_type="application/json")(tipos_estacao)

# Prompts
mcp.prompt(analise_bacia)
