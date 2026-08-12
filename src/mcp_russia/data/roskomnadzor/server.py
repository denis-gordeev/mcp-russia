"""Сервер модуля Роскомнадзора — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_narusheniya, obzor_reestrov
from .resources import (
    istochniki_dannyh,
    struktura_roskomnadzora,
    zakonodatelstvo,
)
from .tools import (
    info_litsenzii,
    info_operatora_pd,
    poisk_narusheniy,
    poisk_ori,
    poisk_smi,
    proverka_blokirovki,
    spisok_kategoriy_narusheniy,
    spisok_kategoriy_pd_operatorov,
    spisok_napravleniy,
    spisok_reestrov,
    spisok_tipov_litsenziy,
    spisok_tipov_smi,
    zapisi_reestra,
)

mcp = FastMCP(
    "mcp-russia-roskomnadzor", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya
)

# Инструменты
mcp.tool(spisok_napravleniy, tags={"направления", "справочник"})
mcp.tool(spisok_tipov_litsenziy, tags={"лицензии", "справочник"})
mcp.tool(spisok_kategoriy_narusheniy, tags={"нарушения", "справочник"})
mcp.tool(spisok_reestrov, tags={"реестры", "справочник"})
mcp.tool(spisok_tipov_smi, tags={"сми", "справочник"})
mcp.tool(spisok_kategoriy_pd_operatorov, tags={"операторы-пд", "справочник"})
mcp.tool(info_litsenzii, tags={"лицензия", "информация"})
mcp.tool(poisk_smi, tags={"сми", "поиск"})
mcp.tool(info_operatora_pd, tags={"оператор-пд", "информация"})
mcp.tool(poisk_narusheniy, tags={"нарушения", "поиск"})
mcp.tool(proverka_blokirovki, tags={"блокировка", "проверка"})
mcp.tool(poisk_ori, tags={"ори", "поиск"})
mcp.tool(zapisi_reestra, tags={"реестр", "записи"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_roskomnadzora)

# Промпты
mcp.prompt(analiz_narusheniya)
mcp.prompt(obzor_reestrov)
