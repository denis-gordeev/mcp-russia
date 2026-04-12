"""⚠️ DEPRECATED — DataJud feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    Используйте модуль ``mcp_brasil.data.kad_arbitrazh`` (КАД — kad.arbitr.ru) для российских арбитражных дел.

Brazilian Judicial Data API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_processo, pesquisa_juridica
from .resources import classes_processuais, info_api, tribunais_disponiveis
from .tools import (
    buscar_processo_por_numero,
    buscar_processos,
    buscar_processos_avancado,
    buscar_processos_por_assunto,
    buscar_processos_por_classe,
    buscar_processos_por_orgao,
    consultar_movimentacoes,
)

mcp = FastMCP("mcp-russia-datajud-legacy (⚠️ DEPRECATED — use 'kad_arbitrazh' for Russian arbitration)")

# Tools (7)
mcp.tool(buscar_processos, tags={"поиск", "процессы", "судебный"})
mcp.tool(buscar_processo_por_numero, tags={"поиск", "процессы", "npu"})
mcp.tool(buscar_processos_por_classe, tags={"поиск", "процессы", "процессуальный-класс"})
mcp.tool(buscar_processos_por_assunto, tags={"поиск", "процессы", "тема"})
mcp.tool(buscar_processos_por_orgao, tags={"поиск", "процессы", "судебный-орган"})
mcp.tool(buscar_processos_avancado, tags={"поиск", "процессы", "судебный", "расширенный"})
mcp.tool(consultar_movimentacoes, tags={"запрос", "движение", "процессы"})

# Resources
mcp.resource("data://tribunais", mime_type="application/json")(tribunais_disponiveis)
mcp.resource("data://classes-processuais", mime_type="application/json")(classes_processuais)
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Prompts
mcp.prompt(analise_processo)
mcp.prompt(pesquisa_juridica)
