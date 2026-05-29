"""HTTP client stubs for the ФССП feature.

All functions are placeholders — real API integration with
fssp.gov.ru requires separate work.
"""

from __future__ import annotations


class FsspClient:
    """HTTP client stub for ФССП API."""

    def __init__(self, base_url: str = "https://fssp.gov.ru/api"):
        self.base_url = base_url

    def poluchit_proizvodstvo(self, nomer: str) -> dict | None:
        """Return данные исполнительного производства (placeholder)."""
        return None

    def poluchit_proizvodstva_dolzhnika(self, fio: str, data_rozhdeniya: str = "") -> list[dict]:
        """Return список производств по должнику (placeholder)."""
        return []

    def poluchit_ogranicheniya(self, fio: str) -> list[dict]:
        """Return ограничения наложенные на должника (placeholder)."""
        return []

    def poluchit_rozysk(self, fio: str) -> list[dict]:
        """Return сведения о розыске (placeholder)."""
        return []
