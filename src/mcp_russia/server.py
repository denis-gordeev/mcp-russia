"""Public server entrypoint for mcp-russia.

The internal feature tree still lives under ``mcp_brasil`` during the
repository migration. This module exposes the stable public import path.
"""

from mcp_brasil.server import (
    mcp,
    registry,
    rekomendovat_instrumenty,
    spisok_funktsiy,
    splanirovat_zapros,
    vypolnit_paket,
)

__all__ = [
    "mcp",
    "registry",
    "rekomendovat_instrumenty",
    "spisok_funktsiy",
    "splanirovat_zapros",
    "vypolnit_paket",
]
