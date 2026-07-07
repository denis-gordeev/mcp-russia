"""Тесты для публичного пространства имён mcp-russia."""

from __future__ import annotations

from mcp_russia import __version__
from mcp_russia.server import mcp, reyestr
from mcp_russia.server import mcp as prezhnyaya_mcp
from mcp_russia.server import reyestr as prezhniy_reyestr


def test_publichnoe_prostranstvo_imen_pereeksportiruet_kornevoy_server() -> None:
    assert mcp is prezhnyaya_mcp
    assert reyestr is prezhniy_reyestr


def test_publichnoe_prostranstvo_imen_otkryvaet_versiyu() -> None:
    assert __version__
