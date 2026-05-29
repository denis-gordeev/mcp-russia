"""⚠️ DEPRECATED — TransfereGov feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_russia.data.gosduma`` (Госдума) и будущий модуль Минфина РФ
    для российских бюджетных данных.

Brazilian Transfer Government API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_emendas_pix
from .resources import info_api
from .tools import (
    buscar_emenda_por_autor,
    buscar_emendas_pix,
    detalhe_emenda,
    emendas_por_municipio,
    resumo_emendas_ano,
)

mcp = FastMCP(
    "mcp-russia-transferegov-legacy (⚠️ DEPRECATED — use 'gosduma' for Russian parliament)"
)

# Tools
mcp.tool(buscar_emendas_pix, tags={"поиск", "emendas-pix", "переводы"})
mcp.tool(buscar_emenda_por_autor, tags={"поиск", "emendas-pix", "парламентарии"})
mcp.tool(detalhe_emenda, tags={"подробности", "emendas-pix", "переводы"})
mcp.tool(emendas_por_municipio, tags={"поиск", "emendas-pix", "муниципалитеты"})
mcp.tool(resumo_emendas_ano, tags={"список", "emendas-pix", "бюджет"})

# Resources
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Prompts
mcp.prompt(analise_emendas_pix)
