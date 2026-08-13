"""Сервер модуля Федерального казначейства — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (CONTRIBUTING.md, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_ispolneniya_byudzheta, obzor_byudzhetnoy_sistemy
from .resources import byudzhetnaya_sistema, istochniki_dannyh, struktura_kaznacheistva
from .tools import (
    byudzhetnaya_smeta,
    ispolnenie_byudzheta,
    mezhbyudzhetnye_transferty,
    poisk_uchastnikov_bp,
    poisk_uchrezhdeniy,
    spisok_kategoriy_raskhodov,
    spisok_podrazdelov_byudzheta,
    spisok_razdelov_byudzheta,
    spisok_vidov_byudzhetov,
)

mcp = FastMCP(
    "mcp-russia-kaznacheistvo", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya
)

# Инструменты
mcp.tool(spisok_vidov_byudzhetov, tags={"виды-бюджетов", "справочник"})
mcp.tool(spisok_kategoriy_raskhodov, tags={"категории-расходов", "справочник"})
mcp.tool(ispolnenie_byudzheta, tags={"бюджет", "исполнение"})
mcp.tool(poisk_uchastnikov_bp, tags={"участники-бп", "поиск"})
mcp.tool(poisk_uchrezhdeniy, tags={"учреждения", "поиск"})
mcp.tool(mezhbyudzhetnye_transferty, tags={"межбюджетные-трансферты", "поиск"})
mcp.tool(spisok_razdelov_byudzheta, tags={"разделы-БК", "справочник"})
mcp.tool(spisok_podrazdelov_byudzheta, tags={"подразделы-БК", "справочник"})
mcp.tool(byudzhetnaya_smeta, tags={"смета", "информация"})

# Ресурсы
mcp.resource("data://kaznacheistvo/istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://kaznacheistvo/struktura", mime_type="text/plain")(struktura_kaznacheistva)
mcp.resource("data://kaznacheistvo/byudzhetnaya-sistema", mime_type="text/plain")(
    byudzhetnaya_sistema
)

# Промпты
mcp.prompt(analiz_ispolneniya_byudzheta)
mcp.prompt(obzor_byudzhetnoy_sistemy)
