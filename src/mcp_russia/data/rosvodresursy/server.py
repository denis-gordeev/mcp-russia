"""Сервер модуля Росводресурсов — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_vodnogo_obekta, obzor_vodokhranilishch
from .resources import (
    basseynovye_okruga_info,
    istochniki_dannyh,
    vodokhozyaystvennaya_deyatelnost,
)
from .tools import (
    gidro_monitoring,
    info_vodnogo_obekta,
    info_vodokhranilishcha,
    poisk_vodnykh_obektov,
    spisok_basseynovykh_okrugov,
    spisok_tipov_vodnykh_obektov,
    spisok_vodokhranilishch,
    vodopolzovanie_regionov,
)

mcp = FastMCP("mcp-russia-rosvodresursy")

# Tools
mcp.tool(spisok_basseynovykh_okrugov, tags={"бассейновые-округа", "справочник"})
mcp.tool(spisok_tipov_vodnykh_obektov, tags={"типы-водных-объектов", "справочник"})
mcp.tool(spisok_vodokhranilishch, tags={"водохранилища", "справочник"})
mcp.tool(poisk_vodnykh_obektov, tags={"водный-объект", "поиск"})
mcp.tool(info_vodnogo_obekta, tags={"водный-объект", "информация"})
mcp.tool(gidro_monitoring, tags={"гидрология", "мониторинг"})
mcp.tool(info_vodokhranilishcha, tags={"водохранилище", "информация"})
mcp.tool(vodopolzovanie_regionov, tags={"водопользование", "регионы"})

# Resources
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://basseynovye-okruga", mime_type="text/plain")(basseynovye_okruga_info)
mcp.resource("data://vodokhozyaystvo", mime_type="text/plain")(vodokhozyaystvennaya_deyatelnost)

# Prompts
mcp.prompt(analiz_vodnogo_obekta)
mcp.prompt(obzor_vodokhranilishch)
