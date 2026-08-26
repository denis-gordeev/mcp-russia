"""mcp-russia — Русскоязычный MCP-сервер для государственных и публичных данных РФ."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcp-russia")
except PackageNotFoundError:
    __version__ = "0.6.0"
