"""Сервер функции deloproizvodstvo — регистрирует инструменты, ресурсы и prompts.

Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import (
    redaktor_akt,
    redaktor_dokladnaya_zapiska,
    redaktor_pismo,
    redaktor_prikaz,
    redaktor_protokol,
    redaktor_rasporyazhenie,
    redaktor_spravka,
)
from .resources import (
    get_manual_deloproizvodstvo,
    get_obrashcheniya,
    get_template_akt,
    get_template_dokladnaya_zapiska,
    get_template_pismo,
    get_template_prikaz,
    get_template_protokol,
    get_template_rasporyazhenie,
    get_template_spravka,
    get_zaklyuchitelnye_formuly,
)
from .tools import (
    formatirovat_data_extenso,
    generirovat_numeraciyu,
    konsulitirovat_obrashchenie,
    spisok_tipov_dokumentov,
    validirovat_dokument,
)

mcp = FastMCP("mcp-russia-deloproizvodstvo")

# Tools
mcp.tool(formatirovat_data_extenso, tags={"форматирование", "дата"})
mcp.tool(generirovat_numeraciyu, tags={"форматирование", "нумерация"})
mcp.tool(konsulitirovat_obrashchenie, tags={"справочник", "обращения"})
mcp.tool(validirovat_dokument, tags={"валидация", "документ"})
mcp.tool(spisok_tipov_dokumentov, tags={"справочник", "типы-документов"})

# Prompts
mcp.prompt(redaktor_pismo)
mcp.prompt(redaktor_prikaz)
mcp.prompt(redaktor_rasporyazhenie)
mcp.prompt(redaktor_akt)
mcp.prompt(redaktor_spravka)
mcp.prompt(redaktor_protokol)
mcp.prompt(redaktor_dokladnaya_zapiska)

# Resources
mcp.resource("template://pismo")(get_template_pismo)
mcp.resource("template://prikaz")(get_template_prikaz)
mcp.resource("template://rasporyazhenie")(get_template_rasporyazhenie)
mcp.resource("template://akt")(get_template_akt)
mcp.resource("template://spravka")(get_template_spravka)
mcp.resource("template://protokol")(get_template_protokol)
mcp.resource("template://dokladnaya_zapiska")(get_template_dokladnaya_zapiska)
mcp.resource("normas://manual")(get_manual_deloproizvodstvo)
mcp.resource("normas://obrashcheniya")(get_obrashcheniya)
mcp.resource("normas://zaklyuchitelnye")(get_zaklyuchitelnye_formuly)
