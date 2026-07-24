"""Сервер модуля Росстата — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_regiona, obzor_inflyatsii
from .resources import istochniki_dannyh, metodologiya
from .tools import (
    demografiya,
    indikator_dannye,
    inflyatsiya,
    informatsiya_o_regionye,
    informatsiya_ob_okruge,
    investitsii_po_vidam,
    otraslevaya_struktura_vrp,
    pokazateli_rosstata,
    spisok_okrugov,
    spisok_regionov,
    sravnenie_regionov,
    vrp_dannye,
    zarplata_dannye,
)

mcp = FastMCP("mcp-russia-rosstat")

# Инструменты
mcp.tool(spisok_regionov, tags={"регионы", "справочник"})
mcp.tool(spisok_okrugov, tags={"федеральные-округа", "справочник"})
mcp.tool(informatsiya_o_regionye, tags={"регион", "информация"})
mcp.tool(informatsiya_ob_okruge, tags={"федеральный-округ", "информация"})
mcp.tool(pokazateli_rosstata, tags={"показатели", "справочник"})
mcp.tool(inflyatsiya, tags={"инфляция", "ИПЦ"})
mcp.tool(demografiya, tags={"демография", "население"})
mcp.tool(vrp_dannye, tags={"ВРП", "экономика"})
mcp.tool(zarplata_dannye, tags={"зарплата", "экономика"})
mcp.tool(sravnenie_regionov, tags={"сравнение", "регионы"})
mcp.tool(indikator_dannye, tags={"показатель", "ЕМИСС", "универсальный"})
mcp.tool(otraslevaya_struktura_vrp, tags={"ВРП", "отрасли", "ОКВЭД"})
mcp.tool(investitsii_po_vidam, tags={"инвестиции", "отрасли", "ОКВЭД"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://metodologiya", mime_type="text/plain")(metodologiya)

# Промпты
mcp.prompt(analiz_regiona)
mcp.prompt(obzor_inflyatsii)
