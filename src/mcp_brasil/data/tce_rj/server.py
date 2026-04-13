"""⚠️ DEPRECATED — TCE-RJ feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Rio de Janeiro) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_municipio_rj
from .resources import endpoints_disponiveis
from .tools import (
    buscar_compras_diretas,
    buscar_concessoes,
    buscar_contratos_municipio,
    buscar_licitacoes,
    buscar_obras_paralisadas,
    buscar_penalidades,
    buscar_prestacao_contas,
)

mcp = FastMCP("mcp-russia-tce-rj-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(buscar_licitacoes)
mcp.tool(buscar_contratos_municipio)
mcp.tool(buscar_compras_diretas)
mcp.tool(buscar_obras_paralisadas)
mcp.tool(buscar_penalidades)
mcp.tool(buscar_prestacao_contas)
mcp.tool(buscar_concessoes)

# Resources
mcp.resource("data://endpoints-disponiveis", mime_type="application/json")(endpoints_disponiveis)

# Prompts
mcp.prompt(analisar_municipio_rj)
