"""Сервер модуля МВД России — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (CONTRIBUTING.md, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_prestupnosti, obzor_dorozhnoy_bezopasnosti
from .resources import istochniki_dannyh, struktura_mvd, zakonodatelstvo
from .tools import (
    narkotiki,
    rozysk_del,
    spisok_federalnykh_okrugov,
    spisok_naborov_dannykh,
    spisok_vidov_dtp,
    spisok_vidov_prestupleniy,
    statistika_dtp,
    statistika_prestupnosti,
)

mcp = FastMCP("mcp-russia-mvd", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya)

mcp.tool(spisok_naborov_dannykh, tags={"наборы-данных", "справочник"})
mcp.tool(spisok_vidov_prestupleniy, tags={"преступления", "справочник"})
mcp.tool(spisok_vidov_dtp, tags={"дтп", "справочник"})
mcp.tool(spisok_federalnykh_okrugov, tags={"федеральные-округа", "справочник"})
mcp.tool(statistika_prestupnosti, tags={"преступность", "статистика"})
mcp.tool(statistika_dtp, tags={"дтп", "статистика"})
mcp.tool(rozysk_del, tags={"розыск", "данные"})
mcp.tool(narkotiki, tags={"наркотики", "статистика"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_mvd)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)

mcp.prompt(analiz_prestupnosti)
mcp.prompt(obzor_dorozhnoy_bezopasnosti)
