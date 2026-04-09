"""CBRF feature server — registers tools, resources, and prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_valyut, obzor_ekonomiki
from .resources import moedas_disponiveis, moedas_principais, referencia_cursos
from .tools import (
    comparar_moedas,
    consultar_moeda,
    converter_moeda,
    cursos_atuais,
    cursos_por_pais,
    listar_moedas,
)

mcp = FastMCP("mcp-russia-cbrf")

# Tools
mcp.tool(cursos_atuais, tags={"курсы-валют", "основные"})
mcp.tool(consultar_moeda, tags={"курс-валюты", "конкретная"})
mcp.tool(listar_moedas, tags={"справочник", "все-валюты"})
mcp.tool(converter_moeda, tags={"конвертация", "рубли"})
mcp.tool(comparar_moedas, tags={"сравнение", "валюты"})
mcp.tool(cursos_por_pais, tags={"страны-партнёры", "валюты"})

# Resources
mcp.resource("data://moedas", mime_type="text/plain")(moedas_disponiveis)
mcp.resource("data://principais", mime_type="text/plain")(moedas_principais)
mcp.resource("data://referencia", mime_type="text/plain")(referencia_cursos)

# Prompts
mcp.prompt(analise_valyut)
mcp.prompt(obzor_ekonomiki)
