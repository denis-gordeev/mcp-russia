"""Tests for the public mcp-russia namespace."""

from __future__ import annotations

from mcp_brasil.server import mcp as legacy_mcp
from mcp_brasil.server import registry as legacy_registry
from mcp_russia import __version__
from mcp_russia.server import mcp, registry


def test_public_namespace_reexports_root_server() -> None:
    assert mcp is legacy_mcp
    assert registry is legacy_registry


def test_public_namespace_exposes_version() -> None:
    assert __version__
