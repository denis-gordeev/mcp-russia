"""HTTP client stubs for the Роспотребнадзор feature.

All functions are placeholders — real API integration with
rospotrebnadzor.ru requires separate work.
"""

from __future__ import annotations


class RospotrebnadzorClient:
    """HTTP client stub for Роспотребнадзор API."""

    def __init__(self, base_url: str = "https://rospotrebnadzor.ru/api"):
        self.base_url = base_url

    # stubs — real integration pending
    def get_napravleniya(self) -> list[dict]:
        """Return направления деятельности (placeholder)."""
        return []

    def get_tipy_proverok(self) -> list[dict]:
        """Return типы проверок (placeholder)."""
        return []

    def get_kategorii_obiektov(self) -> list[dict]:
        """Return категории объектов надзора (placeholder)."""
        return []

    def get_regionalnye_upravleniya(self) -> list[dict]:
        """Return региональные управления (placeholder)."""
        return []

    def get_proverka(self, nomer: str) -> dict | None:
        """Return info проверки (placeholder)."""
        return None

    def get_narusheniya(self, organizaciya: str = "") -> list[dict]:
        """Return список нарушений (placeholder)."""
        return []

    def get_pokazateli(self, kod: str = "") -> list[dict]:
        """Return показатели безопасности (placeholder)."""
        return []

    def get_zhaloby(self, organizaciya: str = "") -> list[dict]:
        """Return жалобы потребителей (placeholder)."""
        return []

    def get_sanpiny(self) -> list[dict]:
        """Return список основных СанПиН (placeholder)."""
        return []
