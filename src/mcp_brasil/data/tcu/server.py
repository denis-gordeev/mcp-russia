"""TCU feature server (legacy) — registers tools, resources, and prompts.

Brazilian Federal Court of Accounts API compatibility layer within mcp-russia.
This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import investigar_empresa_tcu
from .resources import tipos_certidoes_apf
from .tools import (
    buscar_acordaos,
    buscar_contratos_tcu,
    buscar_pedidos_congresso,
    calcular_debito_tcu,
    consultar_cadirreg,
    consultar_certidoes_apf,
    consultar_inabilitados,
    consultar_inidoneos,
)

mcp = FastMCP("mcp-russia-tcu-legacy")

# Tools
mcp.tool(buscar_acordaos, tags={"поиск", "решения", "аудит"})
mcp.tool(consultar_inabilitados, tags={"запрос", "дисквалифицированные", "санкции"})
mcp.tool(consultar_inidoneos, tags={"запрос", "недобросовестные", "санкции", "тендеры"})
mcp.tool(consultar_certidoes_apf, tags={"запрос", "сертификаты", "комплаенс"})
mcp.tool(calcular_debito_tcu, tags={"расчёт", "задолженность", "денежная-коррекция"})
mcp.tool(buscar_pedidos_congresso, tags={"поиск", "конгресс", "контроль"})
mcp.tool(buscar_contratos_tcu, tags={"поиск", "контракты", "закупки"})
mcp.tool(consultar_cadirreg, tags={"запрос", "нерегулярные-счета", "санкции"})

# Resources
mcp.resource("data://tipos-certidoes-apf", mime_type="application/json")(tipos_certidoes_apf)

# Prompts
mcp.prompt(investigar_empresa_tcu)
