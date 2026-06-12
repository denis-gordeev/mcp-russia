"""Сервер модуля ГИБДД/МВД — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_transportnogo_sredstva, analiz_voditelya
from .resources import istochniki_dannyh, sistema_gibdd, zakonodatelstvo
from .tools import (
    info_ts,
    info_vu,
    istoriya_registraciy,
    shtrafy_po_ts,
    shtrafy_po_vu,
    spisok_kategoriyy_vu,
    spisok_regionov_registratsii,
    spisok_statusov_shtrafov,
    spisok_tipov_dtp,
    spisok_tipov_ts,
    spisok_vidov_narusheniy,
    statistika_dtp,
)

mcp = FastMCP("mcp-russia-gibdd")

mcp.tool(spisok_tipov_ts, tags={"тс", "справочник"})
mcp.tool(spisok_kategoriyy_vu, tags={"ву", "справочник"})
mcp.tool(spisok_vidov_narusheniy, tags={"нарушения", "справочник"})
mcp.tool(spisok_statusov_shtrafov, tags={"штрафы", "справочник"})
mcp.tool(spisok_tipov_dtp, tags={"дтп", "справочник"})
mcp.tool(spisok_regionov_registratsii, tags={"регионы", "справочник"})
mcp.tool(info_ts, tags={"тс", "информация"})
mcp.tool(info_vu, tags={"ву", "информация"})
mcp.tool(shtrafy_po_ts, tags={"штрафы", "поиск"})
mcp.tool(shtrafy_po_vu, tags={"штрафы", "поиск"})
mcp.tool(statistika_dtp, tags={"дтп", "статистика"})
mcp.tool(istoriya_registraciy, tags={"регистрация", "информация"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(sistema_gibdd)

mcp.prompt(analiz_transportnogo_sredstva)
mcp.prompt(analiz_voditelya)
