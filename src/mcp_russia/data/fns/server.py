"""Сервер модуля ФНС — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_nalogoplatelshchika, obzor_rezhimov_nalogooblozheniya
from .resources import istochniki_dannyh, sistema_nalogovyh_organov, zakonodatelstvo
from .tools import (
    info_ip,
    info_organizatsii,
    nalogovye_nachisleniya,
    proverki_organizatsii,
    spisok_kategoriy_nalogoplatelshchikov,
    spisok_nalogovyh_rezhimov,
    spisok_statusov_organizatsiy,
    spisok_tipov_proverok,
    spisok_vidov_nalogov,
)

mcp = FastMCP("mcp-russia-fns", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya)

mcp.tool(spisok_nalogovyh_rezhimov, tags={"режимы", "справочник"})
mcp.tool(spisok_vidov_nalogov, tags={"налоги", "справочник"})
mcp.tool(spisok_tipov_proverok, tags={"проверки", "справочник"})
mcp.tool(spisok_statusov_organizatsiy, tags={"статус", "справочник"})
mcp.tool(spisok_kategoriy_nalogoplatelshchikov, tags={"категории", "справочник"})
mcp.tool(info_organizatsii, tags={"егрюл", "информация"})
mcp.tool(info_ip, tags={"егрип", "информация"})
mcp.tool(proverki_organizatsii, tags={"проверки", "поиск"})
mcp.tool(nalogovye_nachisleniya, tags={"начисления", "информация"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(sistema_nalogovyh_organov)

mcp.prompt(analiz_nalogoplatelshchika)
mcp.prompt(obzor_rezhimov_nalogooblozheniya)
