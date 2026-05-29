"""⚠️ DEPRECATED — Saude feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_russia.data.minzdrav`` (Минздрав РФ) для российских медицинских данных.

Brazilian Health Network API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_rede_saude
from .resources import codigos_uf_cnes
from .tools import (
    buscar_estabelecimentos,
    buscar_profissionais,
    consultar_leitos,
    listar_tipos_estabelecimento,
)

mcp = FastMCP("mcp-russia-saude-legacy (⚠️ DEPRECATED — use 'minzdrav' for Russian healthcare)")

# Tools (4)
mcp.tool(buscar_estabelecimentos, tags={"поиск", "учреждения", "cnes", "sus"})
mcp.tool(buscar_profissionais, tags={"поиск", "специалисты", "cnes"})
mcp.tool(listar_tipos_estabelecimento, tags={"список", "учреждения", "типы"})
mcp.tool(consultar_leitos, tags={"запрос", "койки", "больничные"})

# Resources (URIs without namespace prefix — mount adds "saude/" automatically)
mcp.resource("data://codigos-uf", mime_type="application/json")(codigos_uf_cnes)

# Prompts
mcp.prompt(analise_rede_saude)
