"""HTTP client stubs for the Роскомнадзор feature.

All functions are placeholders — real API integration with
rkn.gov.ru requires separate work.
"""

from __future__ import annotations


class RoskomnadzorClient:
    """HTTP client stub for Роскомнадзор API."""

    def __init__(self, base_url: str = "https://rkn.gov.ru/api"):
        self.base_url = base_url

    # stubs — real integration pending
    def get_napravleniya(self) -> list[dict]:
        """Return направления деятельности (placeholder)."""
        return []

    def get_tipy_licenziy(self) -> list[dict]:
        """Return типы лицензий связи (placeholder)."""
        return []

    def get_kategorii_narusheniy(self) -> list[dict]:
        """Return категории нарушений (placeholder)."""
        return []

    def get_reestry(self) -> list[dict]:
        """Return список реестров (placeholder)."""
        return []

    def get_tipy_smi(self) -> list[dict]:
        """Return типы СМИ (placeholder)."""
        return []

    def get_licenziya(self, nomer: str) -> dict | None:
        """Return info лицензии (placeholder)."""
        return None

    def get_smi(self, registracionnyy_nomer: str = "") -> list[dict]:
        """Return список СМИ (placeholder)."""
        return []

    def get_operator_pd(self, inn: str = "") -> list[dict]:
        """Return операторы персональных данных (placeholder)."""
        return []

    def get_narusheniya(self, organizaciya: str = "") -> list[dict]:
        """Return список нарушений (placeholder)."""
        return []

    def get_zapis_reestra(self, reestr_code: str, zapisi_id: str) -> dict | None:
        """Return запись из реестра (placeholder)."""
        return None
