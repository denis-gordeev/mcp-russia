"""Resources для DataJud — уровень обратной совместимости для бразильских судебных данных.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные судебной системы сохраняются для обратной совместимости
с исторической интеграцией CNJ DataJud и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json

from .constants import CLASSES_PROCESSUAIS, DATAJUD_API_BASE, TRIBUNAIS, TRIBUNAL_NOMES


def tribunais_disponiveis() -> str:
    """Список доступных судов в API DataJud с аббревиатурами и названиями (legacy)."""
    data = [
        {"sigla": sigla, "nome": TRIBUNAL_NOMES.get(sigla, sigla.upper())}
        for sigla in sorted(TRIBUNAIS.keys())
    ]
    return json.dumps(data, ensure_ascii=False)


def classes_processuais() -> str:
    """Распространённые процессуальные классы для поиска в DataJud (legacy)."""
    return json.dumps(CLASSES_PROCESSUAIS, ensure_ascii=False)


def info_api() -> str:
    """Общая информация об API DataJud (Национальный совет юстиции Бразилии, legacy)."""
    data = {
        "nome": "Публичное API DataJud — Национальный совет юстиции (Бразилия, legacy)",
        "url_base": DATAJUD_API_BASE,
        "autenticacao": "Требует API Key (регистрация на datajud.cnj.jus.br)",
        "formato": "Elasticsearch (POST с телом JSON)",
        "documentacao": "https://datajud-wiki.cnj.jus.br/api-publica/",
        "cobertura": "Дела всех судов Бразилии (уровень обратной совместимости)",
        "total_tribunais": len(TRIBUNAIS),
    }
    return json.dumps(data, ensure_ascii=False)
