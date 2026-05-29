"""⚠️ DEPRECATED — TCE-PE feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Pernambuco) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_municipio_pe
from .resources import endpoints_tce_pe
from .tools import (
    buscar_contratos_pe,
    buscar_despesas_pe,
    buscar_fornecedores_pe,
    buscar_licitacoes_pe,
    buscar_unidades_pe,
)

mcp = FastMCP("mcp-russia-tce-pe-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(buscar_unidades_pe)
mcp.tool(buscar_licitacoes_pe)
mcp.tool(buscar_contratos_pe)
mcp.tool(buscar_despesas_pe)
mcp.tool(buscar_fornecedores_pe)

# Resources
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_pe)

# Prompts
mcp.prompt(analisar_municipio_pe)
