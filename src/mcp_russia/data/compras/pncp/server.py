"""PNCP sub-server (legacy) — registers PNCP tools, resources, and prompts.

Brazilian National Public Procurement Portal compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import investigar_fornecedor
from .resources import modalidades_licitacao
from .tools import (
    buscar_atas,
    buscar_contratacoes,
    buscar_contratos,
    consultar_fornecedor,
    consultar_orgao,
)

mcp = FastMCP("mcp-russia-pncp-legacy")

# Tools (buscar_itens removed — endpoint /v1/itens returns 404)
mcp.tool(buscar_contratacoes, tags={"поиск", "контракты", "тендеры"})
mcp.tool(buscar_contratos, tags={"поиск", "контракты", "закупки"})
mcp.tool(buscar_atas, tags={"поиск", "протоколы", "регистрация-цен"})
mcp.tool(consultar_fornecedor, tags={"запрос", "поставщики", "закупки"})
mcp.tool(consultar_orgao, tags={"запрос", "органы", "закупки"})

# Resources
mcp.resource("data://modalidades", mime_type="application/json")(modalidades_licitacao)

# Prompts
mcp.prompt(investigar_fornecedor)
