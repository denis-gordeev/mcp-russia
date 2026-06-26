"""Тесты для публичного пространства имён mcp-russia."""

from __future__ import annotations

from mcp_russia import __version__
from mcp_russia.server import mcp, registry
from mcp_russia.server import mcp as legacy_mcp
from mcp_russia.server import registry as legacy_registry


def test_publichnoe_prostranstvo_imen_pereeksportiruet_kornevoy_server() -> None:
    assert mcp is legacy_mcp
    assert registry is legacy_registry


def test_publichnoe_prostranstvo_imen_otkryvaet_versiyu() -> None:
    assert __version__
