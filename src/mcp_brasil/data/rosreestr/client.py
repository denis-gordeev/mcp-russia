"""HTTP client stubs for the Росреестр feature.

All functions are placeholders — real API integration with
rosreestr.gov.ru / pkk.rosreestr.ru requires separate work.
"""

from __future__ import annotations


class RosreestrClient:
    """HTTP client stub for Росреестр API."""

    def __init__(self, base_url: str = "https://rosreestr.gov.ru/api"):
        self.base_url = base_url

    def poluchit_obekt(self, kadastrovyy_nomer: str) -> dict | None:
        """Return данные объекта недвижимости (placeholder)."""
        return None

    def poluchit_kadastrovnuyu_stoimost(self, kadastrovyy_nomer: str) -> dict | None:
        """Return кадастровую стоимость (placeholder)."""
        return None

    def poluchit_prava(self, kadastrovyy_nomer: str) -> list[dict]:
        """Return сведения о правах на объект (placeholder)."""
        return []

    def poluchit_uchastok(self, kadastrovyy_nomer: str) -> dict | None:
        """Return данные земельного участка (placeholder)."""
        return None

    def poluchit_zdanie(self, kadastrovyy_nomer: str) -> dict | None:
        """Return данные здания (placeholder)."""
        return None
