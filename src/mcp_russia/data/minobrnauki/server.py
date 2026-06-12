"""Сервер модуля Минобрнауки — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_vuza, obzor_nauchnyh_grantov
from .resources import istochniki_dannyh, sistema_obrazovaniya, zakonodatelstvo
from .tools import (
    aspirantura,
    granty_i_isledovaniya,
    info_vuza,
    poisk_licenziy,
    programmy_vuza,
    reyting_vuzov,
    spisok_federalnyh_okrugov,
    spisok_form_obucheniya,
    spisok_otrasley_nauki,
    spisok_statusov_akkreditatsii,
    spisok_tipov_grantov,
    spisok_tipov_vuzov,
    spisok_urovney_obrazovaniya,
)

mcp = FastMCP("mcp-russia-minobrnauki")

mcp.tool(spisok_tipov_vuzov, tags={"вузы", "справочник"})
mcp.tool(spisok_form_obucheniya, tags={"обучение", "справочник"})
mcp.tool(spisok_urovney_obrazovaniya, tags={"образование", "справочник"})
mcp.tool(spisok_otrasley_nauki, tags={"наука", "справочник"})
mcp.tool(spisok_tipov_grantov, tags={"гранты", "справочник"})
mcp.tool(spisok_statusov_akkreditatsii, tags={"аккредитация", "справочник"})
mcp.tool(spisok_federalnyh_okrugov, tags={"округа", "справочник"})
mcp.tool(info_vuza, tags={"вузы", "информация"})
mcp.tool(programmy_vuza, tags={"программы", "информация"})
mcp.tool(granty_i_isledovaniya, tags={"гранты", "поиск"})
mcp.tool(reyting_vuzov, tags={"рейтинг", "информация"})
mcp.tool(aspirantura, tags={"аспирантура", "информация"})
mcp.tool(poisk_licenziy, tags={"лицензии", "поиск"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo)
mcp.resource("data://struktura", mime_type="text/plain")(sistema_obrazovaniya)

mcp.prompt(analiz_vuza)
mcp.prompt(obzor_nauchnyh_grantov)
