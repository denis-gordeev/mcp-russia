"""Senado feature server (legacy) — registers tools, resources, and prompts.

.. deprecated::
    This server provides Brazilian Senate data for backward compatibility only.
    For Russian Federation Council data, use the ``gosduma`` module.

Brazilian Senate API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import acompanhar_materia, analise_votacao_senado, perfil_senador
from .resources import comissoes_permanentes, info_api, tipos_materia
from .tools import (
    agenda_comissoes,
    agenda_plenario,
    buscar_materia,
    buscar_senador,
    buscar_senador_por_nome,
    consultar_tramitacao_materia,
    detalhe_comissao,
    detalhe_materia,
    detalhe_votacao,
    emendas_materia,
    legislatura_atual,
    listar_blocos,
    listar_comissoes,
    listar_liderancas,
    listar_senadores,
    listar_votacoes,
    membros_comissao,
    partidos_senado,
    relatorias_senador,
    reunioes_comissao,
    textos_materia,
    ufs_senado,
    votacoes_recentes,
    votacoes_senador,
    votos_materia,
)
from .tools import (
    tipos_materia as tipos_materia_tool,
)

mcp = FastMCP("mcp-russia-senado-legacy (⚠️ DEPRECATED — use 'gosduma' for Russian Parliament)")

# Tools — Сенаторы (4)
mcp.tool(listar_senadores, tags={"список", "сенаторы", "парламентарии"})
mcp.tool(buscar_senador, tags={"подробности", "сенаторы", "парламентарии"})
mcp.tool(buscar_senador_por_nome, tags={"поиск", "сенаторы", "парламентарии"})
mcp.tool(votacoes_senador, tags={"запрос", "сенаторы", "голосования"})

# Tools — Материалы (5)
mcp.tool(buscar_materia, tags={"поиск", "материалы", "законодательство"})
mcp.tool(detalhe_materia, tags={"подробности", "материалы", "законодательство"})
mcp.tool(consultar_tramitacao_materia, tags={"запрос", "движение", "материалы"})
mcp.tool(textos_materia, tags={"запрос", "документы", "материалы"})
mcp.tool(votos_materia, tags={"запрос", "голосования", "материалы"})

# Tools — Голосования (3)
mcp.tool(listar_votacoes, tags={"список", "голосования", "пленум"})
mcp.tool(detalhe_votacao, tags={"подробности", "голосования", "пленум"})
mcp.tool(votacoes_recentes, tags={"список", "голосования", "пленум"})

# Tools — Комиссии (4)
mcp.tool(listar_comissoes, tags={"список", "комиссии"})
mcp.tool(detalhe_comissao, tags={"подробности", "комиссии"})
mcp.tool(membros_comissao, tags={"запрос", "комиссии", "парламентарии"})
mcp.tool(reunioes_comissao, tags={"запрос", "комиссии", "повестка"})

# Tools — Повестка (2)
mcp.tool(agenda_plenario, tags={"запрос", "повестка", "пленум"})
mcp.tool(agenda_comissoes, tags={"запрос", "повестка", "комиссии"})

# Tools — Вспомогательные (4)
mcp.tool(legislatura_atual, tags={"запрос", "легислатура"})
mcp.tool(tipos_materia_tool, tags={"список", "материалы", "типы"})
mcp.tool(partidos_senado, tags={"список", "партии", "парламентарии"})
mcp.tool(ufs_senado, tags={"список", "штаты", "парламентарии"})

# Tools — Открытые данные (4)
mcp.tool(emendas_materia, tags={"запрос", "поправки", "материалы"})
mcp.tool(listar_blocos, tags={"список", "блоки", "коалиции"})
mcp.tool(listar_liderancas, tags={"список", "руководство", "парламентарии"})
mcp.tool(relatorias_senador, tags={"запрос", "докладчики", "сенаторы"})

# Resources (URIs without namespace prefix — mount adds "senado/" automatically)
mcp.resource("data://tipos-materia", mime_type="application/json")(tipos_materia)
mcp.resource("data://info-api", mime_type="application/json")(info_api)
mcp.resource("data://comissoes-permanentes", mime_type="application/json")(comissoes_permanentes)

# Prompts
mcp.prompt(acompanhar_materia)
mcp.prompt(perfil_senador)
mcp.prompt(analise_votacao_senado)
