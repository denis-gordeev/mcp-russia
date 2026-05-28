"""HTTP client stubs for the ГИБДД/МВД feature.

All functions are placeholders — real API integration with
гибдд.рф / gosuslugi.ru requires separate work.
"""

from __future__ import annotations


class GibddClient:
    """HTTP client stub for ГИБДД API."""

    def __init__(self, base_url: str = "https://гибдд.рф"):
        self.base_url = base_url

    def poluchit_info_ts(self, vin: str) -> dict | None:
        """Return данные транспортного средства по VIN (placeholder)."""
        return None

    def poluchit_info_vu(self, nomer_vu: str) -> dict | None:
        """Return данные водительского удостоверения (placeholder)."""
        return None

    def poluchit_shtrafy_po_ts(self, gos_nomer: str) -> list[dict]:
        """Return штрафы по госномеру ТС (placeholder)."""
        return []

    def poluchit_shtrafy_po_vu(self, nomer_vu: str) -> list[dict]:
        """Return штрафы по номеру ВУ (placeholder)."""
        return []

    def poluchit_statistiku_dtp(self, region: str, god: int = 0) -> dict | None:
        """Return статистику ДТП по региону (placeholder)."""
        return None

    def poluchit_istoriyu_registraciy(self, vin: str) -> list[dict]:
        """Return историю регистрационных действий ТС (placeholder)."""
        return []
