"""Сервер модуля Роспотребнадзора — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_proverki, obzor_sanitarnoy_situacii
from .resources import (
    istochniki_dannyh,
    struktura_rospotrebnadzora,
    zakonodatelstvo,
)
from .tools import (
    info_proverki,
    plan_proverok,
    poisk_narusheniy,
    poisk_proverok,
    pokazateli_bezopasnosti,
    spisok_kategoriy_obiektov,
    spisok_napravleniy,
    spisok_regionalnyh_upravleniy,
    spisok_sanpinov,
    spisok_tipov_proverok,
    zhaloby_potrebiteley,
)

mcp = FastMCP("mcp-russia-rospotrebnadzor")

# Tools
mcp.tool(spisok_napravleniy, tags={"направления", "справочник"})
mcp.tool(spisok_tipov_proverok, tags={"типы-проверок", "справочник"})
mcp.tool(spisok_kategoriy_obiektov, tags={"категории-объектов", "справочник"})
mcp.tool(spisok_regionalnyh_upravleniy, tags={"региональные-управления", "справочник"})
mcp.tool(info_proverki, tags={"проверка", "информация"})
mcp.tool(poisk_proverok, tags={"проверки", "поиск"})
mcp.tool(plan_proverok, tags={"план-проверок", "информация"})
mcp.tool(poisk_narusheniy, tags={"нарушения", "поиск"})
mcp.tool(spisok_sanpinov, tags={"санпин", "справочник"})
mcp.tool(zhaloby_potrebiteley, tags={"жалобы", "потребители"})
mcp.tool(pokazateli_bezopasnosti, tags={"показатели", "безопасность"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_rospotrebnadzora)

# Prompts
mcp.prompt(analiz_proverki)
mcp.prompt(obzor_sanitarnoy_situacii)
