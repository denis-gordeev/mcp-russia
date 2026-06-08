"""Глобальные фикстуры для тестов mcp-russia."""

import os

# Отключаем BM25 discovery для тестов, чтобы корневой сервер публиковал все tools
# напрямую. Это должно произойти до импорта модулей mcp_russia.
os.environ.setdefault("MCP_RUSSIA_TOOL_SEARCH", "none")
