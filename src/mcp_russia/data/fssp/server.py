"""Сервер модуля ФССП — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_dolzhnika, obzor_ispolnitelnogo_proizvodstva
from .resources import istochniki_dannyh, struktura_fssp, zakonodatelstvo
from .tools import (
    info_proizvodstva,
    ogranicheniya_dolzhnika,
    poisk_dolzhnika,
    rozysk_dolzhnika,
    spisok_kategoriy_dolzhnikov,
    spisok_ogranicheniy,
    spisok_osnovaniy_vozbuzhdeniya,
    spisok_statusov_proizvodstva,
    spisok_vidov_proizvodstv,
)

mcp = FastMCP("mcp-russia-fssp")

mcp.tool(spisok_vidov_proizvodstv, tags={"виды", "справочник"})
mcp.tool(spisok_statusov_proizvodstva, tags={"статус", "справочник"})
mcp.tool(spisok_ogranicheniy, tags={"ограничения", "справочник"})
mcp.tool(spisok_kategoriy_dolzhnikov, tags={"категории", "справочник"})
mcp.tool(spisok_osnovaniy_vozbuzhdeniya, tags={"основания", "справочник"})
mcp.tool(info_proizvodstva, tags={"производство", "информация"})
mcp.tool(poisk_dolzhnika, tags={"должник", "поиск"})
mcp.tool(ogranicheniya_dolzhnika, tags={"ограничения", "информация"})
mcp.tool(rozysk_dolzhnika, tags={"розыск", "поиск"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_fssp)

mcp.prompt(analiz_dolzhnika)
mcp.prompt(obzor_ispolnitelnogo_proizvodstva)
