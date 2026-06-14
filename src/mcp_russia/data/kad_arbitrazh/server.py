"""Сервер модуля Картотеки арбитражных дел — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_dela, analiz_uchastnika
from .resources import istochniki_dannyh, kodifikatsiya_del, sistema_sudov
from .tools import (
    akty_po_delu,
    info_dela,
    poisk_del,
    spravochnik_aktov,
    spravochnik_instantsiy,
    spravochnik_kategoriy,
    spravochnik_statusov,
    storony_dela,
)

mcp = FastMCP("mcp-russia-kad-arbitrazh")

# Инструменты
mcp.tool(poisk_del, tags={"дела", "поиск"})
mcp.tool(info_dela, tags={"дело", "подробности"})
mcp.tool(akty_po_delu, tags={"акты", "судебные-акты"})
mcp.tool(storony_dela, tags={"стороны", "участники"})
mcp.tool(spravochnik_kategoriy, tags={"категории", "справочник"})
mcp.tool(spravochnik_instantsiy, tags={"инстанции", "справочник"})
mcp.tool(spravochnik_statusov, tags={"статусы", "справочник"})
mcp.tool(spravochnik_aktov, tags={"типы-актов", "справочник"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://sistema", mime_type="text/plain")(sistema_sudov)
mcp.resource("data://kodifikatsiya", mime_type="text/plain")(kodifikatsiya_del)

# Промпты
mcp.prompt(analiz_dela)
mcp.prompt(analiz_uchastnika)
