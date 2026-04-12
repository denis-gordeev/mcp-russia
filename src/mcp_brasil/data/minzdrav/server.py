"""MinZdrav feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_zdorovya_regiona, obzor_med_organizatsiy
from .resources import federalnyye_okruga, istochniki_dannyh, klassifikatsii
from .tools import (
    info_med_organizatsii,
    poisk_med_organizatsiy,
    pokazateli_zdorovya,
    spravochnik_mkb10,
    spravochnik_mo,
    spravochnik_spetsialnostey,
    statistika_zabolevaniy,
)

mcp = FastMCP("mcp-russia-minzdrav")

# Tools
mcp.tool(poisk_med_organizatsiy, tags={"медицинские-организации", "поиск"})
mcp.tool(info_med_organizatsii, tags={"медицинская-организация", "информация"})
mcp.tool(pokazateli_zdorovya, tags={"здоровье", "показатели"})
mcp.tool(statistika_zabolevaniy, tags={"заболеваемость", "статистика"})
mcp.tool(spravochnik_mo, tags={"типы-мо", "справочник"})
mcp.tool(spravochnik_spetsialnostey, tags={"специальности", "справочник"})
mcp.tool(spravochnik_mkb10, tags={"мкб-10", "справочник"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://klassifikatsii", mime_type="text/plain")(klassifikatsii)
mcp.resource("data://okruga", mime_type="text/plain")(federalnyye_okruga)

# Prompts
mcp.prompt(analiz_zdorovya_regiona)
mcp.prompt(obzor_med_organizatsiy)
