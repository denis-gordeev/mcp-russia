"""Справочные данные для слоя Dados Abertos (legacy) — слой обратной совместимости.

NOTE: Это слой обратной совместимости (legacy) в рамках mcp-russia.
Данные бразильского портала открытых данных сохранены для обратной совместимости
и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json


def formatos_disponiveis() -> str:
    """(legacy) Распространённые форматы файлов на портале открытых данных Бразилии."""
    data = [
        {"formato": "CSV", "descricao": "Значения, разделённые запятыми"},
        {"formato": "JSON", "descricao": "JavaScript Object Notation"},
        {"formato": "XML", "descricao": "Extensible Markup Language"},
        {"formato": "XLS/XLSX", "descricao": "Таблица Microsoft Excel"},
        {"formato": "ODS", "descricao": "Open Document Spreadsheet"},
        {"formato": "PDF", "descricao": "Portable Document Format"},
        {"formato": "API", "descricao": "Программный интерфейс"},
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)
