"""Сервер модуля ЦБ РФ — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import analiz_valyut, obzor_ekonomiki
from .resources import dostupnye_valyuty, osnovnye_valyuty, spravochnik_kursov
from .tools import (
    konvertirovat_valyutu,
    kursy_po_stranam,
    spisok_valyut,
    sravnit_valyuty,
    tekushchie_kursy,
    uznat_kurs_valyuty,
)

mcp = FastMCP("mcp-russia-cbrf")

mcp.tool(tekushchie_kursy, tags={"курсы-валют", "основные"})
mcp.tool(uznat_kurs_valyuty, tags={"курс-валюты", "конкретная"})
mcp.tool(spisok_valyut, tags={"справочник", "все-валюты"})
mcp.tool(konvertirovat_valyutu, tags={"конвертация", "рубли"})
mcp.tool(sravnit_valyuty, tags={"сравнение", "валюты"})
mcp.tool(kursy_po_stranam, tags={"страны-партнёры", "валюты"})

mcp.resource("data://valyuty", mime_type="text/plain")(dostupnye_valyuty)
mcp.resource("data://osnovnye", mime_type="text/plain")(osnovnye_valyuty)
mcp.resource("data://spravochnik", mime_type="text/plain")(spravochnik_kursov)

mcp.prompt(analiz_valyut)
mcp.prompt(obzor_ekonomiki)
