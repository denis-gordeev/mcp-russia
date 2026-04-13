"""⚠️ DEPRECATED — TCE-PI feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Piaui) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_municipio_pi
from .resources import endpoints_tce_pi
from .tools import (
    buscar_prefeitura_pi,
    consultar_despesas_pi,
    consultar_receitas_pi,
    listar_orgaos_pi,
    listar_prefeituras_pi,
)

mcp = FastMCP("mcp-russia-tce-pi-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(listar_prefeituras_pi)
mcp.tool(buscar_prefeitura_pi)
mcp.tool(consultar_despesas_pi)
mcp.tool(consultar_receitas_pi)
mcp.tool(listar_orgaos_pi)

# Resources
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_pi)

# Prompts
mcp.prompt(analisar_municipio_pi)
