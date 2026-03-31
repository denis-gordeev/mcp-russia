"""Historical compatibility namespace retained during the mcp-russia migration."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcp-russia")
except PackageNotFoundError:
    __version__ = version("mcp-brasil")
