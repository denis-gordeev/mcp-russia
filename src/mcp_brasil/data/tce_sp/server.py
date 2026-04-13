"""⚠️ DEPRECATED — TCE-SP feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и ``mcp_brasil.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Sao Paulo) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analisar_financas_municipio_sp
from .resources import endpoints_tce_sp
from .tools import consultar_despesas_sp, consultar_receitas_sp, listar_municipios_sp

mcp = FastMCP("mcp-russia-tce-sp-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(listar_municipios_sp)
mcp.tool(consultar_despesas_sp)
mcp.tool(consultar_receitas_sp)

# Resources
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_sp)

# Prompts
mcp.prompt(analisar_financas_municipio_sp)
