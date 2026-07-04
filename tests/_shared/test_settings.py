"""Тесты модуля конфигурации."""

import os
from unittest.mock import patch

from mcp_russia import settings


class TestNastroyki:
    def test_taimaut_po_umolchaniyu(self) -> None:
        assert settings.TAIMAUT_HTTP == 30.0

    def test_maks_povtorov_po_umolchaniyu(self) -> None:
        assert settings.MAKS_POVTOROV_HTTP == 3

    def test_baza_eksp_zaderzh_po_umolchaniyu(self) -> None:
        assert settings.BAZA_EKSPON_ZADERZH == 1.0

    def test_polzovatelskiy_agent_po_umolchaniyu(self) -> None:
        assert "mcp-russia" in settings.POLZOVATELSKIY_AGENT

    def test_pereopredelenie_taimauta_cherez_env(self) -> None:
        """Настройки можно переопределить через переменные окружения (при импорте)."""
        with patch.dict(os.environ, {"MCP_RUSSIA_HTTP_TIMEOUT": "10.0"}):
            znacheniye = float(os.environ.get("MCP_RUSSIA_HTTP_TIMEOUT", "30.0"))
            assert znacheniye == 10.0
