"""Сервер модуля Совета Федерации РФ — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_senatora, obzor_zakonodatelstva
from .resources import istochniki_dannyh, reglament, struktura_sovfeda
from .tools import (
    info_senatora,
    poisk_zakonoproektov,
    spisok_komissiy,
    spisok_komitetov,
    spisok_senatorov,
    spisok_zasedaniy,
)

mcp = FastMCP("mcp-russia-sovfed")

# Инструменты
mcp.tool(spisok_senatorov, tags={"сенаторы", "справочник"})
mcp.tool(info_senatora, tags={"сенатор", "информация"})
mcp.tool(spisok_komitetov, tags={"комитеты", "справочник"})
mcp.tool(spisok_komissiy, tags={"комиссии", "справочник"})
mcp.tool(poisk_zakonoproektov, tags={"законопроекты", "поиск"})
mcp.tool(spisok_zasedaniy, tags={"заседания", "справочник"})

# Ресурсы
mcp.resource("data://istochniki-sovfeda", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura-sovfeda", mime_type="text/plain")(struktura_sovfeda)
mcp.resource("data://reglament-sovfeda", mime_type="text/plain")(reglament)

# Промпты
mcp.prompt(analiz_senatora)
mcp.prompt(obzor_zakonodatelstva)
