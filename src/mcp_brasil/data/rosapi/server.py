"""RosAPI feature server — registers tools, resources, and prompts.

Russian reference data module: addresses, organizations, banks, holidays.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_organizacii, poisk_adresa_prompt
from .resources import dostupnye_servisy, nalogovye_stavki_resurs
from .tools import (
    konsul_adres_po_indeksu,
    konsul_bank_po_bik,
    nalogovye_stavki,
    poisk_adresa,
    poisk_org_po_inn,
    poisk_org_po_ogrn,
    prazdniki_rf,
    spisok_bankov,
)

mcp = FastMCP("mcp-russia-rosapi")

# Tools (8)
mcp.tool(konsul_adres_po_indeksu, tags={"адрес", "почтовый-индекс", "фиаc"})
mcp.tool(poisk_adresa, tags={"адрес", "поиск", "фиаc"})
mcp.tool(poisk_org_po_inn, tags={"организация", "инн", "егр юл"})
mcp.tool(poisk_org_po_ogrn, tags={"организация", "огрн", "егр юл"})
mcp.tool(spisok_bankov, tags={"банки", "справочник", "бик"})
mcp.tool(konsul_bank_po_bik, tags={"банк", "бик", "справочник"})
mcp.tool(prazdniki_rf, tags={"праздники", "календарь", "национальные"})
mcp.tool(nalogovye_stavki, tags={"налоги", "ставки", "фнс"})

# Resources
mcp.resource("data://nalogovye-stavki", mime_type="application/json")(
    nalogovye_stavki_resurs
)
mcp.resource("data://servisy", mime_type="application/json")(dostupnye_servisy)

# Prompts
mcp.prompt(analiz_organizacii)
mcp.prompt(poisk_adresa_prompt)
