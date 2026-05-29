"""⚠️ DEPRECATED — Compras feature server (legacy) — composes sub-servers for each procurement source.

.. deprecated::
    Используйте модуль ``mcp_russia.data.zakupki`` (ЕИС — zakupki.gov.ru) для российских госзакупок.

Brazilian Procurement API compatibility layer within mcp-russia.
Uses FastMCP mount() to namespace tools from each data source:
- pncp: Portal Nacional de Contratações Públicas (Lei 14.133/2021) — ⚠️ DEPRECATED
- dadosabertos: Dados Abertos Compras.gov.br (SIASG/ComprasNet) — ⚠️ DEPRECATED

This file only composes sub-servers. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .dadosabertos.server import mcp as dadosabertos_mcp
from .pncp.server import mcp as pncp_mcp

mcp = FastMCP("mcp-russia-compras-legacy (⚠️ DEPRECATED — use 'zakupki' for Russian procurement)")

# Mount sub-sources with namespace
mcp.mount(pncp_mcp, namespace="pncp")
mcp.mount(dadosabertos_mcp, namespace="dadosabertos")
