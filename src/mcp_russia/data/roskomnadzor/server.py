"""Roskomnadzor feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_narusheniya, obzor_reestrov
from .resources import (
    istochniki_dannyh,
    struktura_roskomnadzora,
    zakonodatelstvo,
)
from .tools import (
    info_licenzii,
    info_operatora_pd,
    poisk_narusheniy,
    poisk_smi,
    spisok_kategoriy_narusheniy,
    spisok_kategoriy_pd_operatorov,
    spisok_napravleniy,
    spisok_reestrov,
    spisok_tipov_licenziy,
    spisok_tipov_smi,
    zapisi_reestra,
)

mcp = FastMCP("mcp-russia-roskomnadzor")

# Tools
mcp.tool(spisok_napravleniy, tags={"направления", "справочник"})
mcp.tool(spisok_tipov_licenziy, tags={"лицензии", "справочник"})
mcp.tool(spisok_kategoriy_narusheniy, tags={"нарушения", "справочник"})
mcp.tool(spisok_reestrov, tags={"реестры", "справочник"})
mcp.tool(spisok_tipov_smi, tags={"сми", "справочник"})
mcp.tool(spisok_kategoriy_pd_operatorov, tags={"операторы-пд", "справочник"})
mcp.tool(info_licenzii, tags={"лицензия", "информация"})
mcp.tool(poisk_smi, tags={"сми", "поиск"})
mcp.tool(info_operatora_pd, tags={"оператор-пд", "информация"})
mcp.tool(poisk_narusheniy, tags={"нарушения", "поиск"})
mcp.tool(zapisi_reestra, tags={"реестр", "записи"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_roskomnadzora)

# Prompts
mcp.prompt(analiz_narusheniya)
mcp.prompt(obzor_reestrov)
