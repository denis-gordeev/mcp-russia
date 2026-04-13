"""⚠️ DEPRECATED — TCE-RS feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Rio Grande do Sul) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_municipio_rs
from .resources import endpoints_tce_rs
from .tools import (
    buscar_datasets_rs,
    buscar_gestao_fiscal_rs,
    buscar_indices_educacao_rs,
    buscar_indices_saude_rs,
    listar_municipios_rs,
)

mcp = FastMCP("mcp-russia-tce-rs-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(listar_municipios_rs)
mcp.tool(buscar_indices_educacao_rs)
mcp.tool(buscar_indices_saude_rs)
mcp.tool(buscar_gestao_fiscal_rs)
mcp.tool(buscar_datasets_rs)

# Resources (URIs without namespace — mount adds "tce_rs/" automatically)
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_rs)

# Prompts
mcp.prompt(analisar_municipio_rs)
