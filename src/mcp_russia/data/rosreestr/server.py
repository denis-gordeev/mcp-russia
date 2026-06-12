"""Сервер модуля Росреестра — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_nedvizhimosti, obzor_zemelnogo_uchastka
from .resources import istochniki_dannyh, sistema_rogistracii, zakonodatelstvo
from .tools import (
    info_obekta,
    kadastrovaya_stoimost,
    prava_na_obekt,
    spisok_form_sobstvennosti,
    spisok_kategoriy_zemel,
    spisok_statusov_obiekta,
    spisok_tipov_nedvizhimosti,
    spisok_vidov_ispolzovaniya,
)

mcp = FastMCP("mcp-russia-rosreestr")

mcp.tool(spisok_tipov_nedvizhimosti, tags={"типы", "справочник"})
mcp.tool(spisok_kategoriy_zemel, tags={"категории", "справочник"})
mcp.tool(spisok_vidov_ispolzovaniya, tags={"виды-использования", "справочник"})
mcp.tool(spisok_statusov_obiekta, tags={"статус", "справочник"})
mcp.tool(spisok_form_sobstvennosti, tags={"собственность", "справочник"})
mcp.tool(info_obekta, tags={"объект", "информация"})
mcp.tool(kadastrovaya_stoimost, tags={"стоимость", "кадастр"})
mcp.tool(prava_na_obekt, tags={"права", "информация"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(sistema_rogistracii)

mcp.prompt(analiz_nedvizhimosti)
mcp.prompt(obzor_zemelnogo_uchastka)
