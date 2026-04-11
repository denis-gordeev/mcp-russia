"""Transparência feature server (legacy) — registers tools, resources, and prompts.

Brazilian Transparency API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_despesas, auditoria_fornecedor, verificacao_compliance
from .resources import bases_sancoes, categorias_beneficios, endpoints_disponiveis, info_api
from .tools import (
    buscar_acordos_leniencia,
    buscar_cartoes_pagamento,
    buscar_contratos,
    buscar_convenios,
    buscar_emendas,
    buscar_licitacoes,
    buscar_notas_fiscais,
    buscar_pep,
    buscar_sancoes,
    buscar_servidores,
    consultar_beneficio_social,
    consultar_bolsa_familia,
    consultar_cnpj,
    consultar_cpf,
    consultar_despesas,
    consultar_viagens,
    detalhar_contrato,
    detalhar_servidor,
)

mcp = FastMCP("mcp-russia-transparencia-legacy")

# Tools
mcp.tool(buscar_contratos, tags={"поиск", "контракты", "поставщики"})
mcp.tool(consultar_despesas, tags={"запрос", "расходы", "бюджет"})
mcp.tool(buscar_servidores, tags={"поиск", "служащие", "госслужба"})
mcp.tool(buscar_licitacoes, tags={"поиск", "тендеры", "закупки"})
mcp.tool(consultar_bolsa_familia, tags={"запрос", "пособие-семье", "социальные-выплаты"})
mcp.tool(buscar_sancoes, tags={"поиск", "санкции", "комплаенс", "антикоррупция"})
mcp.tool(buscar_emendas, tags={"поиск", "поправки", "бюджет"})
mcp.tool(consultar_viagens, tags={"запрос", "поездки", "суточные"})
mcp.tool(buscar_convenios, tags={"поиск", "соглашения", "переводы"})
mcp.tool(buscar_cartoes_pagamento, tags={"поиск", "корпоративная-карта", "расходы"})
mcp.tool(buscar_pep, tags={"поиск", "pep", "комплаенс"})
mcp.tool(buscar_acordos_leniencia, tags={"поиск", "сговор", "антикоррупция"})
mcp.tool(buscar_notas_fiscais, tags={"поиск", "счета-фактуры", "расходы"})
mcp.tool(consultar_beneficio_social, tags={"запрос", "социальные-выплаты", "bpc"})
mcp.tool(consultar_cpf, tags={"запрос", "cpf", "физическое-лицо"})
mcp.tool(consultar_cnpj, tags={"запрос", "cnpj", "юридическое-лицо"})
mcp.tool(detalhar_contrato, tags={"подробности", "контракты"})
mcp.tool(detalhar_servidor, tags={"подробности", "служащие", "вознаграждение"})

# Resources (URIs without namespace prefix — mount adds "transparencia/" automatically)
mcp.resource("data://endpoints", mime_type="application/json")(endpoints_disponiveis)
mcp.resource("data://bases-sancoes", mime_type="application/json")(bases_sancoes)
mcp.resource("data://info-api", mime_type="application/json")(info_api)
mcp.resource("data://categorias-beneficios", mime_type="application/json")(categorias_beneficios)

# Prompts
mcp.prompt(auditoria_fornecedor)
mcp.prompt(analise_despesas)
mcp.prompt(verificacao_compliance)
