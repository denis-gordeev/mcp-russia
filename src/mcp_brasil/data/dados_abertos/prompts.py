"""Analysis prompts for the Dados Abertos feature.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian open data exploration prompts are kept for backward compatibility
with the historical Dados Abertos integration and are NOT part of the target
Russian data model.
"""

from __future__ import annotations


def explorar_dados(tema: str) -> str:
    """Исследование открытых данных по заданной теме (legacy — Бразилия).

    Args:
        tema: Tema de interesse (ex: saúde, educação, meio ambiente).
    """
    return (
        f"Исследуй доступные открытые данные по теме: '{tema}'.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (Dados Abertos — открытые данные федерального правительства Бразилии).\n\n"
        "Passos:\n"
        f"1. Use buscar_conjuntos(texto='{tema}') para encontrar datasets\n"
        "2. Para cada dataset relevante, use detalhar_conjunto(conjunto_id=...) "
        "para ver detalhes\n"
        "3. Use buscar_recursos(conjunto_id=...) para encontrar os arquivos\n\n"
        "Подготовь отчёт:\n"
        "- Наиболее релевантные наборы данных\n"
        "- Организации-издатели\n"
        "- Доступные форматы\n"
        "- Частота обновления\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
