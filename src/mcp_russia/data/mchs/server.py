"""Сервер модуля МЧС России — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_chrezvychaynoy_situatsii, obzor_pozharnoy_obstanovki
from .resources import istochniki_dannyh, struktura_mchs, zakonodatelstvo_chs
from .tools import (
    gidrologicheskaya_obstanovka,
    poisk_chs,
    preduprezhdeniya_chs,
    radiatsionnyy_monitoring,
    spisok_klassov_chs,
    spisok_tipov_opasnosti,
    spisok_vidov_chs,
    spisok_vidov_pojarov,
    statistika_pojarov,
)

mcp = FastMCP("mcp-russia-mchs")

mcp.tool(spisok_vidov_chs, tags={"виды-ЧС", "справочник"})
mcp.tool(spisok_klassov_chs, tags={"классы-ЧС", "справочник"})
mcp.tool(spisok_vidov_pojarov, tags={"пожары", "справочник"})
mcp.tool(spisok_tipov_opasnosti, tags={"опасности", "справочник"})
mcp.tool(statistika_pojarov, tags={"пожары", "статистика"})
mcp.tool(poisk_chs, tags={"ЧС", "поиск"})
mcp.tool(radiatsionnyy_monitoring, tags={"радиация", "мониторинг"})
mcp.tool(gidrologicheskaya_obstanovka, tags={"гидрология", "мониторинг"})
mcp.tool(preduprezhdeniya_chs, tags={"предупреждения", "ЧС"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_mchs)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo_chs)

mcp.prompt(analiz_chrezvychaynoy_situatsii)
mcp.prompt(obzor_pozharnoy_obstanovki)
