"""Сервер модуля Федерального казначейства — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_ispolneniya_byudzheta, obzor_byudzhetnoy_sistemy
from .resources import byudzhetnaya_sistema, istochniki_dannyh, struktura_kaznacheistva
from .tools import (
    ispolnenie_byudzheta,
    mezhbyudzhetnye_transferty,
    poisk_uchastnikov_bp,
    poisk_uchrezhdeniy,
    spisok_kategoriy_raskhodov,
    spisok_vidov_byudzhetov,
)

mcp = FastMCP("mcp-russia-kaznacheistvo")

# Tools
mcp.tool(spisok_vidov_byudzhetov, tags={"виды-бюджетов", "справочник"})
mcp.tool(spisok_kategoriy_raskhodov, tags={"категории-расходов", "справочник"})
mcp.tool(ispolnenie_byudzheta, tags={"бюджет", "исполнение"})
mcp.tool(poisk_uchastnikov_bp, tags={"участники-бп", "поиск"})
mcp.tool(poisk_uchrezhdeniy, tags={"учреждения", "поиск"})
mcp.tool(mezhbyudzhetnye_transferty, tags={"межбюджетные-трансферты", "поиск"})

# Resources
mcp.resource("data://kaznacheistvo/istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://kaznacheistvo/struktura", mime_type="text/plain")(struktura_kaznacheistva)
mcp.resource("data://kaznacheistvo/byudzhetnaya-sistema", mime_type="text/plain")(
    byudzhetnaya_sistema
)

# Prompts
mcp.prompt(analiz_ispolneniya_byudzheta)
mcp.prompt(obzor_byudzhetnoy_sistemy)
