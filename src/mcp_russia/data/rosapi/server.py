"""Сервер модуля РосАПИ — регистрирует инструменты, ресурсы и промпты.

Модуль российских справочных данных: адреса, организации, банки, праздники.
Этот файл только регистрирует компоненты. Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_organizatsii, poisk_adresa_prompt
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

mcp = FastMCP(
    "mcp-russia-rosapi", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya
)

# Инструменты (8)
mcp.tool(konsul_adres_po_indeksu, tags={"адрес", "почтовый-индекс", "фиаc"})
mcp.tool(poisk_adresa, tags={"адрес", "поиск", "фиаc"})
mcp.tool(poisk_org_po_inn, tags={"организация", "инн", "егр юл"})
mcp.tool(poisk_org_po_ogrn, tags={"организация", "огрн", "егр юл"})
mcp.tool(spisok_bankov, tags={"банки", "справочник", "бик"})
mcp.tool(konsul_bank_po_bik, tags={"банк", "бик", "справочник"})
mcp.tool(prazdniki_rf, tags={"праздники", "календарь", "национальные"})
mcp.tool(nalogovye_stavki, tags={"налоги", "ставки", "фнс"})

# Ресурсы
mcp.resource("data://nalogovye-stavki", mime_type="application/json")(nalogovye_stavki_resurs)
mcp.resource("data://servisy", mime_type="application/json")(dostupnye_servisy)

# Промпты
mcp.prompt(analiz_organizatsii)
mcp.prompt(poisk_adresa_prompt)
