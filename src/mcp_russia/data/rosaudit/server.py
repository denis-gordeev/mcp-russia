"""Rosaudit feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_auditorskogo_zaklyucheniya, obzor_ispolneniya_byudzheta
from .resources import (
    istochniki_dannyh,
    struktura_schetnoy_pality,
    zakonodatelstvo,
)
from .tools import (
    info_auditorskogo_zaklyucheniya,
    info_kontrolnogo_meropriyatiya,
    ispolnenie_byudzheta,
    poisk_kontrolnyh_meropriyatiy,
    poisk_narusheniy,
    spisok_napravleniy,
    spisok_subiektov_audita,
    spisok_tipov_meropriyatiy,
)

mcp = FastMCP("mcp-russia-rosaudit")

# Tools
mcp.tool(spisok_napravleniy, tags={"направления", "справочник"})
mcp.tool(spisok_tipov_meropriyatiy, tags={"типы-мероприятий", "справочник"})
mcp.tool(spisok_subiektov_audita, tags={"субъекты-аудита", "справочник"})
mcp.tool(poisk_kontrolnyh_meropriyatiy, tags={"контрольное-мероприятие", "поиск"})
mcp.tool(info_kontrolnogo_meropriyatiya, tags={"контрольное-мероприятие", "информация"})
mcp.tool(info_auditorskogo_zaklyucheniya, tags={"аудиторское-заключение", "информация"})
mcp.tool(ispolnenie_byudzheta, tags={"бюджет", "исполнение"})
mcp.tool(poisk_narusheniy, tags={"нарушения", "поиск"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_schetnoy_pality)

# Prompts
mcp.prompt(analiz_auditorskogo_zaklyucheniya)
mcp.prompt(obzor_ispolneniya_byudzheta)
