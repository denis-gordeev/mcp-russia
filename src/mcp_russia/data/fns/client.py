"""HTTP client stubs for the ФНС feature.

All functions are placeholders — real API integration with
nalog.gov.ru / egrul.nalog.ru requires separate work.
"""

from __future__ import annotations


class FnsClient:
    """HTTP client stub for ФНС API."""

    def __init__(self, base_url: str = "https://api.nalog.ru"):
        self.base_url = base_url

    def poluchit_organizaciyu(self, inn: str) -> dict | None:
        """Return данные организации из ЕГРЮЛ (placeholder)."""
        return None

    def poluchit_ip(self, inn: str) -> dict | None:
        """Return данные ИП из ЕГРИП (placeholder)."""
        return None

    def poluchit_proverki(self, inn: str) -> list[dict]:
        """Return список проверок организации (placeholder)."""
        return []

    def poluchit_nachisleniya(self, inn: str, period: str = "") -> list[dict]:
        """Return налоговые начисления (placeholder)."""
        return []

    def poluchit_svedeniya(self, inn: str) -> dict | None:
        """Return сводные сведения об организации (placeholder)."""
        return None
