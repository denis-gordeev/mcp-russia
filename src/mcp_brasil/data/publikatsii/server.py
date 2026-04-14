"""Publikatsii feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_normativnogo_akta, obzor_zakonodatelstva
from .resources import (
    istochniki_dannyh,
    poryadok_opublikovaniya,
    struktura_zakonodatelstva,
)
from .tools import (
    info_normativnogo_akta,
    info_zakonproekta,
    izmeneniya_akta,
    poisk_aktov,
    publikatsii_po_datam,
    spisok_istochnikov,
    spisok_otrasley,
    spisok_statusov,
    spisok_tipov_aktov,
)

mcp = FastMCP("mcp-russia-publikatsii")

# Tools
mcp.tool(spisok_tipov_aktov, tags={"типы-актов", "справочник"})
mcp.tool(spisok_otrasley, tags={"отрасли", "справочник"})
mcp.tool(spisok_istochnikov, tags={"источники", "справочник"})
mcp.tool(spisok_statusov, tags={"статусы", "справочник"})
mcp.tool(info_normativnogo_akta, tags={"нормативный-акт", "информация"})
mcp.tool(info_zakonproekta, tags={"законопроект", "информация"})
mcp.tool(poisk_aktov, tags={"поиск", "акты"})
mcp.tool(publikatsii_po_datam, tags={"публикации", "период"})
mcp.tool(izmeneniya_akta, tags={"изменения", "акт"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://poryadok-opublikovaniya", mime_type="text/plain")(poryadok_opublikovaniya)
mcp.resource("data://struktura-zakonodatelstva", mime_type="text/plain")(struktura_zakonodatelstva)

# Prompts
mcp.prompt(analiz_normativnogo_akta)
mcp.prompt(obzor_zakonodatelstva)
