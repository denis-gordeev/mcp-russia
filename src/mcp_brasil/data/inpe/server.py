"""INPE feature server (legacy) — registers tools, resources, and prompts.

Brazilian National Institute for Space Research API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import monitoramento_ambiental
from .resources import biomas_brasileiros, estados_amazonia_legal
from .tools import alertas_deter, buscar_focos_queimadas, consultar_desmatamento, dados_satelite

mcp = FastMCP("mcp-russia-inpe-legacy")

# Tools
mcp.tool(buscar_focos_queimadas, tags={"поиск", "пожары", "спутник", "окружающая-среда"})
mcp.tool(consultar_desmatamento, tags={"запрос", "вырубка-леса", "prodes", "окружающая-среда"})
mcp.tool(alertas_deter, tags={"запрос", "deter", "оповещения", "окружающая-среда"})
mcp.tool(dados_satelite, tags={"список", "спутники", "мониторинг"})

# Resources (URIs without namespace prefix — mount adds "inpe/" automatically)
mcp.resource("data://biomas", mime_type="application/json")(biomas_brasileiros)
mcp.resource("data://amazonia-legal", mime_type="application/json")(estados_amazonia_legal)

# Prompts
mcp.prompt(monitoramento_ambiental)
