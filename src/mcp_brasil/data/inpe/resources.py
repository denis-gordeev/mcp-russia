"""Справочные resources для слоя INPE (legacy) — данные для контекста LLM.

NOTE: Это слой обратной совместимости (legacy/compatibility layer) в рамках mcp-russia.
Эти бразильские экологические справочные данные сохранены для обратной совместимости
с исторической интеграцией INPE и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import BIOMAS, ESTADOS_AMAZONIA_LEGAL


def biomas_brasileiros() -> str:
    """(legacy) Список из 6 бразильских биомов, monitored INPE."""
    data = [{"codigo": k, "nome": v} for k, v in BIOMAS.items()]
    return json.dumps(data, ensure_ascii=False)


def estados_amazonia_legal() -> str:
    """(legacy) Список 9 штатов Legal Amazon (Амазонии) Бразилии."""
    data = [{"sigla": uf} for uf in ESTADOS_AMAZONIA_LEGAL]
    return json.dumps(data, ensure_ascii=False)
