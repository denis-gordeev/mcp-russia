"""Rosstat feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_regiona, obzor_inflyacii
from .resources import istochniki_dannyh, metodologiya
from .tools import (
    demografiya,
    indikator_dannye,
    inflyaciya,
    okrug_info,
    pokazateli_rosstata,
    region_info,
    spisok_okrugov,
    spisok_regionov,
    sravnenie_regionov,
    vrp_dannye,
    zarplata_dannye,
)

mcp = FastMCP("mcp-russia-rosstat")

# Tools
mcp.tool(spisok_regionov, tags={"регионы", "справочник"})
mcp.tool(spisok_okrugov, tags={"федеральные-округа", "справочник"})
mcp.tool(region_info, tags={"регион", "информация"})
mcp.tool(okrug_info, tags={"федеральный-округ", "информация"})
mcp.tool(pokazateli_rosstata, tags={"показатели", "справочник"})
mcp.tool(inflyaciya, tags={"инфляция", "ИПЦ"})
mcp.tool(demografiya, tags={"демография", "население"})
mcp.tool(vrp_dannye, tags={"ВРП", "экономика"})
mcp.tool(zarplata_dannye, tags={"зарплата", "экономика"})
mcp.tool(sravnenie_regionov, tags={"сравнение", "регионы"})
mcp.tool(indikator_dannye, tags={"показатель", "ЕМИСС", "универсальный"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://metodologiya", mime_type="text/plain")(metodologiya)

# Prompts
mcp.prompt(analiz_regiona)
mcp.prompt(obzor_inflyacii)
