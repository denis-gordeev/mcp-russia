"""⚠️ DEPRECATED — TCE-TO feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Tocantins) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_pessoa_to
from .resources import endpoints_tce_to
from .tools import buscar_pessoas_to, consultar_processo_to, listar_pautas_to

mcp = FastMCP("mcp-russia-tce-to-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(buscar_pessoas_to)
mcp.tool(consultar_processo_to)
mcp.tool(listar_pautas_to)

# Resources
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_to)

# Prompts
mcp.prompt(analisar_pessoa_to)
