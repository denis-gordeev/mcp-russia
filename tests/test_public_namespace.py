"""Тесты для публичного пространства имён mcp-russia."""

from __future__ import annotations

from mcp_russia import __version__
from mcp_russia.server import mcp, reyestr
from mcp_russia.server import mcp as legacy_mcp
from mcp_russia.server import reyestr as legacy_reyestr


def test_publichnoe_prostranstvo_imen_pereeksportiruet_kornevoy_server() -> None:
    assert mcp is legacy_mcp
    assert reyestr is legacy_reyestr


def test_publichnoe_prostranstvo_imen_otkryvaet_versiyu() -> None:
    assert __version__
