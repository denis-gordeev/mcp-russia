"""ФНС feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_nalogoplatelshchika, obzor_rezhimov_nalogooblozheniya
from .resources import istochniki_dannyh, sistema_nalogovyh_organov, zakonodatelstvo
from .tools import (
    info_ip,
    info_organizacii,
    nalogovye_nachisleniya,
    proverki_organizacii,
    spisok_kategoriy_nalogoplatelshchikov,
    spisok_nalogovyh_rezhimov,
    spisok_statusov_organizaciy,
    spisok_tipov_proverok,
    spisok_vidov_nalogov,
)

mcp = FastMCP("mcp-russia-fns")

mcp.tool(spisok_nalogovyh_rezhimov, tags={"режимы", "справочник"})
mcp.tool(spisok_vidov_nalogov, tags={"налоги", "справочник"})
mcp.tool(spisok_tipov_proverok, tags={"проверки", "справочник"})
mcp.tool(spisok_statusov_organizaciy, tags={"статус", "справочник"})
mcp.tool(spisok_kategoriy_nalogoplatelshchikov, tags={"категории", "справочник"})
mcp.tool(info_organizacii, tags={"егрюл", "информация"})
mcp.tool(info_ip, tags={"егрип", "информация"})
mcp.tool(proverki_organizacii, tags={"проверки", "поиск"})
mcp.tool(nalogovye_nachisleniya, tags={"начисления", "информация"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(sistema_nalogovyh_organov)

mcp.prompt(analiz_nalogoplatelshchika)
mcp.prompt(obzor_rezhimov_nalogooblozheniya)
