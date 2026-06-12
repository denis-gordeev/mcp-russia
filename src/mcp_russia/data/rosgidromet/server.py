"""Сервер модуля Росгидромета — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_pogody_regiona, obzor_ekologii
from .resources import istochniki_dannyh, metodologiya, opasnye_yavleniya
from .tools import (
    ekologiya_regiona,
    pogoda_seychas,
    preduprezhdeniya,
    prognoz_pogody,
    spisok_stanciy,
    spisok_tipov_dannykh,
    sputnik_monitoring,
)

mcp = FastMCP("mcp-russia-rosgidromet")

# Tools
mcp.tool(spisok_stanciy, tags={"станции", "справочник"})
mcp.tool(spisok_tipov_dannykh, tags={"типы-данных", "справочник"})
mcp.tool(pogoda_seychas, tags={"погода", "текущая"})
mcp.tool(prognoz_pogody, tags={"прогноз", "погода"})
mcp.tool(ekologiya_regiona, tags={"экология", "регион"})
mcp.tool(preduprezhdeniya, tags={"предупреждения", "опасные-явления"})
mcp.tool(sputnik_monitoring, tags={"спутники", "мониторинг"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://metodologiya", mime_type="text/plain")(metodologiya)
mcp.resource("data://opasnye-yavleniya", mime_type="text/plain")(opasnye_yavleniya)

# Prompts
mcp.prompt(analiz_pogody_regiona)
mcp.prompt(obzor_ekologii)
