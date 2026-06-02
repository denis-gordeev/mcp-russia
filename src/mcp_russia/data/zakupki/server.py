"""Zakupki feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_zakupki, obzor_zakupok
from .resources import istochniki_dannyh, struktura_eis, zakonodatelstvo
from .tools import (
    info_postavshchika,
    info_zakazchika,
    info_zakupki,
    plany_zakupok,
    poisk_kontraktov,
    poisk_zakupok,
    sposoby_zakupok,
    statusy_zakupok,
)

mcp = FastMCP("mcp-russia-zakupki")

# Tools
mcp.tool(poisk_zakupok, tags={"закупки", "поиск"})
mcp.tool(info_zakupki, tags={"закупка", "подробности"})
mcp.tool(poisk_kontraktov, tags={"контракты", "поиск"})
mcp.tool(info_zakazchika, tags={"заказчик", "информация"})
mcp.tool(info_postavshchika, tags={"поставщик", "информация"})
mcp.tool(statusy_zakupok, tags={"статусы", "справочник"})
mcp.tool(sposoby_zakupok, tags={"способы", "справочник"})
mcp.tool(plany_zakupok, tags={"планы", "закупки"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_eis)

# Prompts
mcp.prompt(analiz_zakupki)
mcp.prompt(obzor_zakupok)
