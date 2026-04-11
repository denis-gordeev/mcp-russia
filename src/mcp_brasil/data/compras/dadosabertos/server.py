"""Dados Abertos sub-server (legacy) — registers Compras.gov.br tools.

Brazilian Open Procurement Data compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .tools import (
    buscar_contratos,
    buscar_dispensas,
    buscar_licitacoes,
    buscar_material_catmat,
    buscar_pregoes,
    buscar_servico_catser,
    buscar_uasg,
    consultar_fornecedor,
)

mcp = FastMCP("mcp-russia-dadosabertos-legacy")

# Tools
mcp.tool(buscar_licitacoes, tags={"поиск", "тендеры", "закупки"})
mcp.tool(buscar_pregoes, tags={"поиск", "аукционы", "закупки"})
mcp.tool(buscar_dispensas, tags={"поиск", "освобождения", "закупки"})
mcp.tool(buscar_contratos, tags={"поиск", "контракты", "закупки"})
mcp.tool(consultar_fornecedor, tags={"запрос", "поставщики", "закупки"})
mcp.tool(buscar_material_catmat, tags={"поиск", "catmat", "материалы"})
mcp.tool(buscar_servico_catser, tags={"поиск", "catser", "услуги"})
mcp.tool(buscar_uasg, tags={"поиск", "uasg", "органы"})
