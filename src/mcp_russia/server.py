"""Public server entrypoint for mcp-russia.

The internal feature tree still lives under ``mcp_brasil`` during the
repository migration. This module exposes the stable public import path.
"""

from mcp_brasil.server import (
    executar_lote,
    listar_features,
    mcp,
    planejar_consulta,
    recomendar_tools,
    registry,
)

__all__ = [
    "executar_lote",
    "listar_features",
    "mcp",
    "planejar_consulta",
    "recomendar_tools",
    "registry",
]
