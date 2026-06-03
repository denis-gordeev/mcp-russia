"""Сервер функции ЦИК РФ — регистрация инструментов, ресурсов и промптов.

Минимум бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_kandidata, sravnenie_partiy
from .resources import (
    info_api,
    izvestnye_vybory_resource,
    partii_rf_resource,
    subyekty_rf_resource,
    tipy_vyborov_resource,
)
from .tools import (
    dolzhnosti_federal,
    gody_vyborov,
    kandidat_podrobno,
    partii_rf,
    poisk_kandidata,
    rezultaty_vyborov,
    spisok_vyborov,
    subyekty_rf,
    tipy_vyborov,
    yavka_i_itogi,
)

mcp = FastMCP("mcp-russia-cekrf")

# Инструменты (10)
mcp.tool(tipy_vyborov, tags={"список", "типы-выборов", "справочник"})
mcp.tool(subyekty_rf, tags={"список", "субъекты-рф", "справочник"})
mcp.tool(dolzhnosti_federal, tags={"список", "должности", "федеральные"})
mcp.tool(partii_rf, tags={"список", "партии", "справочник"})
mcp.tool(gody_vyborov, tags={"список", "годы-выборов", "справочник"})
mcp.tool(spisok_vyborov, tags={"список", "выборы", "поиск"})
mcp.tool(poisk_kandidata, tags={"поиск", "кандидаты", "фио"})
mcp.tool(kandidat_podrobno, tags={"подробности", "кандидаты", "биография"})
mcp.tool(rezultaty_vyborov, tags={"результаты", "голосование", "итоги"})
mcp.tool(yavka_i_itogi, tags={"явка", "итоги", "статистика"})

# Ресурсы (5)
mcp.resource("data://tipy-vyborov", mime_type="application/json")(tipy_vyborov_resource)
mcp.resource("data://subyekty-rf", mime_type="application/json")(subyekty_rf_resource)
mcp.resource("data://partii-rf", mime_type="application/json")(partii_rf_resource)
mcp.resource("data://izvestnye-vybory", mime_type="application/json")(izvestnye_vybory_resource)
mcp.resource("data://info-api", mime_type="application/json")(info_api)

# Промпты (2)
mcp.prompt(analiz_kandidata)
mcp.prompt(sravnenie_partiy)
