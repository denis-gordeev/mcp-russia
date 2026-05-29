"""HTTP client stubs for the Минобрнауки feature.

All functions are placeholders — real API integration with
minobrnauki.gov.ru / vuz.minobrnauki.gov.ru requires separate work.
"""

from __future__ import annotations


class MinobrnaukiClient:
    """HTTP client stub for Минобрнауки API."""

    def __init__(self, base_url: str = "https://minobrnauki.gov.ru"):
        self.base_url = base_url

    def poluchit_vuz(self, nazvanie: str) -> dict | None:
        """Return данные вуза (placeholder)."""
        return None

    def poluchit_programmy(self, vuz: str, uroven: str = "") -> list[dict]:
        """Return образовательные программы вуза (placeholder)."""
        return []

    def poluchit_granty(self, organizatsiya: str = "") -> list[dict]:
        """Return гранты и научные исследования (placeholder)."""
        return []

    def poluchit_reyting(self, tip_reytinga: str = "", god: int = 0) -> list[dict]:
        """Return рейтинг вузов (placeholder)."""
        return []

    def poluchit_aspirantov(self, organizatsiya: str = "") -> list[dict]:
        """Return данные об аспирантах (placeholder)."""
        return []
