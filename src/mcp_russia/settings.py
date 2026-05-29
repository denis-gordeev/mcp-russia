"""Глобальная конфигурация mcp-russia.

Значения могут быть переопределены через переменные окружения.
Автоматически загружает файл .env в корне проекта.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# --- HTTP-клиент ---
HTTP_TIMEOUT: float = float(os.environ.get("MCP_RUSSIA_HTTP_TIMEOUT", "30.0"))
HTTP_MAX_RETRIES: int = int(os.environ.get("MCP_RUSSIA_HTTP_MAX_RETRIES", "3"))
HTTP_BACKOFF_BASE: float = float(os.environ.get("MCP_RUSSIA_HTTP_BACKOFF_BASE", "1.0"))
USER_AGENT: str = os.environ.get("MCP_RUSSIA_USER_AGENT", "mcp-russia/0.5.0")

# --- Поиск инструментов ---
# "bm25" (по умолчанию): BM25-поиск — заменяет list_tools на search_tools + call_tool
# "code_mode": Экспериментальный CodeMode — search + get_tags + execute
# "none": Без трансформации — все 154+ инструментов доступны сразу
TOOL_SEARCH: str = os.environ.get("MCP_RUSSIA_TOOL_SEARCH", "bm25")

# --- ИИ-рекомендации (rekomendovat_instrumenty) ---
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
