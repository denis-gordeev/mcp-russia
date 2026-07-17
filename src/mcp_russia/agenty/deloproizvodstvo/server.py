"""Сервер функции deloproizvodstvo — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (правило ADR-001 №4).
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
    poluchit_manual_deloproizvodstvo,
    poluchit_obrashcheniya,
    poluchit_shablon_akt,
    poluchit_shablon_dokladnaya_zapiska,
    poluchit_shablon_pismo,
    poluchit_shablon_prikaz,
    poluchit_shablon_protokol,
    poluchit_shablon_rasporyazhenie,
    poluchit_shablon_spravka,
    poluchit_zaklyuchitelnye_formuly,
)
from .tools import (
    formatirovat_datu_propisyu,
    generirovat_numeraciyu,
    konsulitirovat_obrashchenie,
    spisok_tipov_dokumentov,
    validirovat_dokument,
)

mcp = FastMCP("mcp-russia-deloproizvodstvo")

# Инструменты
mcp.tool(formatirovat_datu_propisyu, tags={"форматирование", "дата"})
mcp.tool(generirovat_numeraciyu, tags={"форматирование", "нумерация"})
mcp.tool(konsulitirovat_obrashchenie, tags={"справочник", "обращения"})
mcp.tool(validirovat_dokument, tags={"валидация", "документ"})
mcp.tool(spisok_tipov_dokumentov, tags={"справочник", "типы-документов"})

# Промпты
mcp.prompt(redaktor_pismo)
mcp.prompt(redaktor_prikaz)
mcp.prompt(redaktor_rasporyazhenie)
mcp.prompt(redaktor_akt)
mcp.prompt(redaktor_spravka)
mcp.prompt(redaktor_protokol)
mcp.prompt(redaktor_dokladnaya_zapiska)

# Ресурсы
mcp.resource("shablon://pismo")(poluchit_shablon_pismo)
mcp.resource("shablon://prikaz")(poluchit_shablon_prikaz)
mcp.resource("shablon://rasporyazhenie")(poluchit_shablon_rasporyazhenie)
mcp.resource("shablon://akt")(poluchit_shablon_akt)
mcp.resource("shablon://spravka")(poluchit_shablon_spravka)
mcp.resource("shablon://protokol")(poluchit_shablon_protokol)
mcp.resource("shablon://dokladnaya_zapiska")(poluchit_shablon_dokladnaya_zapiska)
mcp.resource("normy://manual")(poluchit_manual_deloproizvodstvo)
mcp.resource("normy://obrashcheniya")(poluchit_obrashcheniya)
mcp.resource("normy://zaklyuchitelnye")(poluchit_zaklyuchitelnye_formuly)
