"""Сервер модуля Ростехнадзора — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (CONTRIBUTING.md, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_intsidenta, obzor_promyshlennoy_bezopasnosti
from .resources import istochniki_dannyh, struktura_rostekhnadzora, zakonodatelstvo_prombez
from .tools import (
    poisk_intsidentov,
    poisk_litsenziy,
    reestr_opo,
    spisok_klassov_opasnosti,
    spisok_vidov_intsidentov,
    spisok_vidov_litsenziy,
    spisok_vidov_nadzora,
)

mcp = FastMCP(
    "mcp-russia-rostekhnadzor", instructions=META_FUNKTSII.opisanie, version=META_FUNKTSII.versiya
)

mcp.tool(spisok_vidov_nadzora, tags={"надзор", "справочник"})
mcp.tool(spisok_klassov_opasnosti, tags={"опасность", "справочник"})
mcp.tool(spisok_vidov_litsenziy, tags={"лицензии", "справочник"})
mcp.tool(spisok_vidov_intsidentov, tags={"инциденты", "справочник"})
mcp.tool(poisk_intsidentov, tags={"инциденты", "поиск"})
mcp.tool(poisk_litsenziy, tags={"лицензии", "поиск"})
mcp.tool(reestr_opo, tags={"ОПО", "реестр"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_rostekhnadzora)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo_prombez)

mcp.prompt(analiz_intsidenta)
mcp.prompt(obzor_promyshlennoy_bezopasnosti)
