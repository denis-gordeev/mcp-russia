"""mcp-russia — Русскоязычная адаптация MCP-сервера для публичных и государственных данных."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcp-russia")
except PackageNotFoundError:
    __version__ = "0.0.0"
