"""Сервер модуля Госдумы — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_deputata, obzor_zakonodatelstva
from .resources import istochniki_dannyh, struktura_dumy
from .tools import (
    golosovaniya,
    info_deputata,
    spisok_deputatov,
    spisok_fraktsii,
    spisok_komitetov,
    spisok_sozyvov,
    zakonoproekty,
)

mcp = FastMCP(
    "mcp-russia-gosduma", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya
)

# Инструменты
mcp.tool(spisok_deputatov, tags={"депутаты", "справочник"})
mcp.tool(info_deputata, tags={"депутат", "информация"})
mcp.tool(spisok_fraktsii, tags={"фракции", "справочник"})
mcp.tool(spisok_komitetov, tags={"комитеты", "справочник"})
mcp.tool(spisok_sozyvov, tags={"созывы", "справочник"})
mcp.tool(zakonoproekty, tags={"законопроекты", "активность"})
mcp.tool(golosovaniya, tags={"голосования", "активность"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_dumy)

# Промпты
mcp.prompt(analiz_deputata)
mcp.prompt(obzor_zakonodatelstva)
