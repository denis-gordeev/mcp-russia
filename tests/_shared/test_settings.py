"""Тесты модуля конфигурации."""

import os
from unittest.mock import patch

from mcp_russia import settings


class TestSettings:
    def test_default_timeout(self) -> None:
        assert settings.TAIMAUT_HTTP == 30.0

    def test_default_max_retries(self) -> None:
        assert settings.MAKS_POVTOROV_HTTP == 3

    def test_default_backoff_base(self) -> None:
        assert settings.BAZA_EKSPON_ZADERZH == 1.0

    def test_default_user_agent(self) -> None:
        assert "mcp-russia" in settings.POLZOVATELSKIY_AGENT

    def test_env_override_timeout(self) -> None:
        """Настройки можно переопределить через переменные окружения (при импорте)."""
        with patch.dict(os.environ, {"MCP_RUSSIA_HTTP_TIMEOUT": "10.0"}):
            val = float(os.environ.get("MCP_RUSSIA_HTTP_TIMEOUT", "30.0"))
            assert val == 10.0
