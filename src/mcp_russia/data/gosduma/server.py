"""Gosduma feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_deputata, obzor_zakonodatelstva
from .resources import istochniki_dannyh, struktura_dumy
from .tools import (
    golosovaniya,
    info_deputata,
    spisok_deputatov,
    spisok_frakcii,
    spisok_komitetov,
    spisok_sozyvov,
    zakonoproekty,
)

mcp = FastMCP("mcp-russia-gosduma")

# Tools
mcp.tool(spisok_deputatov, tags={"депутаты", "справочник"})
mcp.tool(info_deputata, tags={"депутат", "информация"})
mcp.tool(spisok_frakcii, tags={"фракции", "справочник"})
mcp.tool(spisok_komitetov, tags={"комитеты", "справочник"})
mcp.tool(spisok_sozyvov, tags={"созывы", "справочник"})
mcp.tool(zakonoproekty, tags={"законопроекты", "активность"})
mcp.tool(golosovaniya, tags={"голосования", "активность"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_dumy)

# Prompts
mcp.prompt(analiz_deputata)
mcp.prompt(obzor_zakonodatelstva)
