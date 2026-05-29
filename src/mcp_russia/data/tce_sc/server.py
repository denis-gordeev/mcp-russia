"""⚠️ DEPRECATED — TCE-SC feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_russia.data.rosstat`` (Росстат) и ``mcp_russia.data.zakupki`` (ЕИС)
    для российских статистических данных и госзакупок.

Brazilian State Court of Accounts (Santa Catarina) API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import consultar_unidades_sc
from .resources import endpoints_tce_sc
from .tools import listar_municipios_sc, listar_unidades_gestoras_sc

mcp = FastMCP("mcp-russia-tce-sc-legacy (⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)")

# Tools
mcp.tool(listar_municipios_sc)
mcp.tool(listar_unidades_gestoras_sc)

# Resources (URIs without namespace — mount adds "tce_sc/" automatically)
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_tce_sc)

# Prompts
mcp.prompt(consultar_unidades_sc)
