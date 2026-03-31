"""Configuração global do mcp-russia.

Valores podem ser sobrescritos via variáveis de ambiente.
Carrega automaticamente o arquivo .env na raiz do projeto.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# --- HTTP Client ---
HTTP_TIMEOUT: float = float(
    os.environ.get("MCP_RUSSIA_HTTP_TIMEOUT", os.environ.get("MCP_BRASIL_HTTP_TIMEOUT", "30.0"))
)
HTTP_MAX_RETRIES: int = int(
    os.environ.get(
        "MCP_RUSSIA_HTTP_MAX_RETRIES",
        os.environ.get("MCP_BRASIL_HTTP_MAX_RETRIES", "3"),
    )
)
HTTP_BACKOFF_BASE: float = float(
    os.environ.get(
        "MCP_RUSSIA_HTTP_BACKOFF_BASE",
        os.environ.get("MCP_BRASIL_HTTP_BACKOFF_BASE", "1.0"),
    )
)
USER_AGENT: str = os.environ.get(
    "MCP_RUSSIA_USER_AGENT",
    os.environ.get("MCP_BRASIL_USER_AGENT", "mcp-russia/0.5.0"),
)

# --- Tool Discovery ---
# "bm25" (default): BM25 search transform — replaces list_tools with search_tools + call_tool
# "code_mode": Experimental CodeMode transform — search + get_tags + execute
# "none": No transform — all 154+ tools visible at once
TOOL_SEARCH: str = os.environ.get(
    "MCP_RUSSIA_TOOL_SEARCH",
    os.environ.get("MCP_BRASIL_TOOL_SEARCH", "bm25"),
)

# --- LLM Discovery (recomendar_tools) ---
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
