"""Сервер модуля Росприроднадзора — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (CONTRIBUTING.md, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_ekologicheskoy_proverki, obzor_nedropolzovaniya
from .resources import (
    istochniki_dannyh,
    struktura_rosprirodnadzora,
    zakonodatelstvo_ekologicheskoe,
)
from .tools import (
    ekologicheskie_platezhi,
    info_proverki,
    poisk_lesnogo_nadzora,
    poisk_litsenziy_nedra,
    poisk_obektov_negativnogo,
    poisk_proverok,
    spisok_kategoriy_obnv,
    spisok_vidov_litsenziy_nedra,
    spisok_vidov_nadzora,
)

mcp = FastMCP(
    "mcp-russia-rosprirodnadzor",
    instructions=META_FUNKTSII.opisanie,
    version=META_FUNKTSII.versiya,
)

# Инструменты
mcp.tool(spisok_vidov_nadzora, tags={"виды-надзора", "справочник"})
mcp.tool(spisok_kategoriy_obnv, tags={"категории-ОНВ", "справочник"})
mcp.tool(spisok_vidov_litsenziy_nedra, tags={"лицензии-недра", "справочник"})
mcp.tool(poisk_proverok, tags={"проверка", "поиск"})
mcp.tool(info_proverki, tags={"проверка", "информация"})
mcp.tool(poisk_obektov_negativnogo, tags={"ОНВ", "поиск"})
mcp.tool(poisk_litsenziy_nedra, tags={"лицензии-недра", "поиск"})
mcp.tool(ekologicheskie_platezhi, tags={"экологические-платежи", "данные"})
mcp.tool(poisk_lesnogo_nadzora, tags={"лесной-надзор", "поиск"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_rosprirodnadzora)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo_ekologicheskoe)

# Промпты
mcp.prompt(analiz_ekologicheskoy_proverki)
mcp.prompt(obzor_nedropolzovaniya)
