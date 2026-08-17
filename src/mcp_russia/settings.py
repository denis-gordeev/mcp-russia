"""Глобальная конфигурация mcp-russia.

Значения могут быть переопределены через переменные окружения.
Автоматически загружает файл .env в корне проекта.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# --- HTTP-клиент ---
TAIMAUT_HTTP: float = float(os.environ.get("MCP_RUSSIA_HTTP_TIMEOUT", "30.0"))
MAKS_POVTOROV_HTTP: int = int(os.environ.get("MCP_RUSSIA_HTTP_MAX_RETRIES", "3"))
BAZA_EKSPON_ZADERZH: float = float(os.environ.get("MCP_RUSSIA_HTTP_BACKOFF_BASE", "1.0"))
POLZOVATELSKIY_AGENT: str = os.environ.get("MCP_RUSSIA_USER_AGENT", "mcp-russia/0.6.0")

# --- Поиск инструментов ---
# "bm25" (по умолчанию): BM25-поиск — заменяет spisok_instrumentov
#   на poisk_instrumentov + vypolnit_instrument
# "rezhim_koda": Экспериментальный режим кода — teg + poisk + poluchit_skhemy
# "none": Без трансформации — все 257 инструментов доступны сразу
POISK_INSTRUMENTOV: str = os.environ.get("MCP_RUSSIA_TOOL_SEARCH", "bm25")

# --- Dadata API (РосАПИ) ---
KLYUCH_DADATA_API: str = os.environ.get("MCP_RUSSIA_DADATA_API_KEY", "")

# --- Госдума API ---
KLYUCH_GOSDUMY_API: str = os.environ.get("MCP_RUSSIA_DUMA_API_TOKEN", "")

# --- ЕИС Закупки API ---
KLYUCH_ZAKUPKI_API: str = os.environ.get("MCP_RUSSIA_ZAKUPKI_API_TOKEN", "")

# --- ИИ-рекомендации (rekomendovat_instrumenty) ---
KLYUCH_ANTHROPIC_API: str = os.environ.get("ANTHROPIC_API_KEY", "")
