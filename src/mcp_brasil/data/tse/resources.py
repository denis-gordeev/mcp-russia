"""Справочные resources для слоя TSE (legacy) — данные для контекста LLM.

NOTE: Это слой обратной совместимости (legacy) в рамках mcp-russia.
Данные бразильского Высшего избирательного суда сохранены для обратной совместимости
и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import CARGOS_ELEITORAIS, TSE_API_BASE


def cargos_eleitorais() -> str:
    """(legacy) Коды выборных должностей TSE Бразилии."""
    return json.dumps(CARGOS_ELEITORAIS, ensure_ascii=False)


def info_api() -> str:
    """(legacy) Общая информация об API TSE (DivulgaCandContas)."""
    data = {
        "nome": "API DivulgaCandContas — Высший избирательный суд Бразилии (legacy)",
        "url_base": TSE_API_BASE,
        "autenticacao": "Не требует аутентификации",
        "formato": "REST (JSON)",
        "documentacao": "https://divulgacandcontas.tse.jus.br (неофициальная)",
        "cobertura": "Выборы, кандидаты, финансовая отчётность с 2002 года",
        "observacao": "Неофициальное API (reverse-engineered). Без CORS. Рекомендуется rate limit.",
    }
    return json.dumps(data, ensure_ascii=False)
